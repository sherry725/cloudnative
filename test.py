import dimcli
import time
import pandas as pd
from typing import List, Dict, Any

def search_papers_with_error_handling(titles: List[str], delay: float = 1.0) -> Dict[str, Any]:
    """
    Search for papers with comprehensive error handling
    """
    results = {}
    failed_queries = []
    
    dimcli.login()  # Make sure you're logged in
    dsl = dimcli.Dsl()
    
    for i, title in enumerate(titles):
        try:
            print(f"Processing {i+1}/{len(titles)}: {title[:50]}...")
            
            # Clean the title first
            clean_title = clean_title_for_query(title)
            
            # Construct query
            query = f'search publications where title~"{clean_title}" return publications'
            
            # Execute with retry logic
            result = execute_with_retry(dsl, query, max_retries=3)
            
            if result:
                results[title] = result
                print(f"✓ Found {len(result.publications)} results")
            else:
                failed_queries.append(title)
                print("✗ No results found")
                
        except Exception as e:
            print(f"✗ Error with '{title[:50]}...': {str(e)}")
            failed_queries.append(title)
            
        # Rate limiting
        time.sleep(delay)
    
    return {
        'successful_results': results,
        'failed_queries': failed_queries
    }

def clean_title_for_query(title: str) -> str:
    """
    Clean title to avoid query errors
    """
    # Remove or escape problematic characters
    title = title.replace('"', '\\"')  # Escape quotes
    title = title.replace('\\', '')    # Remove backslashes
    title = title.replace('\n', ' ')   # Replace newlines
    title = title.replace('\r', ' ')   # Replace carriage returns
    title = ' '.join(title.split())    # Normalize whitespace
    
    # Truncate if too long (Dimensions has limits)
    if len(title) > 200:
        title = title[:200]
    
    return title

def execute_with_retry(dsl, query: str, max_retries: int = 3) -> Any:
    """
    Execute query with retry logic for temporary failures
    """
    for attempt in range(max_retries):
        try:
            result = dsl.query(query)
            return result
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check if it's a temporary error worth retrying
            if any(temp_error in error_msg for temp_error in 
                   ['timeout', 'rate limit', 'server error', '503', '502', '500']):
                
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff
                    print(f"  Temporary error, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
            
            # For permanent errors or final attempt, re-raise
            raise e
    
    return None

def search_with_fallback_strategies(titles: List[str]) -> Dict[str, Any]:
    """
    Try multiple search strategies if the first fails
    """
    results = {}
    failed_queries = []
    
    dimcli.login()
    dsl = dimcli.Dsl()
    
    for title in titles:
        success = False
        
        # Strategy 1: Exact title search
        try:
            clean_title = clean_title_for_query(title)
            query = f'search publications where title~"{clean_title}" return publications'
            result = dsl.query(query)
            if result and len(result.publications) > 0:
                results[title] = result
                success = True
                print(f"✓ Strategy 1 success: {title[:50]}...")
        except Exception as e:
            print(f"Strategy 1 failed: {str(e)}")
        
        # Strategy 2: Split title into key terms if first fails
        if not success:
            try:
                key_terms = extract_key_terms(title)
                query = f'search publications where title~"{key_terms}" return publications'
                result = dsl.query(query)
                if result and len(result.publications) > 0:
                    results[title] = result
                    success = True
                    print(f"✓ Strategy 2 success: {title[:50]}...")
            except Exception as e:
                print(f"Strategy 2 failed: {str(e)}")
        
        # Strategy 3: Use fuzzy matching with broader search
        if not success:
            try:
                # Remove common words and use broader search
                simplified_title = simplify_title(title)
                query = f'search publications where title~"{simplified_title}" return publications limit 5'
                result = dsl.query(query)
                if result and len(result.publications) > 0:
                    results[title] = result
                    success = True
                    print(f"✓ Strategy 3 success: {title[:50]}...")
            except Exception as e:
                print(f"Strategy 3 failed: {str(e)}")
        
        if not success:
            failed_queries.append(title)
            print(f"✗ All strategies failed: {title[:50]}...")
        
        time.sleep(1)  # Rate limiting
    
    return {
        'successful_results': results,
        'failed_queries': failed_queries
    }

def extract_key_terms(title: str) -> str:
    """
    Extract key terms from title for fallback search
    """
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
    words = title.lower().split()
    key_words = [word for word in words if word not in stop_words and len(word) > 2]
    return ' '.join(key_words[:8])  # Limit to first 8 key terms

def simplify_title(title: str) -> str:
    """
    Create a simplified version of the title
    """
    # Remove special characters and numbers, keep only letters and spaces
    import re
    simplified = re.sub(r'[^a-zA-Z\s]', ' ', title)
    simplified = ' '.join(simplified.split())  # Normalize whitespace
    
    # Take first few words
    words = simplified.split()[:5]
    return ' '.join(words)