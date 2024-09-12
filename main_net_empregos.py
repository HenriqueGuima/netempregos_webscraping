import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape a single page
def scrape_page(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all job offer divs
    job_table = soup.find_all('div', class_='job-item')
    
    # Initialize a list to store job details
    jobs = []
    
    # Loop through each job offer and extract details
    for job in job_table:
        title = job.find('h2').get_text(strip=True)  # Extract the job title
        
        # Extract the company name from the bold <li>
        company = job.find('li', style='font-weight:bold').get_text(strip=True) if job.find('li', style='font-weight:bold') else 'N/A'
        
        # Extract the location using the flaticon-pin icon, with error handling
        location_tag = job.find('i', class_='flaticon-pin')
        if location_tag:
            location = location_tag.find_next_sibling(text=True).strip()
        else:
            location = 'N/A'  # Fallback if location is not found
        
        # Extract the date posted using the flaticon-calendar icon, with error handling
        date_tag = job.find('i', class_='flaticon-calendar')
        if date_tag:
            date_posted = date_tag.find_next_sibling(text=True).strip()
        else:
            date_posted = 'N/A'  # Fallback if date is not found
        
        # Extract the category (Serviços Técnicos) using the fa-tags icon, with error handling
        category_tag = job.find('i', class_='fa fa-tags')
        if category_tag:
            category = category_tag.find_next_sibling(text=True).strip()
        else:
            category = 'N/A'  # Fallback if category is not found
        
        # Add job info to the list
        jobs.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Date Posted': date_posted,
            'Category': category
        })
    
    # Return the list of job offers
    return jobs

# Function to scrape all pages until no more job offers
def scrape_all_pages(base_url):
    all_jobs = []
    page = 1
    
    while True:
        # Construct the URL for the current page
        url = f"{base_url}&page={page}"
        print(f"Scraping page {page}...")
        
        # Scrape the current page
        jobs = scrape_page(url)
        
        # If no jobs are found on the page, stop the loop
        if not jobs:
            print(f"No jobs found on page {page}. Stopping.")
            break
        
        # Otherwise, add the jobs to the list
        all_jobs.extend(jobs)
        
        # Move to the next page
        page += 1
    
    return all_jobs

# Base URL for the job search
base_url = "https://www.net-empregos.com/pesquisa-empregos.asp?categoria=0&zona=0&tipo=0"

# Scrape all job offers from all pages dynamically until no more jobs are found
all_jobs = scrape_all_pages(base_url)

# Convert the list of jobs into a Pandas DataFrame
df = pd.DataFrame(all_jobs)

# Display the DataFrame
print(df)

# Optionally, save to CSV file
df.to_csv('job_offers_net_empregos.csv', index=False)
