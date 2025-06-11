import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import re

class GrobidTEIParser:
    def __init__(self, xml_file_path: str):
        """Initialize parser with TEI XML file path"""
        self.xml_file_path = xml_file_path
        self.tree = ET.parse(xml_file_path)
        self.root = self.tree.getroot()
        
        # Define TEI namespace
        self.ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    def extract_title(self) -> Optional[str]:
        """Extract paper title"""
        title_elem = self.root.find('.//tei:titleStmt/tei:title[@type="main"]', self.ns)
        if title_elem is None:
            title_elem = self.root.find('.//tei:titleStmt/tei:title', self.ns)
        
        if title_elem is not None:
            return self._get_text_content(title_elem).strip()
        return None
    
    def extract_authors(self) -> List[Dict[str, str]]:
        """Extract author information including names and affiliations"""
        authors = []
        
        # Find all authors in the source description
        author_elems = self.root.findall('.//tei:sourceDesc//tei:author', self.ns)
        
        for author_elem in author_elems:
            author_info = {}
            
            # Extract name
            name_elem = author_elem.find('.//tei:persName', self.ns)
            if name_elem is not None:
                # Try to get structured name
                forename = name_elem.find('tei:forename', self.ns)
                surname = name_elem.find('tei:surname', self.ns)
                
                if forename is not None and surname is not None:
                    author_info['name'] = f"{forename.text} {surname.text}"
                else:
                    # Fall back to full name text
                    author_info['name'] = self._get_text_content(name_elem).strip()
            
            # Extract email
            email_elem = author_elem.find('.//tei:email', self.ns)
            if email_elem is not None:
                author_info['email'] = email_elem.text
            
            # Extract affiliation
            affiliation_elems = author_elem.findall('.//tei:affiliation', self.ns)
            affiliations = []
            for aff_elem in affiliation_elems:
                aff_text = self._get_text_content(aff_elem).strip()
                if aff_text:
                    affiliations.append(aff_text)
            
            if affiliations:
                author_info['affiliations'] = affiliations
            
            if author_info:  # Only add if we found some information
                authors.append(author_info)
        
        return authors
    
    def extract_affiliations(self) -> List[Dict[str, str]]:
        """Extract all affiliations with their IDs"""
        affiliations = []
        
        # Look for affiliations in the header
        aff_elems = self.root.findall('.//tei:sourceDesc//tei:affiliation', self.ns)
        
        for aff_elem in aff_elems:
            aff_info = {}
            
            # Get affiliation ID if available
            aff_id = aff_elem.get('key') or aff_elem.get('xml:id')
            if aff_id:
                aff_info['id'] = aff_id
            
            # Get affiliation text
            aff_text = self._get_text_content(aff_elem).strip()
            if aff_text:
                aff_info['text'] = aff_text
            
            # Try to extract organization name
            org_elem = aff_elem.find('.//tei:orgName', self.ns)
            if org_elem is not None:
                aff_info['organization'] = org_elem.text
            
            # Try to extract address
            address_elem = aff_elem.find('.//tei:address', self.ns)
            if address_elem is not None:
                aff_info['address'] = self._get_text_content(address_elem).strip()
            
            if aff_info:
                affiliations.append(aff_info)
        
        return affiliations
    
    def extract_abstract(self) -> Optional[str]:
        """Extract paper abstract"""
        abstract_elem = self.root.find('.//tei:abstract', self.ns)
        if abstract_elem is not None:
            return self._get_text_content(abstract_elem).strip()
        return None
    
    def extract_references(self) -> List[Dict[str, str]]:
        """Extract bibliography references"""
        references = []
        
        # Find all bibliography entries
        bibl_elems = self.root.findall('.//tei:listBibl/tei:biblStruct', self.ns)
        
        for bibl_elem in bibl_elems:
            ref_info = {}
            
            # Get reference ID
            ref_id = bibl_elem.get('xml:id')
            if ref_id:
                ref_info['id'] = ref_id
            
            # Extract title
            title_elem = bibl_elem.find('.//tei:title[@level="a"]', self.ns)  # Article title
            if title_elem is None:
                title_elem = bibl_elem.find('.//tei:title', self.ns)  # Any title
            
            if title_elem is not None:
                ref_info['title'] = self._get_text_content(title_elem).strip()
            
            # Extract authors
            author_elems = bibl_elem.findall('.//tei:author', self.ns)
            authors = []
            for author_elem in author_elems:
                name_elem = author_elem.find('.//tei:persName', self.ns)
                if name_elem is not None:
                    author_name = self._get_text_content(name_elem).strip()
                    if author_name:
                        authors.append(author_name)
            
            if authors:
                ref_info['authors'] = authors
            
            # Extract journal/conference name
            journal_elem = bibl_elem.find('.//tei:title[@level="j"]', self.ns)  # Journal
            if journal_elem is None:
                journal_elem = bibl_elem.find('.//tei:title[@level="m"]', self.ns)  # Monograph/Book
            
            if journal_elem is not None:
                ref_info['venue'] = self._get_text_content(journal_elem).strip()
            
            # Extract publication year
            date_elem = bibl_elem.find('.//tei:date[@type="published"]', self.ns)
            if date_elem is None:
                date_elem = bibl_elem.find('.//tei:date', self.ns)
            
            if date_elem is not None:
                year = date_elem.get('when')
                if year:
                    ref_info['year'] = year
                else:
                    date_text = date_elem.text
                    if date_text:
                        # Try to extract year from date text
                        year_match = re.search(r'\b(19|20)\d{2}\b', date_text)
                        if year_match:
                            ref_info['year'] = year_match.group()
            
            # Extract pages
            page_elem = bibl_elem.find('.//tei:biblScope[@unit="page"]', self.ns)
            if page_elem is not None:
                ref_info['pages'] = page_elem.text
            
            # Extract volume
            vol_elem = bibl_elem.find('.//tei:biblScope[@unit="volume"]', self.ns)
            if vol_elem is not None:
                ref_info['volume'] = vol_elem.text
            
            # Extract DOI
            doi_elem = bibl_elem.find('.//tei:idno[@type="DOI"]', self.ns)
            if doi_elem is not None:
                ref_info['doi'] = doi_elem.text
            
            if ref_info:
                references.append(ref_info)
        
        return references
    
    def extract_keywords(self) -> List[str]:
        """Extract keywords if available"""
        keywords = []
        keyword_elems = self.root.findall('.//tei:keywords//tei:term', self.ns)
        
        for keyword_elem in keyword_elems:
            keyword = keyword_elem.text
            if keyword:
                keywords.append(keyword.strip())
        
        return keywords
    
    def _get_text_content(self, element) -> str:
        """Get all text content from an element, including subelements"""
        text_parts = []
        
        if element.text:
            text_parts.append(element.text)
        
        for child in element:
            text_parts.append(self._get_text_content(child))
            if child.tail:
                text_parts.append(child.tail)
        
        return ' '.join(text_parts)
    
    def extract_all(self) -> Dict:
        """Extract all information and return as dictionary"""
        return {
            'title': self.extract_title(),
            'authors': self.extract_authors(),
            'affiliations': self.extract_affiliations(),
            'abstract': self.extract_abstract(),
            'keywords': self.extract_keywords(),
            'references': self.extract_references()
        }

