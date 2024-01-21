from django import forms

from .models import Order, OrderItem, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image']


class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
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
                order=order, product=product, quantity=quantity
            )
            order_item.save()

        order.save()
        return order


class OrderItemListForm(forms.ModelForm):
    from_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    to_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    product_limit = forms.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = ('from_date', 'to_date', 'product_limit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
