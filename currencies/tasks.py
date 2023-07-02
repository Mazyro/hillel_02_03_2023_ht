from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from currencies.clients.monobank import monobank_client
from currencies.clients.nbu import nationbank_client
from currencies.clients.privatbank import privatbank_client
from currencies.models import CurrencyHistory
from project.celery import app


@app.task
def delete_old_currencies():
    CurrencyHistory.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=30)
    ).delete()


@shared_task
def get_currencies_task():
    monobank_client.prepare_data()
    nationbank_client.prepare_data()
    privatbank_client.prepare_data()


@shared_task
def set_currencies_task():
    delete_old_currencies.delay()
    # conditions ifs res excists
    res = []
    history = []

    if monobank_client.results:
        res = monobank_client.results
    elif nationbank_client.results:
        res = nationbank_client.results
    elif privatbank_client.results:
        res = privatbank_client.results
    for i in res:
        history.append(CurrencyHistory(**i))
    if history:
        CurrencyHistory.objects.bulk_create(history)
