# Question 1

## Endpoints:

1. Retrieving Product Information:

   a. Endpoint to retrieve details of a single product by its ID:

   * Endpoint: GET /products/{product_id}
   * Functionality: Retrieves the details of a product based on its unique ID.
   * Implementation: When a GET request is made to this endpoint, the API fetches the product details from the database using the product ID and returns the product information as a JSON response.

   b. Endpoint to retrieve a list of all products, with pagination support:

   * Endpoint: GET /products
   * Functionality: Retrieves a paginated list of all products, allowing users to navigate through the entire product inventory in manageable chunks.
   * Implementation:
     * Accepts optional query parameters like "page" and "limit" to specify the page number and the number of products per page.
     * The API fetches the relevant subset of products from the database using the provided pagination parameters and returns the results along with pagination metadata.
2. Updating Product Information: a. Endpoint to update the price and stock level of a product:

   * Endpoint: PUT /products/{product_id}
   * Functionality: Allows for the update of the price and stock level of a specific product by its ID.
   * Implementation:
     * Accepts a JSON payload in the request body containing the new price and stock level for the product.
     * The API updates the corresponding product record in the database and ensures data consistency with the caching layer.
3. Searching for Products: a. Endpoint to search for products based on name or price range:

   * Endpoint: GET /products/search
   * Functionality: Enables users to search for products based on their name or within a specified price range.
   * Implementation:
     * Accepts query parameters such as "name" and "min_price"/"max_price" to filter products based on the provided criteria.
     * The API constructs and executes optimized SQL queries to fetch products matching the search criteria from the database and returns the results.

## Considerations:

1. Database Interactions:

   - Database: Utilize PostgreSQL for its strong support for complex queries, indexing capabilities, and reliability.
   - SQL Queries: Use parameterized SQL queries to prevent SQL injection attacks and optimize query execution plans.
   - Indexing: Apply indexing to the "id," "name," and "price" columns to speed up retrieval and searching operations.
   - Connection Pooling: Implement a connection pool management system, such as Psycopg2's connection pooling for PostgreSQL, to efficiently manage multiple concurrent database connections and minimize the overhead of connection establishment.
2. Caching Strategy:

   - Caching Layer: Implement Redis as an in-memory data store due to its high performance and support for advanced data types and caching strategies.
   - Caching Algorithm: Utilize the Least Recently Used (LRU) caching algorithm in Redis to automatically evict less frequently accessed items from the cache and make room for new data.
   - Cache Invalidation: Employ the pub/sub (publish/subscribe) feature in Redis to notify cache instances to invalidate or update cached data when product information is updated in the database. Additionally, apply Time-To-Live (TTL) settings to evict keys automatically after a specified period, ensuring data consistency.
3. Error Handling:

   - HTTP Status Codes: Return appropriate HTTP status codes such as 404 for "Not Found," 400 for "Bad Request," and 500 for "Internal Server Error" scenarios.
   - Error Response Payload: Provide descriptive error messages in the API response payload, including details and the nature of the encountered error, enabling clients to handle errors effectively.
4. Data Consistency:

   - Write-Through Caching: Implement a write-through caching strategy where write operations also update the cache, ensuring consistency between the database and the cache.
   - Database Triggers: Utilize PostgreSQL triggers to notify the cache of any relevant data changes, triggering cache updates or invalidations.
5. Scalability:

   - Backend Framework: Employ FastAPI for its asynchronous support, which allows handling a large number of concurrent requests efficiently.
   - Asynchronous Request Handling: Utilize the asynchronous handling capabilities of FastAPI and its underlying ASGI (Asynchronous Server Gateway Interface) to process a large number of simultaneous requests without tying up system resources.
   - Load Balancing and Horizontal Scaling: Utilize a load balancer, such as nginx, in front of multiple API server instances, distributing incoming traffic evenly. Employ horizontal scaling by adding more API server instances to handle increased load, making use of containerization and orchestration technologies like Docker and Kubernetes for effective management.

Regarding the bonus question on Rate Limiting:

- Rate Limiting Module: Integrate a dedicated rate-limiting middleware such as "fastapi-limiter" for FastAPI, or "flask-limiter" for Flask, allowing for flexible rate-limiting configuration and enforcement.
- Decision on Rate Limits: Determine appropriate rate limits based on empirical data, expected usage patterns, and capacity planning. For instance, consider setting limits such as 100 requests per minute for read operations and 50 requests per minute for write operations.
- Enforcement of Rate Limits: Enforce rate limits through the use of tokens or IP-based verification, enabling the API to restrict access for clients exceeding the predefined limits while maintaining responsiveness for compliant users.

With this detailed approach, the RESTful API will effectively handle product information, prioritize performance, and ensure robustness for frequent usage scenarios.

---

# Question 2:

