from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
class ExcursionBooking(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.CharField(max_length=5)
    people_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запись на экскурсию"
        verbose_name_plural = "Записи на экскурсии"

    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('graduate', 'Выпускник'),
        ('veteran', 'Ветеран'),
        ('parent', 'Родитель'),
        ('user', 'Пользователь'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name='Кто вы?')
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name='Год поступления/выпуска')
    group_name = models.CharField(max_length=100, blank=True, verbose_name='Группа')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Photo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)

    image = models.ImageField(upload_to='gallery/')

    created_at = models.DateTimeField(auto_now_add=True)

    image_mobile = ImageSpecField(
        source='image',
        processors=[ResizeToFit(480, 480)],
        format='WEBP',
        options={'quality': 80}
    )

    image_tablet = ImageSpecField(
        source='image',
        processors=[ResizeToFit(960, 960)],
        format='WEBP',
        options={'quality': 80}
    )

    image_desktop = ImageSpecField(
        source='image',
        processors=[ResizeToFit(1440, 1440)],
        format='WEBP',
        options={'quality': 85}
    )

    image_blur = ImageSpecField(
        source='image',
        processors=[ResizeToFit(20, 20)],
        format='WEBP',
        options={'quality': 20}
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo_detail', args=[str(self.id)])
class HistoricalEvent(models.Model):
    CATEGORY_CHOICES = [
        ('history_tekum', 'История техникума'),
        ('awards', 'Награды'),
        ('graduates', 'Выпускники'),
        ('honor_board', 'Доска почета'),
        ('living_memory', 'Живая память поколений'),
        ('ww2_participants', 'Участники ВОВ'),
        ('home_front', 'Труженики тыла'),
        ('local_wars_fallen', 'Погибшие в локальных войнах'),
        ('exhibits', 'Экспонаты'),
        ('book_of_memory', 'Книга памяти'),
        ('teachers', 'Преподаватели'),
        ('sports_glory', 'Спортивная слава'),
        ('other', 'Другое'),
    ]
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(verbose_name='Дата события', null=True, blank=True)
    image = models.ImageField(upload_to='history/', verbose_name='Изображение', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Историческое событие'
        verbose_name_plural = 'Исторические события'

    def __str__(self):
        return self.title
class CollageImage(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='excursion_collage/', verbose_name='Фото для коллажа')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Фото для коллажа'
        verbose_name_plural = 'Фото для коллажа'

    def __str__(self):
        return self.title

class RecentEvent(models.Model):
    image = models.ImageField(upload_to='Recent_event/', verbose_name='Фото для недавних событий')
    title= models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(verbose_name='Дата события', null=True, blank=True)
    class Meta:
        verbose_name = 'Недавние событие'
        verbose_name_plural = 'Недавние события'
        ordering = ['-date']
    def __str__(self):
        return self.title