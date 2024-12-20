from django.contrib import admin
from .models import Client, ImageOption

@admin.register(ImageOption)
class ImageOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ('image',)
    list_display_links = ('image',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone_number', 'birth_date', 'gender', 'profile_image', 'created_at')
    list_filter = ('gender', 'created_at', 'birth_date')
    date_hierarchy = 'birth_date'
    list_display_links = ('user', 'first_name', 'last_name')
    raw_id_fields = ('user', 'profile_image')
    search_fields = ('first_name', 'last_name', 'phone_number', 'user__username')
    readonly_fields = ('created_at',)

    @admin.display(description='Profile Image URL')
    def profile_image_url(self, obj):
        return obj.get_profile_image_url()

    @admin.display(description='Полное имя')
    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
