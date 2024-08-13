import random
import csv
import pymysql.cursors  # Importing the MySQL connector
from faker import Faker

print('Generating data...\nPlease wait a moment...')


class DataPipeline:
    def __init__(self, dbname, user, password, host):
        """
        Initializes DataPipeline object with database credentials.

        Parameters:
            dbname (str): Name of the database.
            user (str): Username for database authentication.
            password (str): Password for database authentication.
            host (str): Hostname where the database is hosted.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def create_connection(self):
        """
        Creates a connection to the MySQL database.

        Returns:
            pymysql.connections.Connection: Connection object.
        """
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.dbname,
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_table(self, cursor, platform_name):
        """
        Creates a table for the specified AI platform in the database if not exists.

        Parameters:
            cursor (pymysql.cursors.Cursor): Database cursor object.
            platform_name (str): Name of the AI platform.
        """
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {platform_name.lower().replace(' ', '_')} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(10),
                name VARCHAR(100),
                email VARCHAR(100),
                
                sign_up_date DATE,
                last_login DATE,
                usage_stats TEXT,
                subscription_tier VARCHAR(20),
                preferences TEXT,
                activity_log TEXT
            )
        ''')

    def ingest_data(self, cursor, platform_name, records):
        """
        Ingests data into the table for the specified AI platform.

        Parameters:
            cursor (pymysql.cursors.Cursor): Database cursor object.
            platform_name (str): Name of the AI platform.
            records (list): List of dictionaries containing user records for the platform.
        """
        for record in records:
            cursor.execute(f'''
                INSERT INTO {platform_name.lower().replace(' ', '_')} 
                    (user_id, name, email, sign_up_date, last_login, usage_stats, subscription_tier, preferences, activity_log)
                VALUES 
                    (%(user_id)s, %(name)s, %(email)s, %(sign_up_date)s, %(last_login)s, %(usage_stats)s, %(subscription_tier)s, %(preferences)s, %(activity_log)s)
            ''', record)

    def run_pipeline(self, platform_data):
        """
        Runs the data pipeline to create tables, ingest data, and save to CSV files.

        Parameters:
            platform_data (dict): Dictionary containing platform names as keys and their respective records as values.
        """
        conn = self.create_connection()
        cursor = conn.cursor()

        try:
            for platform_name, records in platform_data.items():
                self.create_table(cursor, platform_name)
                self.ingest_data(cursor, platform_name, records)
            conn.commit()
            print("Data ingestion successful.")
        except Exception as e:
            conn.rollback()
            print(f"Error during data ingestion: {str(e)}")
        finally:
            cursor.close()
            conn.close()


def generate_platform_records(platform_name, num_records):
    """
    Generates fake user records for a single AI platform using Faker library.

    Parameters:
        platform_name (str): Name of the AI platform.
        num_records (int): Number of records to generate.

    Returns:
        list: List of dictionaries containing user records.
    """
    fake = Faker()
    platform_records = []
    for _ in range(num_records):
        user_id = f"{platform_name[:3].upper()}{fake.random_number(digits=6)}"
        name = fake.name()
        email = fake.email()
        
        sign_up_date = fake.date_this_decade()
        last_login = fake.date_this_year()
        usage_stats = fake.text(max_nb_chars=200)
        subscription_tier = random.choice(['Free', 'Basic', 'Pro', 'Enterprise'])
        preferences = fake.text(max_nb_chars=100)
        activity_log = fake.text(max_nb_chars=200)

        platform_records.append({
            'user_id': user_id,
            'name': name,
            'email': email,
            
            'sign_up_date': sign_up_date,
            'last_login': last_login,
            'usage_stats': usage_stats,
            'subscription_tier': subscription_tier,
            'preferences': preferences,
            'activity_log': activity_log
        })

    return platform_records


if __name__ == "__main__":
    # Provide database credentials
    dbname = "data_pipeline_ai_platforms"
    user = "root"
    password = "****"
    host = "127.0.0.1"

    # Specify platform names and the number of records per platform
    platform_names = [
        "AI Innovate",
        "Cortex Analytics",
        "Neuronix",
        "SynthMind",
        "DeepVision",
        "QuantumLeap",
        "MindSphere",
        "DataBot",
        "InsightAI",
        "RoboGen"
    ]
    num_records_per_platform = 1000

    # Generate data for all platforms
    platform_data = {}
    for platform_name in platform_names:
        platform_data[platform_name] = generate_platform_records(platform_name, num_records_per_platform)

    # Initialize pipeline and run
    pipeline = DataPipeline(dbname, user, password, host)
    pipeline.run_pipeline(platform_data)
