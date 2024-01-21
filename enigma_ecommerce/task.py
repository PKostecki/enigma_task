from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from enigma_recruitment_task.settings import EMAIL_HOST_USER

from .models import Order


@shared_task(serializer='json', name="send_mail")
def send_email(subject, message, sender, receiver):
    send_mail(subject, message, sender, [receiver])


@shared_task(serializer='json', name="send_payment_reminder_email")
def send_payment_reminder_email():
    today = timezone.now().date()

    orders_to_remind = Order.objects.filter(
        payment_due_date__lte=today + timedelta(days=5)
    )

    for order in orders_to_remind:
        customer_email = order.customer.email
        customer_username = order.customer.username

        subject = f"Payment reminder - Order {order.pk}"
        message = f"Hello {customer_username},\n\n"
        message += (
            f"This is a reminder to your order:  {order.pk}. Please make a payment.\n\n"
        )
        message += "Greetings"

        send_mail(subject, message, EMAIL_HOST_USER, [customer_email])
