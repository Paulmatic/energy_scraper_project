# Energy Scraper Project

## Overview

The Energy Scraper Project is a Python-based tool that scrapes articles related to energy markets from Energy Intelligence. It collects the articles, saves them to a CSV file, and uploads the data to a PostgreSQL database. The project is containerized with Docker for easy deployment and includes a Jenkins pipeline for continuous integration.

## Features

- Scrapes energy market articles from Energy Intelligence
- Saves data to a CSV file
- Uploads data to a PostgreSQL database
- Containerized using Docker
- CI/CD with Jenkins

## Prerequisites

- Docker
- Docker Compose
- PostgreSQL

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Paulmatic/energy_scraper_project.git
   cd energy_scraper_project

## Set up environment variables:

2. Create a .env file in the root directory and add the necessary environment variables:

DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name
Build and run the Docker containers:

3. docker-compose up --build
Access pgAdmin at http://localhost:8082, login with the credentials from your .env file.

The scraper will run automatically and start scraping data.

4. Usage
The script will scrape the articles and save the data to a CSV file located in the data directory.

It will also upload the data to a PostgreSQL table named energy_intelligence.

5. License
This project is licensed under the MIT License - see the LICENSE file for details.