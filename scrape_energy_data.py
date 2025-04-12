import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as beauty
from dotenv import load_dotenv
from utils.db import get_engine
from datetime import datetime

# Load environment variables
load_dotenv()

# Constants
URL = 'https://www.energyintel.com/core-service-oil-markets/?q=&f0=&from=&to=&f1=00000179-16a9-d124-a97d-7efb60f50000&f3=0&f4=00000178-eb8d-d3a9-a97a-fbad9c9f0000&f4=00000178-eb8d-d3a9-a97a-fbad9c5b0000&sourceObj='
CSV_PATH = os.path.join("data", "energy_intelligence.csv")
LOG_PATH = os.path.join("logs", "scrape.log")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def scrape_articles():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = beauty(response.text, 'lxml')

        products = soup.find_all('li', class_='SearchResultsModule-results-item')
        all_products = []

        for product in products:
            article_category = product.find('div', class_='PromoO-category')
            article = product.find('div', class_='PromoO-title')
            article_description = product.find('div', class_='PromoO-description')
            date_ = product.find('div', class_='PromoO-date')

            product_info = {
                "article_category": article_category.text.strip() if article_category else None,
                "article": article.text.strip() if article else None,
                "article_description": article_description.text.strip() if article_description else None,
                "date_": date_.text.strip() if date_ else None,
            }
            all_products.append(product_info)

        return pd.DataFrame(all_products)

    except Exception as e:
        log(f"Scraping failed: {e}")
        raise

def save_to_csv(df):
    try:
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        df.to_csv(CSV_PATH, index=False)
        log("Data saved to CSV.")
    except Exception as e:
        log(f"CSV saving failed: {e}")
        raise

def upload_to_postgres(df):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df.to_sql("energy_intelligence", conn, index=False, if_exists="replace")
        log("Data uploaded to PostgreSQL.")
    except Exception as e:
        log(f"PostgreSQL upload failed: {e}")
        raise

if __name__ == "__main__":
    log("Script started.")
    df = scrape_articles()
    save_to_csv(df)
    upload_to_postgres(df)
    log("Script finished successfully.")
