from django.core.cache import cache

from django.views.generic import ListView
from currencies.models import CurrencyHistory
from project.model_choices import CurrencyCacheKeys


class CurrencyView(ListView):
    model = CurrencyHistory
    template_name = 'parts/curr.html'
    context_object_name = 'currency_rates'

    def get_queryset(self):
        queryset = cache.get(CurrencyCacheKeys.CURRENCIES)
        if not queryset:
            print('TO CACHE')
            queryset = CurrencyHistory.objects.all()
            cache.set(CurrencyCacheKeys.CURRENCIES, queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset
