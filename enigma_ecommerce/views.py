from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, query
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from enigma_recruitment_task.settings import EMAIL_HOST_USER

from .forms import OrderForm, OrderItemListForm, ProductForm
from .models import Order, OrderItem, Product
from .task import send_email


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
@method_decorator(
    user_passes_test(
        lambda user: user.groups.filter(name="Sellers").exists(), login_url='login'
    ),
    name='dispatch',
)
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
@method_decorator(
    user_passes_test(
        lambda user: user.groups.filter(name="Sellers").exists(), login_url='login'
    ),
    name='dispatch',
)
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
@method_decorator(
    user_passes_test(
        lambda user: user.groups.filter(name="Sellers").exists(), login_url='login'
    ),
    name='dispatch',
)
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'generic_delete.html'
    success_url = reverse_lazy('enigma_ecommerce:product-list')


@method_decorator(login_required, name="dispatch")
@method_decorator(
    user_passes_test(
        lambda user: user.groups.filter(name="Customers").exists(), login_url='login'
    ),
    name='dispatch',
)
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'generic_update.html'
    success_url = reverse_lazy('enigma_ecommerce:product-list')

    def form_valid(self, form):
        super().form_valid(form)

        product_names = [item.product.name for item in self.object.orderitem_set.all()]
        send_email.delay(
            f"Order {self.object.pk}",
            f"Thank you for ordering {', '.join(product_names)}.\nTotal Price: {self.object.total_price}",
            EMAIL_HOST_USER,
            self.object.customer.email,
        )
        return JsonResponse(
            {
                "total_price": self.object.total_price,
                "payment_due_date": self.object.payment_due_date,
            }
        )

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer'] = self.request.user
        return kwargs


@method_decorator(login_required, name="dispatch")
@method_decorator(
    user_passes_test(
        lambda user: user.groups.filter(name="Sellers").exists(), login_url='login'
    ),
    name='dispatch',
)
class OrderItemListView(ListView):
    model = OrderItem
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = OrderItemListForm(self.request.GET)
        product_limit = 15

        if form.is_valid():
            queryset = self.get_queryset_from_time_period(queryset=queryset, form=form)
            product_limit = form.cleaned_data.get('product_limit', product_limit)

        queryset = (
            queryset.values('product__name')
            .annotate(
                num_orders=Count('order', distinct=True), total_quantity=Sum('quantity')
            )
            .order_by('-num_orders')
        )
        queryset = queryset[:product_limit]

        return super().get_context_data(form=form, object_list=queryset, **kwargs)

    @staticmethod
    def get_queryset_from_time_period(
        queryset: query.QuerySet, form: OrderItemListForm
    ) -> query.QuerySet:
        if form.is_valid():
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')

            if from_date and to_date:
                queryset = queryset.filter(
                    order__order_date__range=[from_date, to_date]
                )
        return queryset
