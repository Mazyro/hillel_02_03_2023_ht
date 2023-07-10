from django.views.generic import TemplateView
from currencies.models import CurrencyHistory


class HeaderView(TemplateView):
    template_name = 'parts/header.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency_rates'] = CurrencyHistory.objects.all()
        return context
