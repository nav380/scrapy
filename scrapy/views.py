from django.http import JsonResponse
from .scrapy import run_scraper  # Import the function from scraper.py

def scrape_articles(request):
    results = run_scraper()
    return JsonResponse({"count": len(results), "data": results}, safe=False)
