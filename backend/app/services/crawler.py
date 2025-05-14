from playwright.sync_api import sync_playwright

# def extract_backlinks(url: str, target_domain: str):
#     results = []
#     source_url = url.strip()

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
#         page = browser.new_page()
#         page.goto(source_url, timeout=60000)
#         title = page.title()
#         anchors = page.query_selector_all("a")

#         for a in anchors:
#             href = a.get_attribute("href")
#             rel = a.get_attribute("rel")

#             if href and target_domain in href:
#                 results.append({
#                     "source_url": source_url,
#                     "target_url": href.strip() if href else "",
#                     "title": title.strip() if title else "",
#                     "rel": rel.strip() if rel else "none"
#                 })

#         browser.close()

#     return results

# def extract_backlinks(url: str, target_domain: str):
#     results = []
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
#         page = browser.new_page()
#         page.goto(url, timeout=60000)
#         anchors = page.query_selector_all("a")

#         for a in anchors:
#             href = a.get_attribute("href")
#             rel = a.get_attribute("rel")

#             if href and target_domain in href:
#                 target_title = ""
#                 try:
#                     # Open the href in a new tab to get the target title
#                     new_page = browser.new_page()
#                     new_page.goto(href, timeout=15000)
#                     target_title = new_page.title()
#                     new_page.close()
#                 except Exception as e:
#                     print(f"⚠️ Failed to load target {href}: {e}")
#                     target_title = "Failed to fetch"

#                 results.append({
#                     "source_url": url,
#                     "target_url": href.strip(),
#                     "title": target_title.strip(),
#                     "rel": rel.strip() if rel else "none"
#                 })

#         browser.close()
#     return results

from playwright.sync_api import sync_playwright

def extract_backlinks(url: str, target_domain: str):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="networkidle")  # Ensure JS is loaded

        anchors = page.query_selector_all("a")

        for a in anchors:
            href = a.get_attribute("href")

            if href and target_domain in href:
                rel = a.evaluate("node => node.getAttribute('rel')")  # More reliable than get_attribute()
                target_title = "Failed to fetch"
                try:
                    new_page = browser.new_page()
                    new_page.goto(href, timeout=15000)
                    target_title = new_page.title()
                    new_page.close()
                except Exception as e:
                    print(f"⚠️ Failed to load target {href}: {e}")

                results.append({
                    "source_url": url,
                    "target_url": href.strip(),
                    "title": target_title.strip(),
                    "rel": rel.strip() if rel else "none"
                })

        browser.close()
    return results


# from app.core.celery_app import celery
# from app.services.crawler import extract_backlinks
# from app.db.session import SessionLocal
# from app.models.job import Job, JobStatus
# # from app.models.backlink import Backlink

# import logging

# logger = logging.getLogger(__name__)

# BATCH_SIZE = 100

# def commit_backlinks_in_batches(db, backlinks, batch_size=BATCH_SIZE):
#     for i in range(0, len(backlinks), batch_size):
#         batch = backlinks[i:i + batch_size]
#         try:
#             db.bulk_save_objects(batch)
#             db.commit()
#             logger.info(f"✅ Successfully inserted batch {i // batch_size + 1}")
#         except Exception as e:
#             logger.error(f"❌ Error inserting batch {i // batch_size + 1}: {e}")
#             db.rollback()
#             raise  # Re-raise to handle in outer try-except

# @celery.task(name="crawl_backlinks")
# def crawl_backlinks_task(job_id: int, url: str, target_domain: str):
#     db = SessionLocal()
#     try:
#         job = db.query(Job).get(job_id)
#         if not job:
#             logger.error(f"❌ Job with ID {job_id} not found.")
#             return

#         job.status = JobStatus.in_progress
#         db.commit()
#         logger.info(f"🚀 Job {job_id} started for URL: {url}")

#         results = extract_backlinks(url, target_domain)

#         backlinks = [Backlink(job_id=job.id, **r) for r in results]
#         logger.info(f"🔗 {len(backlinks)} backlinks extracted for Job {job_id}")

#         try:
#             commit_backlinks_in_batches(db, backlinks)
#         except Exception as e:
#             job.status = JobStatus.failed
#             db.commit()
#             logger.error(f"❌ Failed to save backlinks for Job {job_id}: {e}")
#             return

#         job.status = JobStatus.completed
#         logger.info(f"✅ Job {job_id} completed successfully.")

#     except Exception as e:
#         logger.exception(f"❌ Unexpected error in Job {job_id}: {e}")
#         if 'job' in locals() and job:
#             job.status = JobStatus.failed
#             db.commit()

#     finally:
#         db.close()
