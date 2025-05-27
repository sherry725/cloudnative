#!/usr/bin/env python3
"""
TAVI Clinical Trials Scraper for ClinicalTrials.gov
Retrieves clinical studies related to Transcatheter Aortic Valve Implantation (TAVI)
"""

import requests
import json
import pandas as pd
import time
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TAVITrialsScraper:
    def __init__(self):
        self.base_url = "https://clinicaltrials.gov/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def search_tavi_studies(self, max_studies: int = 100) -> List[Dict]:
        """
        Search for TAVI-related clinical studies
        """
        # TAVI related search terms
        search_terms = [
            "transcatheter aortic valve implantation",
            "transcatheter aortic valve replacement", 
            "TAVI",
            "TAVR"
        ]
        
        # Create search query
        query = " OR ".join([f'"{term}"' for term in search_terms])
        
        params = {
            'query.term': query,
            'format': 'json',
            'markupFormat': 'markdown',
            'countTotal': 'true',
            'pageSize': min(max_studies, 1000),  # API limit is 1000 per request
            'sortBy': 'LastUpdatePostDate',
            'sortOrder': 'desc'
        }
        
        try:
            logger.info(f"Searching for TAVI studies with query: {query}")
            response = self.session.get(f"{self.base_url}/studies", params=params)
            response.raise_for_status()
            
            data = response.json()
            studies = data.get('studies', [])
            total_count = data.get('totalCount', 0)
            
            logger.info(f"Found {total_count} total studies, retrieved {len(studies)} studies")
            return studies
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching studies: {e}")
            return []
    
    def extract_study_details(self, study: Dict) -> Dict:
        """
        Extract relevant details from a study record
        """
        protocol_section = study.get('protocolSection', {})
        identification_module = protocol_section.get('identificationModule', {})
        status_module = protocol_section.get('statusModule', {})
        design_module = protocol_section.get('designModule', {})
        conditions_module = protocol_section.get('conditionsModule', {})
        arms_interventions_module = protocol_section.get('armsInterventionsModule', {})
        contacts_locations_module = protocol_section.get('contactsLocationsModule', {})
        sponsor_collaborators_module = protocol_section.get('sponsorCollaboratorsModule', {})
        
        # Extract key information
        extracted = {
            'nct_id': identification_module.get('nctId', ''),
            'title': identification_module.get('briefTitle', ''),
            'official_title': identification_module.get('officialTitle', ''),
            'acronym': identification_module.get('acronym', ''),
            'status': status_module.get('overallStatus', ''),
            'phase': design_module.get('phases', []),
            'study_type': design_module.get('studyType', ''),
            'enrollment': design_module.get('enrollmentInfo', {}).get('count', 0),
            'start_date': status_module.get('startDateStruct', {}).get('date', ''),
            'completion_date': status_module.get('primaryCompletionDateStruct', {}).get('date', ''),
            'last_update': status_module.get('lastUpdatePostDateStruct', {}).get('date', ''),
            'conditions': conditions_module.get('conditions', []),
            'interventions': [],
            'locations': [],
            'sponsor': sponsor_collaborators_module.get('leadSponsor', {}).get('name', ''),
            'collaborators': [collab.get('name', '') for collab in sponsor_collaborators_module.get('collaborators', [])],
            'url': f"https://clinicaltrials.gov/study/{identification_module.get('nctId', '')}"
        }
        
        # Extract interventions
        interventions = arms_interventions_module.get('interventions', [])
        for intervention in interventions:
            extracted['interventions'].append({
                'type': intervention.get('type', ''),
                'name': intervention.get('name', ''),
                'description': intervention.get('description', '')
            })
        
        # Extract locations
        locations = contacts_locations_module.get('locations', [])
        for location in locations:
            facility = location.get('facility', {})
            extracted['locations'].append({
                'facility': facility.get('name', ''),
                'city': facility.get('city', ''),
                'country': facility.get('country', ''),
                'status': location.get('status', '')
            })
        
        return extracted
    
    def get_study_details(self, nct_id: str) -> Optional[Dict]:
        """
        Get detailed information for a specific study by NCT ID
        """
        try:
            logger.info(f"Fetching details for study: {nct_id}")
            response = self.session.get(f"{self.base_url}/studies/{nct_id}", 
                                      params={'format': 'json', 'markupFormat': 'markdown'})
            response.raise_for_status()
            
            data = response.json()
            if 'studies' in data and len(data['studies']) > 0:
                return self.extract_study_details(data['studies'][0])
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching study {nct_id}: {e}")
            return None
    
    def scrape_tavi_trials(self, max_studies: int = 100, delay: float = 1.0) -> pd.DataFrame:
        """
        Main scraping function that returns a pandas DataFrame
        """
        logger.info(f"Starting TAVI trials scraping (max {max_studies} studies)")
        
        # Get initial search results
        studies = self.search_tavi_studies(max_studies)
        
        if not studies:
            logger.warning("No studies found")
            return pd.DataFrame()
        
        # Extract details for each study
        detailed_studies = []
        for i, study in enumerate(studies[:max_studies]):
            if i > 0 and delay > 0:
                time.sleep(delay)  # Be respectful to the API
            
            details = self.extract_study_details(study)
            if details:
                detailed_studies.append(details)
                logger.info(f"Processed study {i+1}/{min(len(studies), max_studies)}: {details['nct_id']}")
        
        # Convert to DataFrame
        df = pd.DataFrame(detailed_studies)
        
        # Clean up the data
        if not df.empty:
            df['enrollment'] = pd.to_numeric(df['enrollment'], errors='coerce')
            df['phase'] = df['phase'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
            df['conditions'] = df['conditions'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
            df['collaborators'] = df['collaborators'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
            
        logger.info(f"Scraping completed. Retrieved {len(detailed_studies)} studies")
        return df
    
    def save_results(self, df: pd.DataFrame, filename: str = None):
        """
        Save results to CSV and JSON files
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tavi_trials_{timestamp}"
        
        # Save to CSV
        csv_file = f"{filename}.csv"
        df.to_csv(csv_file, index=False)
        logger.info(f"Results saved to {csv_file}")
        
        # Save to JSON for more detailed data
        json_file = f"{filename}.json"
        df.to_json(json_file, orient='records', indent=2)
        logger.info(f"Results saved to {json_file}")
        
        return csv_file, json_file

def main():
    """
    Main execution function
    """
    scraper = TAVITrialsScraper()
    
    # Scrape TAVI trials (adjust max_studies as needed)
    df = scraper.scrape_tavi_trials(max_studies=50, delay=1.0)
    
    if not df.empty:
        # Display basic statistics
        print(f"\n=== TAVI Clinical Trials Summary ===")
        print(f"Total studies found: {len(df)}")
        print(f"Study statuses: {df['status'].value_counts().to_dict()}")
        print(f"Study types: {df['study_type'].value_counts().to_dict()}")
        print(f"Top sponsors: {df['sponsor'].value_counts().head().to_dict()}")
        
        # Display first few studies
        print(f"\n=== Sample Studies ===")
        for _, study in df.head(3).iterrows():
            print(f"NCT ID: {study['nct_id']}")
            print(f"Title: {study['title']}")
            print(f"Status: {study['status']}")
            print(f"Enrollment: {study['enrollment']}")
            print(f"URL: {study['url']}")
            print("-" * 50)
        
        # Save results
        csv_file, json_file = scraper.save_results(df)
        print(f"\nResults saved to {csv_file} and {json_file}")
        
    else:
        print("No studies found or error occurred during scraping")

if __name__ == "__main__":
    main()