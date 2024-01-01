# web_data_extraction
This repository presents a method for crawling and scraping a generic website URL.  
The approach employed utilizes the [Scrapy](https://scrapy.org) framework to develop an efficient crawler, along with the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library for basic scraping and formatting of the gathered information.  
The repository is intended solely for demonstration purposes, and I hereby disclaim any responsibility for how the contents might be used.   
<ins> Users are responsible for ensuring their usage aligns with the Terms of Service and policies of the websites they crawl. </ins>

## Current features
- [✅] **extract_from_url API**:
    - This API enables text extraction from a list of any website URL, utilizing the [trafilatura](https://trafilatura.readthedocs.io/en/latest/usage-python.html) library for text content extraction.
    - It offers the ability to recursively navigate within a webpage, staying within the same domain. Users can specify this using the max_next_pages parameter (where 0 denotes only the current URL, and a higher number allows navigation through multiple pages).
    <img width="1000" alt="web_extraction_1" src="https://github.com/sarapiscitelli/web-data-extraction/assets/104431794/42e3b340-416e-440e-84a5-ee9322a9a0de">

- [✅] **extract_from_trustpilot_url API**:
  - This feature focuses on extracting formatted content from a specific organization's page on [trustpilot](https://www.trustpilot.com)
  - It also includes functionality to navigate through subsequent pages to gather all reviews, controlled by the max_next_pages parameter.
  <img width="947" alt="web_extraction_2" src="https://github.com/sarapiscitelli/web-data-extraction/assets/104431794/2b9bea45-adca-411f-98d4-171db27f3252">


## How to Run  
For running the application, [Docker](https://docs.docker.com/get-docker/) is the recommended platform. Ensure you have Docker ([refer to the installation guide](https://docs.docker.com/compose/install/)) and docker-compose installed ([refer to the installation guide](https://docs.docker.com/compose/install/)) on your machine. 

1. Initial setup   
   1.1 Clone the repository to your local machine
    ```
    git clone https://github.com/sarapiscitelli/web-data-extraction.git
    cd web-data-extraction
    ```
   
   1.2 Ensure your Docker daemon and Docker Compose are running on your local machine
   ```
   docker --version                                           
   docker-compose --version
   ```
   You should see output similar to the following:  
   ```console
   Docker version 24.0.5, build ced0996
   Docker Compose version v2.20.2-desktop.1
   ```   
   1.3 Configure the .env file with the required variables:   
   ```
   # scraper backend configurations
   SCRAPER_BACKEND_PORT=8081
   SCRAPER_BACKEND_HOST=0.0.0.0
   SCRAPER_API_V1_STR=/api/v1
   ```

3. Starting the Application  
    Execute the following commands to initiate the application:

    ```
    ./start.sh build
    ./start.sh run
    ```

4. Accessing API Documentation   
    Visit http://localhost:8081/docs (adjust the url and port based on your environment settings) to view the API documentation.
