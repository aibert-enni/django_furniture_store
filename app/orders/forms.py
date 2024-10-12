import re
from django import forms

class CreateOrderForm(forms.Form):
    
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=(('0', False), ('1', True)),)
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=(('stripe', 'stripe'), ('yookassa', 'yookassa'), ('on_get', 'on_get')),)

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError('Только цифры должны быть!')
        
        pattern = re.compile(r'^\d{10}$')
        
        if not pattern.match(data):
            raise forms.ValidationError('Неверный формат номера телефона!')

        return data

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введите ваше имя',
    #         }
    #     )
    # )

    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введите вашу фамилию',
    #         }
    #     )
    # )

    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введите ваш номер телефона',
    #         }
    #     )
    # )

    # requires_delivery = forms.BooleanField(
    #     widget=forms.RadioSelect(),
    #     choises=(('0', False), ('1', True)),
    #     initial=0
    # )

    # delivery_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'delivery-address',
    #             'rows': '2',
    #             'placeholder': 'Введите адрес доставки',
    #         }
    #     ),
    #     required=False
    # )

    # payment_on_get = forms.BooleanField(
    #     widget=forms.RadioSelect(),
    #     choises=(('0', False), ('1', True)),
    #     initial=0
    # )