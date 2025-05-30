from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.avito_scraper import AvitoScraper
import os

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'avito_real_estate_scraper',
    default_args=default_args,
    description='Scrapes real estate listings from Avito.ru',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def scrape_avito(**context):
    """Task to scrape Avito listings"""
    scraper = AvitoScraper()
    df = scraper.scrape_listings(num_pages=5)
    
    # Create data directory if it doesn't exist
    data_dir = '/opt/airflow/data'
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to CSV with timestamp
    timestamp = context['execution_date'].strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(data_dir, f'avito_listings_{timestamp}.csv')
    df.to_csv(filename, index=False, encoding='utf-8')
    
    return filename

# Define tasks
scrape_task = PythonOperator(
    task_id='scrape_avito_listings',
    python_callable=scrape_avito,
    provide_context=True,
    dag=dag,
)

# Set task dependencies (only one task for now)
scrape_task 