from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Product


def index(request):
    return HttpResponse("Hello, world. You're at the Enigma-ecommerce index.")


class ProductListView(ListView):
    model = Product
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('sort_by'):
            queryset = queryset.order_by(self.request.GET.get('sort_by'))
        return queryset


class ProductDetailView(DetailView):
    model = Product