from celery import Celery

app = Celery('bod1801',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1',
             include=['bod1801.tasks'])

# Optional configuration, see the application user guide
# app.conf.update(
#     result_expires=3600,
# )
