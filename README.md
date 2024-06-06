# AI Platform User and Metadata Analysis

## Project Purpose
This project is designed to create an end-to-end data pipeline for ingesting and analyzing user and metadata from various AI platforms. The goal is to demonstrate data engineering skills through the development, implementation, and documentation of a comprehensive data pipeline.

## Table of Contents
- [Project Purpose](#project-purpose)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
- [Usage](#usage)
- [Data Fields](#data-fields)
- [Comments Within Code](#comments-within-code)
- [Additional Documentation](#additional-documentation)
- [GitHub Repository Structure](#github-repository-structure)
- [Contributing](#contributing)
- [License](#license)

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- MySQL
- pip (Python package installer)

### Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ai-platform-user-metadata.git
    cd ai-platform-user-metadata
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup
1. **Start MySQL server:**

2. **Create a database:**
    ```sql
    CREATE DATABASE data_pipeline;
    ```

3. **Update database credentials:**
   Update the following lines in `main.py` with your MySQL credentials:
    ```python
    dbname = "data_pipeline"
    user = "your_username"
    password = "your_password"
    host = "localhost"
    ```

## Usage

1. **Generate and ingest data:**
    ```bash
    python main.py
    ```

   This will:
   - Generate 100,000 user records across ten AI platforms.
   - Create tables in the `data_pipeline` database.
   - Ingest the generated data into the corresponding tables.

## Data Fields

Each table represents user data for a specific AI platform and contains the following fields:

- `id`: INT, Auto Increment, Primary Key
- `user_id`: VARCHAR(10), Unique identifier for the user
- `name`: VARCHAR(100), User's name
- `email`: VARCHAR(100), User's email address
- `telephone`: VARCHAR(20), User's phone number
- `sign_up_date`: DATE, Date the user signed up
- `last_login`: DATE, Date of the user's last login
- `usage_stats`: TEXT, Summary of the user's usage statistics
- `subscription_tier`: VARCHAR(20), The user's subscription tier (e.g., Free, Basic, Pro, Enterprise)
- `preferences`: TEXT, User preferences
- `activity_log`: TEXT, Summary of the user's activity log

## Comments Within Code

Comments have been added to the code to clarify complex logic or processes. Here's an example snippet:

```python
def create_table(self, cursor, platform_name):
    """
    Creates a table for the specified AI platform in the database if not exists.

    Parameters:
        cursor (pymysql.cursors.Cursor): Database cursor object.
        platform_name (str): Name of the AI platform.
    """
    # Define the SQL command for creating a table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {platform_name.lower().replace(' ', '_')} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(10),
            name VARCHAR(100),
            email VARCHAR(100),
            telephone VARCHAR(20),
            sign_up_date DATE,
            last_login DATE,
            usage_stats TEXT,
            subscription_tier VARCHAR(20),
            preferences TEXT,
            activity_log TEXT
        )
    ''')
