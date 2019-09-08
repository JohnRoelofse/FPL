from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import sqlalchemy

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite', engine=sqlalchemy.create_engine('sqlite:///jobs.sqlite'))
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

def bingo():
    print('Bingo! It\'s working!')

scheduler.add_job(bingo, 'interval', minutes=1)
scheduler.start()