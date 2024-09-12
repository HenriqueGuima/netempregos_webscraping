import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_table = soup.find_all('div', class_='job-item')
    jobs = []
    
    for job in job_table:
        title = job.find('h2').get_text(strip=True)  
        
        company = job.find('li', style='font-weight:bold').get_text(strip=True) if job.find('li', style='font-weight:bold') else 'N/A'
        
        location_tag = job.find('i', class_='flaticon-pin')
        if location_tag:
            location = location_tag.find_next_sibling(text=True).strip()
        else:
            location = 'N/A'  
        
        date_tag = job.find('i', class_='flaticon-calendar')
        if date_tag:
            date_posted = date_tag.find_next_sibling(text=True).strip()
        else:
            date_posted = 'N/A' 
        
        category_tag = job.find('i', class_='fa fa-tags')
        if category_tag:
            category = category_tag.find_next_sibling(text=True).strip()
        else:
            category = 'N/A'  
        
        jobs.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Date Posted': date_posted,
            'Category': category
        })
    
    return jobs

def scrape_all_pages(base_url):
    all_jobs = []
    page = 1
    
    while True:
        url = f"{base_url}&page={page}"
        print(f"Scraping page {page}...")
        
        jobs = scrape_page(url)
        
        if not jobs:
            print(f"No jobs found on page {page}. Stopping.")
            break
        
        all_jobs.extend(jobs)
        
        page += 1
    
    return all_jobs

base_url = "https://www.net-empregos.com/pesquisa-empregos.asp?categoria=0&zona=0&tipo=0"

all_jobs = scrape_all_pages(base_url)

df = pd.DataFrame(all_jobs)

print(df)

df.to_csv('job_offers_net_empregos.csv', index=False)
