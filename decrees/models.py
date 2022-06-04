from django.db import models
from django.contrib.auth.models import AbstractUser

from decrees.managers import UserManager

from datetime import datetime
# from django.contrib.auth import get_user_model
# User = get_user_model()

import datetime
# Create your models here.


class MyUser(AbstractUser):
    """
        ('password', models.CharField(max_length=128, verbose_name='password')),
        ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
        ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
        ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
        ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
        ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
        ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
        ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
        ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
        ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),

    """
    location = models.CharField(max_length=201, unique=False, default='default_location')
    # objects = UserManager()

    def get_location(self):
        return f'{self.get_username()} is located at {self.location_2}'
    


class Position(models.Model):
    name = models.CharField(max_length=800)    
    level_choices = [('federal', 'federal'),
                        ('regional','regional')]    

    level = models.CharField(max_length=50, choices=level_choices)

    def __str__(self) -> str:
        return f'{self.name}'


class Person(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.name


class Event(models.Model): 
    
    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['person','region','position', 'date'], name='unique_event'),
            
        ]

    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    event_choices = [('appoint', 'appoint'),
                        ('resign','resign')]    
    level_choices = [('federal', 'federal'),
                        ('regional','regional')]

    action = models.CharField(max_length=50, choices=event_choices)
    date = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.RESTRICT)
    level = models.CharField(max_length=51, choices=level_choices)
    full_text = models.CharField(max_length=99999, null=True)
    line = models.CharField(max_length=8000, null=True)
    link = models.CharField(max_length=2000, null=True, default='https://example.com')
    file_name = models.CharField(max_length=599, null=True, default='defaults_file_name')

    region_choices = ['Белгородская область', 'Брянская область', 'Владимирская область', 'Воронежская область', 'Ивановская область', 'Калужская область', 'Костромская область', 'Курская область', 'Липецкая область', 'Московская область', 'Орловская область', 'Рязанская область', 'Смоленская область', 'Тамбовская область', 'Тверская область', 'Тульская область', 'Ярославская область', 'Москва', 'Республика Карелия', 'Республика Коми', 'Архангельская область', 'Ненецкий автономный округ', 'Вологодская область', 'Калининградская область', 'Ленинградская область', 'Мурманская область', 'Новгородская область', 'Санкт-Петербург', 'Республика Адыгея', 'Республика Калмыкия', 'Республика Крым', 'Краснодарский край', 'Астраханская область', 'Волгоградская область', 'Ростовская область', 'Севастополь', 'Республика Башкортостан', 'Республика Марий Эл', 'Республика Мордовия', 'Республика Татарстан', 'Удмуртская Республика', 'Чувашская Республика', 'Кировская область', 'Нижегородская область', 'Оренбургская область', 'Пензенская область', 'Пермский край', 'Самарская область', 'Саратовская область', 'Ульяновская область', 'Курганская область', 'Свердловская область', 'Тюменская область', 'Челябинская область', 'Ханты-Мансийский автономный', 'Ямало-Ненецкий автономный округ', 'Республика Алтай', 'Республика Тыва', 'Республика Хакасия', 'Алтайский край', 'Красноярский край', 'Иркутская область', 'Кемеровская область', 'Новосибирская область', 'Омская область', 'Томская область', 'Республика Бурятия', 'Республика Саха (Якутия)', 'Приморский край', 'Хабаровский край', 'Амурская область', 'Камчатский край', 'Магаданская область', 'Сахалинская область', 'Забайкальский край', 'Еврейская автономная область', 'Чукотский автономный округ', 'Республика Дагестан', 'Республика Ингушетия', 'Кабардино-Балкарская Республика', 'Карачаево-Черкесская Республика', 'Республика Северная Осетия - Алания', 'Чеченская республика', 'Ставропольский край']
    region_choices = [(e,e) for e in region_choices]
    region = models.CharField(max_length=100, choices=region_choices, default='регион не указан')

    def __str__(self) -> str:
        return f'{self.action} {self.position} on {self.date}'






'''        constraints = [
            models.UniqueConstraint(
                fields=['user', 'doc_name'], name="unique_user_docname"
            ),
            models.CheckConstraint(check=models.Q(size__lte=95), name='my_size_limit')
        ]
'''    
