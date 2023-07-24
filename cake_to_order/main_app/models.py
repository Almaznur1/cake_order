from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers


from PIL import Image, ImageDraw, ImageFont

from torchvision.transforms import PILToTensor, ToPILImage
from torchvision.utils import make_grid

from more_itertools import chunked

import base64
import io
import sys


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Клиент')

    telegram_id = models.CharField(
        'Telegram id',
        max_length=50,
        db_index=True)

    phone = PhoneNumberField(
        'Номер телефона',
        null=True,
        blank=True)
    adress = models.CharField(
        'Адрес',
        max_length=50,
        null=True,
        blank=True)


    class Meta:
        verbose_name='Клиент'
        verbose_name_plural='Клиенты'


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, тел.: {self.phone}'


    def get_client(tel_id):
        client = Client.objects.filter(telegram_id=tel_id).first()
        if client:
            return {
                'name': client.user.first_name,
                'phone': phonenumbers.format_number(
                         client.phone,
                         phonenumbers.PhoneNumberFormat.E164),
                'adress': client.adress}
        else:
            return None


class Cake(models.Model):
    title = models.CharField(
        'Название',
        max_length=50)
    description = models.TextField(
        'Описание',)
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2)
    weight = models.DecimalField(
        'Вес',
        max_digits=4,
        decimal_places=2)
    image = models.ImageField(
        'Картинка',
        upload_to='cakes_img')


    class Meta:
        verbose_name='Торт'
        verbose_name_plural='Торты'


    def __str__(self):
        return f'{self.title}, {self.weight} кг., {self.price} р.'


    def get_cakes():
        cakes = []
        base = Cake.objects.all()
        base_chunk = chunked(base, 6)
        if sys.platform == 'linux':
            font_name = 'arial.ttf'
        else:
            font_name = 'Helvetica'
        for record_page in base_chunk:
            image_ids = []
            imgs = []
            for record in record_page:
                image = Image.open(record.image)
                ImageDraw.Draw(image). \
                    rectangle((0, 0, 100, 60), fill='white')

                ImageDraw.Draw(image).text(
                    (10, 10),  # Coordinates
                    str(record.id),  # Text
                    (0, 0, 0),  # Color
                    font=ImageFont.truetype(font=font_name, size=50))  # Helvetica arial.ttf FreeSans.ttf
                image_ids.append(record.id)
                imgs.append(image)

            grid = make_grid([PILToTensor()(img) for img in imgs],
                nrow=3,
                padding=25,
                pad_value=255)

            image_buf = ToPILImage()(grid)
            buffer = io.BytesIO()
            image_buf.save(buffer, format='png')
            # img_str = base64.b64encode(buffer.getvalue()).decode('utf8')

            cakes.append({'img': buffer.getvalue(),
                           'id': image_ids})

        return cakes


    def get_cake(id):
        cake = Cake.objects.get(id=id)
        img = cake.image
        description = f'<b>{cake.title}</b>\n' \
            f'{cake.description}\n' \
            f'<b>{cake.price} ₽ / {cake.weight} кг.</b>'
        return {'img': img,
                'text': description}


class Topping(models.Model):
    title = models.CharField(
        'Название',
        max_length=50)
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2)


    class Meta:
        verbose_name='Топпинг'
        verbose_name_plural='Топпинги'


    def __str__(self):
        return f'{self.title}, {self.price} р.'


    def get_topping():
        base = Topping.objects.all()
        toppings = {}
        for record in base:
            toppings[record.id] = f'{record.title} (+ {int(record.price)} р.)'

        return toppings



class Berry(models.Model):
    title = models.CharField(
        'Название',
        max_length=50)
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2)


    class Meta:
        verbose_name='Ягода'
        verbose_name_plural='Ягоды'


    def __str__(self):
        return f'{self.title}, {self.price} р.'

    def get_berry():
        base = Berry.objects.all()
        berrys = {}
        for record in base:
            berrys[record.id] = f'{record.title} (+ {int(record.price)} р.)'

        return berrys


class Decor(models.Model):
    title = models.CharField(
        'Название',
        max_length=50)
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2)


    class Meta:
        verbose_name='Декор'
        verbose_name_plural='Декор'


    def __str__(self):
        return f'{self.title}, {self.price} р.'


    def get_decor():
        base = Decor.objects.all()
        decors = {}
        for record in base:
            decors[record.id] = f'{record.title} (+ {int(record.price)} р.)'

        return decors


class CakeLevel(models.Model):
    title = models.CharField(
        'Название',
        max_length=50)
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2)


    class Meta:
        verbose_name='Уровень'
        verbose_name_plural='Уровни'


    def __str__(self):
        return f'{self.title}, {self.price} р.'


    def get_cake_level():
        base = CakeLevel.objects.all()
        cake_levels = {}
        for record in base:
            cake_levels[record.id] = f'{record.title} (+ {int(record.price)} р.)'

        return cake_levels


