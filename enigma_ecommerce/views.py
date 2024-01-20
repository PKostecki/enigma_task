from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Product, Order
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ProductForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.http import JsonResponse
from django.core.mail import send_mail



def is_seller(user):
    return user.groups.filter(name="Sellers").exists()


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


@method_decorator(login_required, name="dispatch")
@method_decorator(user_passes_test(lambda user: user.groups.filter(name="Sellers").exists(), login_url='login'),
                  name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'generic_update.html'
    success_url = reverse_lazy('enigma_ecommerce:product-list')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(user_passes_test(lambda user: user.groups.filter(name="Sellers").exists(), login_url='login'),
                  name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'generic_update.html'
    success_url = reverse_lazy('enigma_ecommerce:product-list')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(user_passes_test(lambda user: user.groups.filter(name="Sellers").exists(), login_url='login'),
                  name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'generic_delete.html'
    success_url = reverse_lazy('enigma_ecommerce:product-list')


@method_decorator(login_required, name="dispatch")
@method_decorator(user_passes_test(lambda user: user.groups.filter(name="Customers").exists(), login_url='login'),
                  name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'generic_update.html'
    success_url = reverse_lazy('enigma_ecommerce:product-list')

    def form_valid(self, form):
        super().form_valid(form)

        product_names = [item.product.name for item in self.object.orderitem_set.all()]

        send_mail(
            f"Order {self.object.pk}",
            f"Thank you for ordering {', '.join(product_names)}.\nTotal Price: {self.object.total_price}",
            None,
            ["sometest_mail@gmail.com"],
            fail_silently=False,
        )
        return JsonResponse({"total_price": self.object.total_price, "payment_due_date": self.object.payment_due_date})

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer'] = self.request.user
        return kwargs