import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as beauty
from dotenv import load_dotenv
from utils.db import get_engine
from datetime import datetime
from dateutil import parser

# Load environment variables
load_dotenv()

# Constants
URL = 'https://www.energyintel.com/core-service-oil-markets/?q=&f0=&from=&to=&f1=00000179-16a9-d124-a97d-7efb60f50000&f3=0&f4=00000178-eb8d-d3a9-a97a-fbad9c9f0000&f4=00000178-eb8d-d3a9-a97a-fbad9c5b0000&sourceObj='
CSV_PATH = os.path.join("data", "energy_intelligence.csv")
LOG_PATH = os.path.join("logs", "scrape.log")

def log(message: str):
    """Write a message to the log file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def scrape_articles() -> pd.DataFrame:
    """Scrape articles from Energy Intelligence and return as DataFrame."""
    log("Scraping articles from Energy Intelligence...")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = beauty(response.text, 'lxml')

        products = soup.find_all('li', class_='SearchResultsModule-results-item')
        if not products:
            log("No articles found on the page.")
            return pd.DataFrame()

        all_products = []
        for product in products:
            article_category = product.find('div', class_='PromoO-category')
            article = product.find('div', class_='PromoO-title')
            article_description = product.find('div', class_='PromoO-description')
            date_ = product.find('div', class_='PromoO-date')

            try:
                parsed_date = parser.parse(date_.text.strip()).date() if date_ else None
            except Exception:
                parsed_date = None

            product_info = {
                "article_category": article_category.text.strip() if article_category else None,
                "article": article.text.strip() if article else None,
                "article_description": article_description.text.strip() if article_description else None,
                "date_": parsed_date,
            }
            all_products.append(product_info)

        df = pd.DataFrame(all_products)
        df.drop_duplicates(subset=["article"], inplace=True)
        log(f"Scraped {len(df)} unique articles.")
        if not df.empty:
            log("Top 3 articles scraped:\n" + df.head(3).to_string(index=False))
        return df

    except Exception as e:
        log(f"Scraping failed: {str(e)}")
        raise

def save_to_csv(df: pd.DataFrame):
    """Save the DataFrame to a CSV file."""
    log("Saving DataFrame to CSV...")
    try:
        if df.empty:
            log("No data to save.")
            return
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        df.to_csv(CSV_PATH, index=False)
        log(f"Data saved to {CSV_PATH}.")
    except Exception as e:
        log(f"CSV saving failed: {str(e)}")
        raise

def upload_to_postgres(df: pd.DataFrame):
    """Upload the DataFrame to a PostgreSQL table."""
    log("Uploading DataFrame to PostgreSQL...")
    try:
        if df.empty:
            log("No data to upload to PostgreSQL.")
            return
        engine = get_engine()
        with engine.connect() as conn:
            df.to_sql("energy_intelligence", conn, index=False, if_exists="replace")
        log("Data uploaded to PostgreSQL table 'energy_intelligence'.")
    except Exception as e:
        log(f"PostgreSQL upload failed: {str(e)}")
        raise

if __name__ == "__main__":
    log("Script started.")
    df = scrape_articles()
    save_to_csv(df)
    upload_to_postgres(df)
    log("Script finished successfully.")