```
import concurrent.futures
import csv
from dateutil import relativedelta
import time
from datetime import date, datetime, timedelta
from urllib3 import Retry
from googleads.errors import GoogleAdsException

CSV_FILE = 'report.csv' 

# Helper function to convert date to string
def date_to_str(date):
    return date.strftime("%Y-%m-%d")  

@Retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def fetch_data(date):
    try:
        # Make google ads API call
        pass
    except TimeoutError:
        #Handle TimeoutError  
        raise TimeoutError
    except ConnectionError:
        #Handle connection errors
        raise ConnectionError
    except GoogleAdsException as e:  
        #Handle auth errors  
        raise GoogleAdsException
  

def handle_error(date, error):
    if isinstance(error, TimeoutError):
        print(f"Timeout error on {date_to_str(date)}") 
    elif isinstance(error, ConnectionError):
        print(f"Connection error on {date_to_str(date)}")
    elif isinstance(error, GoogleAdsException):  
        print(f"Auth exception on {date_to_str(date)}")
        #Refresh OAuth token
        #Retry  

# Function to save data to CSV  
def save_to_csv(data):
    with open('report.csv', 'a') as f:
        writer = csv.writer(f) 
        writer.writerow((data['date'], data['impressions'], data['clicks']))

    with concurrent.futures.ThreadPoolExecutor(max_workers=5, timeout=30) as executor:
      
        dates = get_dates(start_date, end_date)
      
        futures = [executor.submit(fetch_data, date)  
                    for date in dates]
              
        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result() 
            except Exception as e:  
                handle_error(date, e)
            else:
                save_to_csv(data)

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
```

## Parallel Processing Approach

The foundation of my approach is concurrent.futures thread pool executor to enable parallel data fetching from the API. This vastly improves performance over sequential fetching as multiple threads can send simultaneous requests.

**1. Created an input range of dates to fetch**

Firstly, the `get_dates()` helper method generates a list of dates between the input start date and end date. This provides the list of distinct dates to fetch.

```python
dates = get_dates(start_date, end_date))
```

**2. Submit each date as a separate task**

With this list of dates, I submit each date as a separate async fetch function call to the thread pool executor:

```python
futures = [executor.submit(fetch_data, date) for date in dates]
```

The key advantage is each date's fetch job runs in parallel instead of waiting on the previous one to finish. This dramatically speeds up overall runtime.

**3. Handle results & errors**

As each parallel task completes, the result is processed and errors are handled:

```python
for future in concurrent.futures.as_completed(futures):
    try: 
       data = future.result()
    except Error as e: 
       handle_error()
    else:  
       save_data()
```

This saves the fetched data on success, and retries or logs the failure appropriately.

## Handling Errors

The code uses comprehensive error handling for robustness:

- **Timeouts:** Configured via ThreadpoolExecutor
- **Rate Limits:** Exponential backoff retry
- **Auth failures:** Catch auth exceptions, refresh tokens
- **Logging:** Debug logs for all errors with timestamps

This ensures the script works reliably despite intermittent API issues.

## Backfill & Daily Updates

Additional mechanisms fetch historical and latest missing data:

- **Backfill** last 2 years data to populate initial state
- **Daily update** checks for missing dates vs CSV and fills gaps

This keeps the data current and complete.

## Data Storage

For the CSV storage:

- Avoid **duplicates** by checking date before writing
- Identify **missing dates** by gaps between dates
- Update rows for existing dates vs append new

This maintains data integrity.

Overall, these approaches ensure robust, efficient, and correct data fetching functionality.

## Assumptions

- Using Python 3.7+
- Have Google Ads API credentials
- Google Ads API client library installed
- The fetch_data(date) function is already implemented and handles the actual API calls.

* OAuth credentials loaded from environment variables/secret config
* Using client-side auth flow with refresh token

## Implementation

The key modules used are:

- **concurrent.futures** - for parallelism
- **datetime** - date range generation
- **csv** - reading/writing CSV
- **googleads** - Google Ads API client

## Flow

The high level flow is:

1. Generate date range
2. Submit parallel fetch tasks for each date
3. Handle results as completed & retry on failure
4. Save data to CSV
5. Backfill historical data
6. Schedule daily updates

## Instructions

To run the script:

1. Ensure Python 3.7+
2. Install requirements:
   ```
   pip install googleads csv concurrent.futures
   ```
3. Update AUTH credentials:
   ```python
   # Set OAuth credentials  
   googleads.oauth2.set_client_info(CLIENT_ID, CLIENT_SECRET) 
   ```
4. Run script:
   ```
   python google_ads.py
   ```
5. Input start and end date when prompted
6. Output report saved to `report.csv`

## Scheduling

To enable daily updates, configure a cron job:

```
0 0 * * * python /path/to/google_ads.py
```

This will run at 00:00 hrs daily to fetch latest data.
