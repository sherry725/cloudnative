import scrapy
import csv
import os
import pandas as pd
from datetime import datetime
import time
from urllib.parse import urljoin, parse_qs, urlparse
import json
import logging

class WhoTrialsSpider(scrapy.Spider):
    name = 'who_trials'
    allowed_domains = ['trialsearch.who.int']
    
    def __init__(self, *args, **kwargs):
        super(WhoTrialsSpider, self).__init__(*args, **kwargs)
        self.keyword = "tricuspid"
        self.csv_file = f"who_trials_{self.keyword}.csv"
        self.existing_trials = set()
        self.base_url = "https://trialsearch.who.int"
        self.search_url = "https://trialsearch.who.int/Trial2.aspx"
        
        # Load existing trial IDs if CSV exists
        self.load_existing_trials()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_existing_trials(self):
        """Load existing trial IDs from CSV to avoid duplicates"""
        if os.path.exists(self.csv_file):
            try:
                df = pd.read_csv(self.csv_file)
                if 'trial_id' in df.columns:
                    self.existing_trials = set(df['trial_id'].astype(str))
                    self.logger.info(f"Loaded {len(self.existing_trials)} existing trials from {self.csv_file}")
                else:
                    self.logger.warning("No 'trial_id' column found in existing CSV")
            except Exception as e:
                self.logger.error(f"Error loading existing CSV: {e}")
        else:
            self.logger.info("No existing CSV file found. Will scrape all trials.")
    
    def start_requests(self):
        """Start the crawling process with search request"""
        # First, get the search page to understand the form structure
        yield scrapy.Request(
            url=self.search_url,
            callback=self.parse_search_page,
            meta={'dont_cache': True}
        )
    
    def parse_search_page(self, response):
        """Parse the search page and submit search form"""
        # Extract form data and viewstate (ASP.NET specific)
        form_data = {
            '__VIEWSTATE': response.css('input[name="__VIEWSTATE"]::attr(value)').get(''),
            '__VIEWSTATEGENERATOR': response.css('input[name="__VIEWSTATEGENERATOR"]::attr(value)').get(''),
            '__EVENTVALIDATION': response.css('input[name="__EVENTVALIDATION"]::attr(value)').get(''),
            'ctl00$ContentPlaceHolder1$txtTitle': self.keyword,
            'ctl00$ContentPlaceHolder1$btnSearch': 'Search'
        }
        
        # Submit search form
        yield scrapy.FormRequest(
            url=self.search_url,
            formdata=form_data,
            callback=self.parse_search_results,
            meta={'page': 1}
        )
    
    def parse_search_results(self, response):
        """Parse search results and extract trial links"""
        current_page = response.meta.get('page', 1)
        self.logger.info(f"Parsing search results page {current_page}")
        
        # Extract trial links from search results
        trial_links = response.css('a[href*="TrialID="]::attr(href)').getall()
        
        if not trial_links:
            # Try alternative selectors
            trial_links = response.css('a[href*="Trial3.aspx"]::attr(href)').getall()
        
        self.logger.info(f"Found {len(trial_links)} trial links on page {current_page}")
        
        # Process each trial link
        for link in trial_links:
            full_url = urljoin(response.url, link)
            
            # Extract trial ID from URL
            parsed_url = urlparse(full_url)
            query_params = parse_qs(parsed_url.query)
            trial_id = query_params.get('TrialID', [''])[0]
            
            if trial_id and trial_id not in self.existing_trials:
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_trial_detail,
                    meta={'trial_id': trial_id}
                )
            elif trial_id:
                self.logger.info(f"Skipping existing trial: {trial_id}")
        
        # Check for next page
        next_page_link = response.css('a[href*="Page$Next"]::attr(href)').get()
        if next_page_link:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_search_results,
                meta={'page': current_page + 1}
            )
    
    def parse_trial_detail(self, response):
        """Parse individual trial detail page"""
        trial_id = response.meta['trial_id']
        
        # Extract trial information
        trial_data = {
            'trial_id': trial_id,
            'url': response.url,
            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'title': self.clean_text(response.css('h2::text').get() or ''),
            'public_title': self.extract_field_value(response, 'Public title'),
            'scientific_title': self.extract_field_value(response, 'Scientific title'),
            'acronym': self.extract_field_value(response, 'Acronym'),
            'primary_sponsor': self.extract_field_value(response, 'Primary sponsor'),
            'secondary_sponsor': self.extract_field_value(response, 'Secondary sponsor'),
            'source_of_monetary': self.extract_field_value(response, 'Source of monetary'),
            'primary_registry': self.extract_field_value(response, 'Primary registry'),
            'trial_id_primary': self.extract_field_value(response, 'Trial ID Primary'),
            'trial_id_secondary': self.extract_field_value(response, 'Trial ID Secondary'),
            'date_registration': self.extract_field_value(response, 'Date of registration'),
            'date_enrolment': self.extract_field_value(response, 'Date of first enrolment'),
            'target_sample_size': self.extract_field_value(response, 'Target sample size'),
            'recruitment_status': self.extract_field_value(response, 'Recruitment status'),
            'study_type': self.extract_field_value(response, 'Study type'),
            'study_design': self.extract_field_value(response, 'Study design'),
            'phase': self.extract_field_value(response, 'Phase'),
            'primary_purpose': self.extract_field_value(response, 'Primary purpose'),
            'intervention': self.extract_field_value(response, 'Intervention'),
            'key_inclusion_criteria': self.extract_field_value(response, 'Key inclusion criteria'),
            'key_exclusion_criteria': self.extract_field_value(response, 'Key exclusion criteria'),
            'primary_outcome': self.extract_field_value(response, 'Primary outcome'),
            'secondary_outcome': self.extract_field_value(response, 'Secondary outcome'),
            'contact_name': self.extract_field_value(response, 'Contact for public queries'),
            'contact_scientific': self.extract_field_value(response, 'Contact for scientific queries'),
            'countries': self.extract_field_value(response, 'Countries of recruitment'),
            'health_conditions': self.extract_field_value(response, 'Health condition(s) or problem(s) studied'),
            'age_group': self.extract_field_value(response, 'Age group'),
            'gender': self.extract_field_value(response, 'Gender'),
            'results_available': self.extract_field_value(response, 'Results available'),
            'date_updated': self.extract_field_value(response, 'Date of last update')
        }
        
        self.logger.info(f"Scraped trial: {trial_id} - {trial_data.get('title', 'No title')[:50]}...")
        
        yield trial_data
    
    def extract_field_value(self, response, field_name):
        """Extract field value by finding the label and getting the next element"""
        # Try multiple approaches to find the field value
        approaches = [
            f'//td[contains(text(), "{field_name}")]/following-sibling::td[1]//text()',
            f'//strong[contains(text(), "{field_name}")]/following::text()[1]',
            f'//b[contains(text(), "{field_name}")]/following::text()[1]',
            f'//label[contains(text(), "{field_name}")]/following-sibling::*//text()',
            f'//*[contains(text(), "{field_name}:")]/following-sibling::*//text()'
        ]
        
        for approach in approaches:
            values = response.xpath(approach).getall()
            if values:
                return self.clean_text(' '.join(values))
        
        return ''
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ''
        return ' '.join(text.strip().split())
    
    def closed(self, reason):
        """Called when spider is closed"""
        self.logger.info(f"Spider closed: {reason}")

