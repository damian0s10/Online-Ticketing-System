import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tickets.settings')

app = Celery('tickets')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))