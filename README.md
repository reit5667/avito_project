# Avito Real Estate Parser

This Apache Airflow project scrapes real estate listings from Avito.ru (Saint Petersburg region) and stores the data for analysis.

## Project Structure

```
avito_project/
├── dags/                    # Airflow DAG files
│   ├── avito_parser_dag.py # Main DAG file
│   └── scripts/            # Supporting Python scripts
│       └── avito_scraper.py # Scraping logic
├── docker-compose.yml      # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

- Scrapes real estate listings from Avito.ru (Saint Petersburg)
- Extracts key information:
  - Title
  - Price
  - Location
  - Description
  - Parameters (area, floor, etc.)
  - Publication date
- Stores data in structured format
- Runs on a schedule via Airflow

## Prerequisites

- Docker and Docker Compose
- Python 3.8 or later

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd avito_project
```

2. Create required directories:
```bash
mkdir -p ./dags ./logs ./plugins
```

3. Start Airflow using Docker Compose:
```bash
docker-compose up -d
```

4. Access the Airflow web interface:
- URL: http://localhost:8080
- Username: airflow
- Password: airflow

## Usage

The DAG is scheduled to run daily and will:
1. Scrape new listings from Avito
2. Process and clean the data
3. Store results in a CSV file

## Notes

- Please respect Avito.ru's robots.txt and terms of service
- Use appropriate delays between requests
- This is for educational purposes only

## License

MIT License 