"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.urls import urlpatterns as products_urlpatterns
from orders.urls import urlpatterns as orders_urlpatterns
from feedbacks.urls import urlpatterns as feedbacks_urlpatterns
from accounts.urls import urlpatterns as accounts_urlpatterns
from main.urls import urlpatterns as main_urlpatterns
from django.conf import settings
from favourites.urls import urlpatterns as favourites_urlpatterns
# from currencies.urls import urlpatterns as currencies_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include(products_urlpatterns)),
    path('orders/', include(orders_urlpatterns)),
    path('feedbacks/', include(feedbacks_urlpatterns)),
    path('accounts/', include(accounts_urlpatterns)),
    path('', include(main_urlpatterns)),
    path('favourites/', include(favourites_urlpatterns)),
    path('favourites/', include(favourites_urlpatterns)),
    # path('currencies/', include(currencies_urlpatterns)),
    path('set-language/', set_language, name='set_language'),
]

urlpatterns = i18n_patterns(*urlpatterns)


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
