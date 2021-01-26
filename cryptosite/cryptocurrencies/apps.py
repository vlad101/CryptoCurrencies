from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import atexit

class CryptocurrenciesConfig(AppConfig):
    name = 'cryptocurrencies'

    """
    Kick off updater on startup
    """
    def ready(self):
        from .taskscheduler import pusher_task
        pusher_util = pusher_task.PusherUtil()
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=pusher_util.retrieve_data,
            trigger=IntervalTrigger(seconds=10),
            id='prices_retrieval_job',
            name='Retrieve prices every 10 seconds',
            replace_existing=True)
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())