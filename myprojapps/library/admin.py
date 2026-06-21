from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .forms import *
admin.site.site_header = 'Музей ЗТТиЭ'
admin.site.site_title = 'Панель управления'
admin.site.index_title = 'Добро пожаловать!'

@admin.register(ExcursionBooking)
class ExcursionBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','phone','date','time','people_count','created_at')
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at', 'image_preview')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'date')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview'),
            'classes': ('wide',)
        }),
    )

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" height="150" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'

@admin.register(HistoricalEvent)
class HistoricalEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    fieldsets = (
        ('Основное', {'fields': ('title', 'description', 'date', 'image')}),
        ('Категоризация', {'fields': ('category',)}),
    )

@admin.register(RecentEvent)
class RecentEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title',)
@admin.register(CollageImage)
class CollageImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image_preview')
    list_editable = ('order',)
    fields = ('title', 'image', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'year', 'group_name')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')