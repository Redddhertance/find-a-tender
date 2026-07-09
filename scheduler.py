from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from main import run_pipeline

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, 'interval', hours = 3)
    print('System active')
try:
    scheduler.start()
except(KeyboardInterrupt, SystemExit):
    print('System stopped')