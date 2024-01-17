
import concurrent.futures
import csv
from dateutil import relativedelta
import time
from datetime import date, datetime, timedelta
from urllib3 import Retry
from googleads.errors import GoogleAdsException
from googleads import oauth2
import logging

CSV_FILE = 'report.csv' 

# Set up logger
logger = logging.getLogger('google_ads')  
logger.setLevel(logging.DEBUG)

# File handler  
fh = logging.FileHandler('errors.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def handle_error(date, error):
    logger.error(f"Error fetching {date}: {error}")

with open(CSV_FILE, 'w') as f:
    writer = csv.writer(f)     
    writer.writerow(['date', 'impressions', 'clicks'])

# Helper function to convert date to string
def date_to_str(date):
    return date.strftime("%Y-%m-%d")  

@Retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def fetch_data(date):
    try:
        # Make google ads API call
        pass
    except Exception as e:  
        handle_error(date, e)
  

def refresh_oauth_token():

    # OAuth2 configuration object
    oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN 
    )

    try:
        # Refresh authorization
        oauth2_client.RefreshAccessToken()

    except oauth2.errors.GoogleAdsException as ex:
        handle_error(date, ex)

    else:
        print("Successfully refreshed OAuth token!")
        # Updated access token available 
        # oauth2_client.access_token

# Function to save data to CSV  
def save_to_csv(data):
    with open('report.csv', 'a') as f:
        writer = csv.writer(f) 
        writer.writerow((data['date'], data['impressions'], data['clicks']))

# Function for error handling      
def handle_error(date, error):
    print(f"Error fetching data for {date_to_str(date)}: {error}")  
    # Log error  

# Parallel processing using ThreadPoolExecutor  
def fetch_parallel(start_date, end_date):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, date)  
                   for date in get_dates(start_date, end_date)]
            
        for future in concurrent.futures.as_completed(futures):
            date = future.args[0] # Get date  
            try:
                data = future.result()
            except Exception as e:  
                handle_error(date, e)
            else:
                save_to_csv(data)

# Get list of dates between start and end          
def get_dates(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += datetime.timedelta(days=1)  
    return dates

# Calculate last 2 years date range   
def get_last_two_years(): 
    today = datetime.date.today()
    past = today + relativedelta.relativedelta(years=-2) 
    start_date = past 
    end_date = today
    return start_date, end_date  

def get_max_date_from_csv():
    dates = []
    with open(CSV_FILE) as f:
        reader = csv.reader(f)
        next(reader) # Skip header  
        for row in reader:
            dates.append(row[0]) 
    return max(dates)

def get_missing_dates(start_date, end_date):
    with open(CSV_FILE) as f: 
       reader = csv.reader(f)
       existing_dates = [row[0] for row in reader]  
    missing = []
    for d in get_dates(start_date, end_date):
        if d not in existing_dates:
            missing.append(d)
    return missing

def daily_update():
   
    latest_date = get_max_date_from_csv()
    start_date = latest_date + timedelta(days=1)  
    end_date = datetime.now().date()
  
    missing_dates = get_missing_dates(start_date, end_date)

    if missing_dates:
        start_date = missing_dates[0]
        end_date = missing_dates[-1]  
        fetch_parallel(start_date, end_date) 

if __name__ == "__main__":
  
    # Get inputs   
    start_date = datetime.date(2023, 1, 1)  
    end_date = datetime.date(2023, 1, 5)
  
    print("Fetching data...")
  
    start = time.time()
    fetch_parallel(start_date, end_date)  
    end = time.time()

    print(f"Data fetched in {end-start:.2f} seconds")

    # Backfill historical data
    print("Backfilling historical data...")
    start_date, end_date = get_last_two_years() 
    fetch_parallel(start_date, end_date)

    daily_update()
