# from celery import shared_task
# from datetime import datetime
# from app.db.session import SessionLocal
# from app.models.job import Job
# from app.tasks.backlink_task import crawl_backlinks_task

# # @shared_task
# # def check_and_schedule_jobs():
#     # now = datetime.now()
#     # current_time = now.time()
#     # today = now.date()
#     # weekday = now.weekday()  # 0 = Monday

#     # db = SessionLocal()
#     # try:
#     #     jobs = db.query(Job).filter(Job.schedule.isnot(None), Job.run_at.isnot(None)).all()

#     #     for job in jobs:
#     #         if job.status == 'cancelled':
#     #             continue

#     #         if job.run_at.hour == current_time.hour and job.run_at.minute == current_time.minute:
#     #             if job.schedule == 'daily':
#     #                 crawl_backlinks_task.delay(job.id)

#     #             elif job.schedule == 'weekly' and weekday == 0:  # Every Monday
#     #                 crawl_backlinks_task.delay(job.id)

#     #             elif job.schedule == 'monthly' and today.day == 1:  # 1st of each month
#     #                 crawl_backlinks_task.delay(job.id)

#     # except Exception as e:
#     #     print(f"❌ Error in scheduler task: {e}")
#     # finally:
#     #     db.close()

# @shared_task(name="app.tasks.scheduler.check_and_schedule_jobs")
# def check_and_schedule_jobs():
#     from datetime import datetime
#     now = datetime.now()
#     current_time = now.time()
#     db = SessionLocal()
#     print(f"⏰ Scheduler running at {now.strftime('%H:%M:%S')}")

#     try:
#         jobs = db.query(Job).filter(Job.schedule.isnot(None), Job.run_at.isnot(None)).all()
#         for job in jobs:
#             print(f"📝 Evaluating Job {job.id}: status={job.status}, run_at={job.run_at}")

#             if job.status in ['completed', 'cancelled']:
#                 continue

#             scheduled_time = datetime.combine(now.date(), job.run_at)
#             time_diff = abs((now - scheduled_time).total_seconds())

#             if time_diff <= 60:
#                 print(f"✅ Job {job.id} is due! Triggering now.")
#                 from app.tasks.backlink_task import crawl_backlinks_task
#                 crawl_backlinks_task.delay(job.id, job.url, job.target_domain)
#             else:
#                 print(f"⏸️ Job {job.id} not due yet (Δ={time_diff:.1f}s)")
#     except Exception as e:
#         print(f"❌ Error in scheduler: {e}")
#     finally:
#         db.close()


from celery import shared_task
from datetime import datetime
from app.db.session import SessionLocal
from app.models.job import Job
from app.tasks.backlink_task import crawl_backlinks_task

@shared_task(name="app.tasks.scheduler.check_and_schedule_jobs")
def check_and_schedule_jobs():
    now = datetime.now()  # Now uses container's timezone
    db = SessionLocal()
    print(f"⏰ Scheduler running at {now.strftime('%H:%M:%S')}")

    try:
        jobs = db.query(Job).filter(Job.schedule.isnot(None), Job.run_at.isnot(None)).all()
        for job in jobs:
            print(f"📝 Job {job.id} | Status: {job.status} | Scheduled at: {job.run_at} | Now: {now.time().strftime('%H:%M:%S')}")

            if job.status in ['completed', 'cancelled']:
                continue

            scheduled_time = datetime.combine(now.date(), job.run_at)

            if now >= scheduled_time and job.status == 'queued':
                print(f"✅ Triggering job {job.id}!")
                crawl_backlinks_task.delay(job.id, job.url, job.target_domain)
            else:
                time_diff = (scheduled_time - now).total_seconds()
                print(f"⏸️ Not time yet (Δ = {int(time_diff)}s) for Job {job.id}")
    except Exception as e:
        print(f"❌ Error in scheduler: {e}")
    finally:
        db.close()