class CakeForm(models.Model):
    title = models.CharField(
        'Название',
        max_length=50)
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2)


    class Meta:
        verbose_name='Форма'
        verbose_name_plural='Формы'


    def __str__(self):
        return f'{self.title}, {self.price} р.'


    def get_cake_form():
        base = CakeForm.objects.all()
        cake_form = {}
        for record in base:
            cake_form[record.id] = f'{record.title} (+ {int(record.price)} р.)'

        return cake_form


class OrderCake(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Клиент',
        related_name='orders')
    cake_catalog = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Торт',
        related_name='orders',
        blank=True)
    cake_level = models.ForeignKey(
        CakeLevel,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Уровень',
        related_name='orders',
        blank=True)
    cake_form = models.ForeignKey(
        CakeForm,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Форма',
        related_name='orders',
        blank=True)
    topping =  models.ForeignKey(
        Topping,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Топпинг',
        related_name='orders',
        blank=True)
    berry =  models.ForeignKey(
        Berry,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Ягоды',
        related_name='orders',
        blank=True)
    decor =  models.ForeignKey(
        Decor,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Декор',
        related_name='orders',
        blank=True)
    inscription = models.CharField(
        'Надпись',
        null=True,
        max_length=200,
        blank=True)
    comment = models.TextField(
        'Комментарий',
        null=True,
        blank=True)
    order_date = models.DateField(
        verbose_name='Доставка',
        default=timezone.now)
    CHOICES = (
        ('AM', '11:00 - 15:00'),
        ('PM', '15:00 - 19:00'),
    )
    order_time = models.CharField(
        verbose_name='Время доставки',
        max_length=15,
        choices=CHOICES,
        default='PM')


    class Meta:
        verbose_name='Заказ'
        verbose_name_plural='Заказы'


    def __str__(self):
        return f'{self.client}, {self.order_date} {self.order_time}'


    def save_order(from_telegram):
        
        if len(from_telegram['name'].split()) > 1:
            first_name = from_telegram['name'].split()[0]
            last_name = from_telegram['name'].split()[1]
        else:
            first_name = from_telegram['name']
            last_name = ''

        client = Client.objects.\
            filter(telegram_id=from_telegram['telegram_id']).\
            first()
        if not client:
            user = User.objects.create(
                username=f'{first_name} {last_name}',
                first_name=first_name,
                last_name=last_name)

            client = Client.objects.create(
                user=user,
                telegram_id=from_telegram['telegram_id'],
                phone=from_telegram['phone'],
                adress=from_telegram['address'])

        for key, value in from_telegram.items():
            from_telegram[key] = value if value != 'no_data' else None

        cake_value = from_telegram['cake_id']
        cake_level_value = from_telegram['level_id']
        cake_form_value = from_telegram['shape_id']
        topping_value = from_telegram['topping_id']
        berry_value = from_telegram['berry_id']
        decor_value = from_telegram['decor_id']
        time_value = 'PM' if from_telegram['time'] == '15:00 - 19:00' else 'AM'
        # 'date': '30.07'
        from datetime import datetime
        date_value = timezone.make_aware(datetime.strptime(
            from_telegram['date']+'.2023',
            '%d.%m.%Y'))

        cake = Cake.objects.get(id=cake_value) if cake_value else None

        level = CakeLevel.objects.get(id=cake_level_value) \
            if cake_level_value else None

        form = CakeForm.objects.get(id=cake_form_value) \
            if cake_form_value else None

        topping = Topping.objects.get(id=topping_value) \
            if topping_value else None

        berry = Berry.objects.get(id=berry_value) \
            if berry_value else None

        decor = Decor.objects.get(id=decor_value) \
            if decor_value else None

        order = OrderCake.objects.create(
            client=client,
            cake_catalog= cake,
            cake_level=level,
            cake_form=form,
            topping=topping,
            berry=berry,
            decor=decor,
            inscription=from_telegram['inscription'],
            comment=from_telegram['comment'],
            order_date=date_value,
            order_time=time_value
            )
        amount = 0;
        amount += order.cake_catalog.price if order.cake_catalog else 0
        amount += order.cake_level.price if order.cake_level else 0
        amount += order.cake_form.price if order.cake_form else 0
        amount += order.topping.price if order.topping else 0
        amount += order.berry.price if order.berry else 0
        amount += order.decor.price if order.decor else 0
        amount += 500 if order.inscription else 0

        if order.cake_catalog:
            cake_str = order.cake_catalog.title
        else:
            cake_str = f'{order.cake_form.title}, {order.cake_level.title}'

        return f'{order.client.user.first_name} Вы заказали:\n'\
               f'<b>{cake_str}</b>\n'\
               f'Топпинг: <b>{order.topping.title if order.topping else "-"}</b>\n'\
               f'Ягоды: <b>{order.berry.title if order.berry else "-"}</b>\n'\
               f'Декор: <b>{order.decor.title if order.decor else "-"}</b>\n'\
               f'Надпись: <b>{order.inscription if order.inscription else "-"}</b>\n'\
               f'Коментарий: <b>{order.comment if order.comment else "-"}</b>\n'\
               f'Доставка: <b>{order.order_date.strftime("%d.%m")}, {order.order_time}</b>\n'\
               f'На сумму: <b>{amount} ₽</b>'









