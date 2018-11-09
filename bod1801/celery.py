from celery import Celery

import bod1801.celeryconfig

app = Celery('bod1801')
app.config_from_object(bod1801.celeryconfig)
