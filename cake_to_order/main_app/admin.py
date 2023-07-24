from django.contrib import admin
from .models import Client, Cake, Topping, Berry, Decor, CakeLevel, CakeForm, OrderCake


admin.site.register(Client)
admin.site.register(Cake)
admin.site.register(Topping)
admin.site.register(Berry)
admin.site.register(Decor)
admin.site.register(CakeLevel)
admin.site.register(CakeForm)
# admin.site.register(OrderCake)

# Register your models here.
@admin.register(OrderCake)
class OrderCakeAdmin(admin.ModelAdmin):
    list_display = [
        'get_client_full_name',
        'get_cake',
        'topping',
        'berry',
        'decor',
        'inscription',
        'comment',
        'order_date',
        'order_time',
        'get_amount',
        ]
    # list_filter = ['is_speaker',]
    # search_fields = ('user__email',
    #                  'user__first_name',
    #                  'user__last_name',
    #                  'phone')


    def get_client_full_name(self, obj):
        return f'{obj.client.user.first_name} {obj.client.user.last_name}'

    get_client_full_name.short_description = 'Пользователь'


    def get_cake(self, obj):
        if obj.cake_catalog:
            cake_str = obj.cake_catalog.title
        else:
            cake_str = f'{obj.cake_form.title}, {obj.cake_level.title}'

        return cake_str

    get_cake.short_description = 'Торт'

    def get_amount(self, obj):
        amount = 0
        amount += obj.cake_catalog.price if obj.cake_catalog else 0
        amount += obj.cake_level.price if obj.cake_level else 0
        amount += obj.cake_form.price if obj.cake_form else 0
        amount += obj.topping.price if obj.topping else 0
        amount += obj.berry.price if obj.berry else 0
        amount += obj.decor.price if obj.decor else 0
        amount += 500 if obj.inscription else 0
        return f'{amount} ₽'

    get_amount.short_description = 'Сумма'
