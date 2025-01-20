import smtplib
from pydantic import EmailStr
from app.tasks.celery_app import celery_app
from PIL import Image
from pathlib import Path

from app.tasks.email_templates import create_booking_confirmation_template
from app.config import settings


@celery_app.task
def process_pic(
    path: str
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resize_large = im.resize((1000, 500))
    im_resize_large.save(f'app/static/images/resized_1000_500_{im_path.name}')
    
    im_resize_small = im.resize((200, 100))
    im_resize_small.save(f'app/static/images/resized_200_100_{im_path.name}')
    
@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    
    email_to_mock = settings.SMTP_USER
    msg_conteng = create_booking_confirmation_template(booking, email_to_mock)
    
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_conteng)