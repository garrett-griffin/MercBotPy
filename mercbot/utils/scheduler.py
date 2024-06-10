from apscheduler.schedulers.asyncio import AsyncIOScheduler
from mercbot.main import main

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'interval', hours=1)  # Adjust the interval as needed
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
