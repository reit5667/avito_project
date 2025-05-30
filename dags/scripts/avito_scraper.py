import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
import time
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AvitoScraper:
    def __init__(self):
        self.base_url = "https://www.avito.ru/sankt-peterburg/nedvizhimost"
        self.ua = UserAgent()
        
    def get_headers(self):
        """Generate random headers for each request"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

    def get_page(self, url, retries=3):
        """Get page content with retry mechanism"""
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.get_headers())
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.error(f"Error fetching {url}: {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(random.uniform(2, 5))
        return None

    def parse_listing(self, item):
        """Parse individual listing data"""
        try:
            # Extract title
            title = item.find('h3', {'itemprop': 'name'}).text.strip()
            
            # Extract price
            price_elem = item.find('span', {'class': 'price-text-_YGDY'})
            price = price_elem.text.strip() if price_elem else "N/A"
            
            # Extract location
            location_elem = item.find('div', {'class': 'geo-geo'})
            location = location_elem.text.strip() if location_elem else "N/A"
            
            # Extract link
            link_elem = item.find('a', {'class': 'link-link'})
            link = f"https://www.avito.ru{link_elem['href']}" if link_elem else "N/A"
            
            return {
                'title': title,
                'price': price,
                'location': location,
                'link': link,
                'scraped_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parsing listing: {e}")
            return None

    def scrape_page(self, page_num=1):
        """Scrape a single page of listings"""
        url = f"{self.base_url}?p={page_num}"
        logger.info(f"Scraping page {page_num}")
        
        try:
            html = self.get_page(url)
            if not html:
                return []
            
            soup = BeautifulSoup(html, 'lxml')
            listings = soup.find_all('div', {'data-marker': 'item'})
            
            results = []
            for item in listings:
                listing_data = self.parse_listing(item)
                if listing_data:
                    results.append(listing_data)
                time.sleep(random.uniform(0.5, 1.5))  # Be nice to the server
                
            return results
        
        except Exception as e:
            logger.error(f"Error scraping page {page_num}: {e}")
            return []

    def scrape_listings(self, num_pages=5):
        """Scrape multiple pages of listings"""
        all_listings = []
        
        for page in range(1, num_pages + 1):
            listings = self.scrape_page(page)
            all_listings.extend(listings)
            time.sleep(random.uniform(2, 4))  # Delay between pages
            
        return pd.DataFrame(all_listings)

def main():
    """Main function to run the scraper"""
    scraper = AvitoScraper()
    df = scraper.scrape_listings(num_pages=3)  # Scrape 3 pages by default
    
    # Save to CSV with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'avito_listings_{timestamp}.csv'
    df.to_csv(filename, index=False, encoding='utf-8')
    logger.info(f"Saved {len(df)} listings to {filename}")
    
    return filename

if __name__ == '__main__':
    main() 