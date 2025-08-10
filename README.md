Django + Scrapy Web Scraper
A Django-based web scraping application integrated with Scrapy for extracting, processing, and storing structured data.
This project is designed to run Scrapy spiders within a Django environment, allowing seamless data storage in Django models and enabling further processing, visualization, or API exposure.

✨ Features
Django + Scrapy Integration – Easily run Scrapy spiders from Django management commands.

Customizable Spiders – Scrape data from any website by adjusting selectors.

Django ORM Support – Store scraped data directly into Django models.

Extensible – Add pipelines, middlewares, and processing logic for your needs.

Command-line Friendly – Run spiders via python manage.py crawl <spider_name>.

📦 Installation
bash
Copy
Edit
# Clone the repository
git clone https://github.com/nav380/scrapy.git
cd scrapy

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate
🚀 Usage
Run a spider directly from Django:

bash
Copy
Edit
python manage.py crawl example
📂 Project Structure
bash
Copy
Edit
project_name/
│── project_name/         # Django project settings
│── scraper/              # Scrapy spiders & pipelines
│── manage.py             # Django entry point
│── requirements.txt      # Dependencies
🛠 Technologies Used
Python 3.x

Django

Scrapy