# Custom pipeline to save data to CSV
class WhoTrialsPipeline:
    def __init__(self):
        self.items = []
        
    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
    
    def close_spider(self, spider):
        if self.items:
            # Create DataFrame
            df = pd.DataFrame(self.items)
            
            # If CSV exists, append new data
            if os.path.exists(spider.csv_file):
                existing_df = pd.read_csv(spider.csv_file)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                # Remove duplicates based on trial_id
                combined_df = combined_df.drop_duplicates(subset=['trial_id'], keep='first')
            else:
                combined_df = df
            
            # Save to CSV
            combined_df.to_csv(spider.csv_file, index=False)
            spider.logger.info(f"Saved {len(self.items)} new trials to {spider.csv_file}")
            spider.logger.info(f"Total trials in database: {len(combined_df)}")

# Settings for the spider
SPIDER_SETTINGS = {
    'USER_AGENT': 'WHO Trials Spider 1.0',
    'ROBOTSTXT_OBEY': True,
    'DOWNLOAD_DELAY': 1,  # Be respectful - 1 second delay between requests
    'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
    'CONCURRENT_REQUESTS': 1,  # Conservative to avoid overwhelming the server
    'ITEM_PIPELINES': {
        '__main__.WhoTrialsPipeline': 300,
    },
    'HTTPCACHE_ENABLED': False,  # Disable cache to get fresh data
}

# Function to run the spider
def run_spider():
    """Function to run the spider"""
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    
    # Update settings
    settings = get_project_settings()
    settings.update(SPIDER_SETTINGS)
    
    process = CrawlerProcess(settings)
    process.crawl(WhoTrialsSpider)
    process.start()

# Daily scheduler using APScheduler (alternative to cron)
def setup_daily_scheduler():
    """Setup daily scheduler for the spider"""
    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
        from apscheduler.triggers.cron import CronTrigger
        
        scheduler = BlockingScheduler()
        
        # Schedule to run daily at 9:00 AM
        scheduler.add_job(
            run_spider,
            CronTrigger(hour=9, minute=0),
            id='who_trials_daily',
            name='WHO Trials Daily Scraper'
        )
        
        print("Scheduler started. Spider will run daily at 9:00 AM")
        print("Press Ctrl+C to stop the scheduler")
        
        try:
            scheduler.start()
        except KeyboardInterrupt:
            print("Scheduler stopped.")
            
    except ImportError:
        print("APScheduler not installed. Install with: pip install apscheduler")
        print("Alternatively, use cron job to run this script daily")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "schedule":
        setup_daily_scheduler()
    else:
        run_spider()