# Example usage
def main():
    # Replace with your TEI XML file path
    xml_file = "path/to/your/grobid_output.tei.xml"
    
    try:
        parser = GrobidTEIParser(xml_file)
        
        # Extract individual components
        print("Title:", parser.extract_title())
        print("\nAuthors:")
        for author in parser.extract_authors():
            print(f"  - {author}")
        
        print("\nAffiliations:")
        for aff in parser.extract_affiliations():
            print(f"  - {aff}")
        
        print("\nAbstract:", parser.extract_abstract())
        
        print("\nKeywords:", parser.extract_keywords())
        
        print(f"\nReferences ({len(parser.extract_references())} found):")
        for i, ref in enumerate(parser.extract_references()[:3]):  # Show first 3
            print(f"  {i+1}. {ref}")
        
        # Or extract everything at once
        all_data = parser.extract_all()
        print(f"\nComplete extraction: {len(all_data)} fields extracted")
        
    except FileNotFoundError:
        print(f"Error: Could not find XML file at {xml_file}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()


from lxml import etree
from bs4 import BeautifulSoup, NavigableString
import re
from typing import List, Dict, Optional, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustGrobidTEIParser:
    def __init__(self, xml_file_path: str):
        """Initialize parser with TEI XML file path using lxml and BeautifulSoup"""
        self.xml_file_path = xml_file_path
        
        # Try to parse with lxml first (faster and more strict)
        try:
            with open(xml_file_path, 'r', encoding='utf-8') as file:
                self.lxml_tree = etree.parse(file)
                self.lxml_root = self.lxml_tree.getroot()
            logger.info("Successfully parsed with lxml")
        except Exception as e:
            logger.warning(f"lxml parsing failed: {e}")
            self.lxml_tree = None
            self.lxml_root = None
        
        # Parse with BeautifulSoup (more forgiving)
        try:
            with open(xml_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.soup = BeautifulSoup(content, 'xml')
            logger.info("Successfully parsed with BeautifulSoup")
        except Exception as e:
            logger.error(f"BeautifulSoup parsing failed: {e}")
            raise
        
        # Define TEI namespace for lxml
        self.ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    def extract_title(self) -> Optional[str]:
        """Extract paper title using both lxml and BeautifulSoup fallback"""
        title = None
        
        # Try lxml first
        if self.lxml_root is not None:
            try:
                title_elem = self.lxml_root.find('.//tei:titleStmt/tei:title[@type="main"]', self.ns)
                if title_elem is None:
                    title_elem = self.lxml_root.find('.//tei:titleStmt/tei:title', self.ns)
                
                if title_elem is not None:
                    title = self._get_lxml_text(title_elem).strip()
            except Exception as e:
                logger.warning(f"lxml title extraction failed: {e}")
        
        # Fallback to BeautifulSoup
        if not title:
            try:
                title_elem = self.soup.find('title', {'type': 'main'})
                if not title_elem:
                    title_elem = self.soup.find('title')
                
                if title_elem:
                    title = self._get_bs4_text(title_elem).strip()
            except Exception as e:
                logger.warning(f"BeautifulSoup title extraction failed: {e}")
        
        return title
    
    def extract_authors(self) -> List[Dict[str, Union[str, List[str]]]]:
        """Extract comprehensive author information"""
        authors = []
        
        # Try BeautifulSoup first (more flexible for complex structures)
        try:
            author_elems = self.soup.find_all('author')
            
            for author_elem in author_elems:
                author_info = {}
                
                # Extract name with multiple strategies
                name = self._extract_author_name(author_elem)
                if name:
                    author_info['name'] = name
                
                # Extract email
                email_elem = author_elem.find('email')
                if email_elem:
                    author_info['email'] = email_elem.get_text(strip=True)
                
                # Extract affiliations (multiple possible)
                affiliations = self._extract_author_affiliations(author_elem)
                if affiliations:
                    author_info['affiliations'] = affiliations
                
                # Extract ORCID if available
                orcid = self._extract_orcid(author_elem)
                if orcid:
                    author_info['orcid'] = orcid
                
                if author_info:
                    authors.append(author_info)
                    
        except Exception as e:
            logger.warning(f"BeautifulSoup author extraction failed: {e}")
            
            # Fallback to lxml
            if self.lxml_root is not None:
                try:
                    author_elems = self.lxml_root.findall('.//tei:author', self.ns)
                    for author_elem in author_elems:
                        author_info = {}
                        
                        name_elem = author_elem.find('.//tei:persName', self.ns)
                        if name_elem is not None:
                            author_info['name'] = self._get_lxml_text(name_elem).strip()
                        
                        if author_info:
                            authors.append(author_info)
                except Exception as e2:
                    logger.error(f"lxml author fallback failed: {e2}")
        
        return authors
    
    def _extract_author_name(self, author_elem) -> Optional[str]:
        """Extract author name with multiple fallback strategies"""
        # Strategy 1: Structured name (forename + surname)
        persname = author_elem.find('persName')
        if persname:
            forename = persname.find('forename')
            surname = persname.find('surname')
            
            if forename and surname:
                forename_text = self._get_bs4_text(forename).strip()
                surname_text = self._get_bs4_text(surname).strip()
                if forename_text and surname_text:
                    return f"{forename_text} {surname_text}"
            
            # Strategy 2: Full persName text
            persname_text = self._get_bs4_text(persname).strip()
            if persname_text:
                return persname_text
        
        # Strategy 3: Direct author text
        author_text = self._get_bs4_text(author_elem).strip()
        if author_text:
            # Clean up - remove email and affiliation info
            author_text = re.sub(r'\S+@\S+', '', author_text)  # Remove emails
            author_text = re.sub(r'\d+', '', author_text)      # Remove affiliation numbers
            return author_text.strip()
        
        return None
    
    def _extract_author_affiliations(self, author_elem) -> List[str]:
        """Extract all affiliations for an author"""
        affiliations = []
        
        # Direct affiliation elements
        aff_elems = author_elem.find_all('affiliation')
        for aff_elem in aff_elems:
            aff_text = self._get_bs4_text(aff_elem).strip()
            if aff_text:
                affiliations.append(aff_text)
        
        # Affiliation references (common in GROBID)
        aff_refs = author_elem.find_all('affiliation', {'ref': True})
        for aff_ref in aff_refs:
            ref_id = aff_ref.get('ref')
            if ref_id:
                # Find the referenced affiliation
                target_aff = self.soup.find('affiliation', {'xml:id': ref_id})
                if target_aff:
                    aff_text = self._get_bs4_text(target_aff).strip()
                    if aff_text:
                        affiliations.append(aff_text)
        
        return affiliations
    
    def _extract_orcid(self, author_elem) -> Optional[str]:
        """Extract ORCID identifier if available"""
        # Look for ORCID in various formats
        orcid_elem = author_elem.find('idno', {'type': 'ORCID'})
        if orcid_elem:
            return orcid_elem.get_text(strip=True)
        
        # Check for ORCID in href attributes
        orcid_link = author_elem.find('ptr', {'target': re.compile(r'orcid\.org')})
        if orcid_link:
            target = orcid_link.get('target', '')
            orcid_match = re.search(r'(\d{4}-\d{4}-\d{4}-\d{3}[\dX])', target)
            if orcid_match:
                return orcid_match.group(1)
        
        return None
    
    def extract_affiliations(self) -> List[Dict[str, str]]:
        """Extract all unique affiliations"""
        affiliations = []
        seen_affiliations = set()
        
        try:
            aff_elems = self.soup.find_all('affiliation')
            
            for aff_elem in aff_elems:
                aff_info = {}
                
                # Get affiliation ID
                aff_id = aff_elem.get('xml:id') or aff_elem.get('key')
                if aff_id:
                    aff_info['id'] = aff_id
                
                # Get full affiliation text
                aff_text = self._get_bs4_text(aff_elem).strip()
                if aff_text and aff_text not in seen_affiliations:
                    aff_info['text'] = aff_text
                    seen_affiliations.add(aff_text)
                    
                    # Try to extract structured information
                    org_elem = aff_elem.find('orgName')
                    if org_elem:
                        aff_info['organization'] = self._get_bs4_text(org_elem).strip()
                    
                    # Extract address components
                    address_parts = []
                    for addr_elem in aff_elem.find_all(['address', 'settlement', 'country']):
                        addr_text = self._get_bs4_text(addr_elem).strip()
                        if addr_text:
                            address_parts.append(addr_text)
                    
                    if address_parts:
                        aff_info['address'] = ', '.join(address_parts)
                    
                    affiliations.append(aff_info)
                    
        except Exception as e:
            logger.warning(f"Affiliation extraction failed: {e}")
        
        return affiliations
    
    def extract_abstract(self) -> Optional[str]:
        """Extract abstract with robust text handling"""
        try:
            abstract_elem = self.soup.find('abstract')
            if abstract_elem:
                # Remove any nested div or p tags and get clean text
                abstract_text = self._get_bs4_text(abstract_elem).strip()
                # Clean up extra whitespace
                abstract_text = re.sub(r'\s+', ' ', abstract_text)
                return abstract_text
        except Exception as e:
            logger.warning(f"Abstract extraction failed: {e}")
        
        return None
    
    def extract_references(self) -> List[Dict[str, Union[str, List[str]]]]:
        """Extract comprehensive reference information"""
        references = []
        
        try:
            # Look for bibliography structures
            bibl_elems = self.soup.find_all('biblStruct')
            
            for i, bibl_elem in enumerate(bibl_elems):
                ref_info = {'index': i + 1}
                
                # Extract reference ID
                ref_id = bibl_elem.get('xml:id')
                if ref_id:
                    ref_info['id'] = ref_id
                
                # Extract title with fallback strategies
                title = self._extract_reference_title(bibl_elem)
                if title:
                    ref_info['title'] = title
                
                # Extract authors
                authors = self._extract_reference_authors(bibl_elem)
                if authors:
                    ref_info['authors'] = authors
                
                # Extract venue (journal/conference)
                venue = self._extract_reference_venue(bibl_elem)
                if venue:
                    ref_info['venue'] = venue
                
                # Extract date/year
                year = self._extract_reference_year(bibl_elem)
                if year:
                    ref_info['year'] = year
                
                # Extract additional metadata
                metadata = self._extract_reference_metadata(bibl_elem)
                ref_info.update(metadata)
                
                # Extract raw text as fallback
                if len(ref_info) <= 2:  # Only has index and maybe id
                    raw_text = self._get_bs4_text(bibl_elem).strip()
                    if raw_text:
                        ref_info['raw_text'] = raw_text
                
                references.append(ref_info)
                
        except Exception as e:
            logger.warning(f"Reference extraction failed: {e}")
        
        return references
    
    def _extract_reference_title(self, bibl_elem) -> Optional[str]:
        """Extract reference title with multiple strategies"""
        # Strategy 1: Article title
        title_elem = bibl_elem.find('title', {'level': 'a'})
        if title_elem:
            return self._get_bs4_text(title_elem).strip()
        
        # Strategy 2: Any title
        title_elem = bibl_elem.find('title')
        if title_elem:
            return self._get_bs4_text(title_elem).strip()
        
        return None
    
    def _extract_reference_authors(self, bibl_elem) -> List[str]:
        """Extract reference authors"""
        authors = []
        author_elems = bibl_elem.find_all('author')
        
        for author_elem in author_elems:
            name = self._extract_author_name(author_elem)
            if name:
                authors.append(name)
        
        return authors
    
    def _extract_reference_venue(self, bibl_elem) -> Optional[str]:
        """Extract publication venue"""
        # Journal
        venue_elem = bibl_elem.find('title', {'level': 'j'})
        if venue_elem:
            return self._get_bs4_text(venue_elem).strip()
        
        # Book/Monograph
        venue_elem = bibl_elem.find('title', {'level': 'm'})
        if venue_elem:
            return self._get_bs4_text(venue_elem).strip()
        
        return None
    
    def _extract_reference_year(self, bibl_elem) -> Optional[str]:
        """Extract publication year"""
        # Published date
        date_elem = bibl_elem.find('date', {'type': 'published'})
        if not date_elem:
            date_elem = bibl_elem.find('date')
        
        if date_elem:
            # Check 'when' attribute first
            when = date_elem.get('when')
            if when:
                year_match = re.search(r'\b(19|20)\d{2}\b', when)
                if year_match:
                    return year_match.group()
            
            # Extract from text
            date_text = self._get_bs4_text(date_elem)
            year_match = re.search(r'\b(19|20)\d{2}\b', date_text)
            if year_match:
                return year_match.group()
        
        return None
    
    def _extract_reference_metadata(self, bibl_elem) -> Dict[str, str]:
        """Extract additional reference metadata"""
        metadata = {}
        
        # Pages
        page_elem = bibl_elem.find('biblScope', {'unit': 'page'})
        if page_elem:
            metadata['pages'] = self._get_bs4_text(page_elem).strip()
        
        # Volume
        vol_elem = bibl_elem.find('biblScope', {'unit': 'volume'})
        if vol_elem:
            metadata['volume'] = self._get_bs4_text(vol_elem).strip()
        
        # Issue
        issue_elem = bibl_elem.find('biblScope', {'unit': 'issue'})
        if issue_elem:
            metadata['issue'] = self._get_bs4_text(issue_elem).strip()
        
        # DOI
        doi_elem = bibl_elem.find('idno', {'type': 'DOI'})
        if doi_elem:
            metadata['doi'] = self._get_bs4_text(doi_elem).strip()
        
        # arXiv
        arxiv_elem = bibl_elem.find('idno', {'type': 'arXiv'})
        if arxiv_elem:
            metadata['arxiv'] = self._get_bs4_text(arxiv_elem).strip()
        
        return metadata
    
    def extract_keywords(self) -> List[str]:
        """Extract keywords with robust handling"""
        keywords = []
        
        try:
            # Multiple possible structures
            keyword_elems = self.soup.find_all('term')
            for term_elem in keyword_elems:
                keyword = self._get_bs4_text(term_elem).strip()
                if keyword:
                    keywords.append(keyword)
            
            # Alternative structure
            if not keywords:
                keywords_section = self.soup.find('keywords')
                if keywords_section:
                    # Split by common delimiters
                    keywords_text = self._get_bs4_text(keywords_section)
                    keywords = [k.strip() for k in re.split(r'[,;·]', keywords_text) if k.strip()]
                    
        except Exception as e:
            logger.warning(f"Keywords extraction failed: {e}")
        
        return keywords
    
    def _get_bs4_text(self, element) -> str:
        """Get clean text from BeautifulSoup element"""
        if element is None:
            return ""
        
        # Get text with proper spacing
        text = element.get_text(separator=' ', strip=True)
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _get_lxml_text(self, element) -> str:
        """Get clean text from lxml element"""
        if element is None:
            return ""
        
        # Get all text content including subelements
        text_parts = []
        
        if element.text:
            text_parts.append(element.text.strip())
        
        for child in element:
            child_text = self._get_lxml_text(child)
            if child_text:
                text_parts.append(child_text)
            if child.tail:
                text_parts.append(child.tail.strip())
        
        text = ' '.join(text_parts)
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def extract_all(self) -> Dict:
        """Extract all information with error handling"""
        result = {}
        
        try:
            result['title'] = self.extract_title()
        except Exception as e:
            logger.error(f"Title extraction failed: {e}")
            result['title'] = None
        
        try:
            result['authors'] = self.extract_authors()
        except Exception as e:
            logger.error(f"Authors extraction failed: {e}")
            result['authors'] = []
        
        try:
            result['affiliations'] = self.extract_affiliations()
        except Exception as e:
            logger.error(f"Affiliations extraction failed: {e}")
            result['affiliations'] = []
        
        try:
            result['abstract'] = self.extract_abstract()
        except Exception as e:
            logger.error(f"Abstract extraction failed: {e}")
            result['abstract'] = None
        
        try:
            result['keywords'] = self.extract_keywords()
        except Exception as e:
            logger.error(f"Keywords extraction failed: {e}")
            result['keywords'] = []
        
        try:
            result['references'] = self.extract_references()
        except Exception as e:
            logger.error(f"References extraction failed: {e}")
            result['references'] = []
        
        return result

# Utility functions for batch processing
def process_multiple_files(file_paths: List[str]) -> List[Dict]:
    """Process multiple TEI XML files"""
    results = []
    
    for file_path in file_paths:
        try:
            logger.info(f"Processing {file_path}")
            parser = RobustGrobidTEIParser(file_path)
            data = parser.extract_all()
            data['source_file'] = file_path
            results.append(data)
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            results.append({
                'source_file': file_path,
                'error': str(e)
            })
    
    return results

def export_to_json(data: Union[Dict, List[Dict]], output_file: str):
    """Export extracted data to JSON"""
    import json
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Data exported to {output_file}")

# Example usage
def main():
    # Single file processing
    xml_file = "path/to/your/grobid_output.tei.xml"
    
    try:
        parser = RobustGrobidTEIParser(xml_file)
        
        # Extract all data
        all_data = parser.extract_all()
        
        # Print summary
        print(f"Title: {all_data['title']}")
        print(f"Authors: {len(all_data['authors'])} found")
        print(f"Affiliations: {len(all_data['affiliations'])} found")
        print(f"References: {len(all_data['references'])} found")
        print(f"Keywords: {len(all_data['keywords'])} found")
        
        # Export to JSON
        export_to_json(all_data, "extracted_data.json")
        
        # Batch processing example
        # file_list = ["file1.tei.xml", "file2.tei.xml", "file3.tei.xml"]
        # batch_results = process_multiple_files(file_list)
        # export_to_json(batch_results, "batch_results.json")
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")

if __name__ == "__main__":
    main()