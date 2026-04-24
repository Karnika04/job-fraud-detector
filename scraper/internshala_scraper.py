import os
from typing import List

import requests
from bs4 import BeautifulSoup


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def fetch_sample_internshala_jobs() -> List[dict]:
    """
    Fetch sample internships from a public Internshala-like HTML page.

    This is a simplified demonstration scraper; in practice, respect
    robots.txt and terms of service.
    """

    url = "https://www.example.com/internships"  # Placeholder URL
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    jobs: List[dict] = []

    for job_el in soup.select(".internship-card")[:10]:
        title = job_el.select_one(".internship-title").get_text(strip=True) if job_el.select_one(".internship-title") else ""
        desc = job_el.select_one(".internship-description").get_text(strip=True) if job_el.select_one(".internship-description") else ""

        if not title and not desc:
            continue

        jobs.append(
            {
                "title": title,
                "description": desc,
                "company_profile": "",
                "requirements": "",
            }
        )

    return jobs


def send_to_backend(jobs: List[dict]) -> None:
    """Send scraped jobs to backend /predict endpoint."""

    for job in jobs:
        try:
            resp = requests.post(f"{BACKEND_URL}/predict", json=job, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            print(f"Title: {job['title']!r} => {data['prediction']} ({data['fraud_probability']:.2f})")
        except Exception as exc:
            print(f"Failed to process job {job.get('title')}: {exc}")


if __name__ == "__main__":
    scraped_jobs = fetch_sample_internshala_jobs()
    send_to_backend(scraped_jobs)

