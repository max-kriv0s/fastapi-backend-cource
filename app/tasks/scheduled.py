import asyncio
from app.tasks.celery_app import celery_app

# celery beat
@celery_app.task(name="email.booking_reminder_1day")
def remind_booking_1day():
    asyncio.run(remind_of_booking(1))


@celery_app.task(name="email.booking_reminder_3days")
def remind_booking_3days():
    asyncio.run(remind_of_booking(3))


async def get_data():
    await asyncio.sleep(5)


@celery_app.task(name='periodic_task')
def periodic_task():
    """Пример запуска асинхронной функции внутри celery таски"""
    print(12345)
    asyncio.run(get_data())