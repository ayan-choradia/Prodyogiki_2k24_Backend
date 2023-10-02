# tasks.py

from celery import shared_task


# @shared_task
# def test_celery_connection():
#     print("Celery connection successful!")


@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"
