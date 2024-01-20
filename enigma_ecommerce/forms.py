from django import forms
from .models import Product, Order, OrderItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image']


class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all()
    )
    quantity = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ['delivery_address']

    def save(self, commit=True):
        order = super().save(commit=False)

        if self.customer:
            order.customer = self.customer

        if commit:
            order.save()

            product = self.cleaned_data['product']
            quantity = self.cleaned_data['quantity']

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            order_item.save()

        order.save()
        return order
