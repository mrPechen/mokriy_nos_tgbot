from django.contrib import admin
from .models import User, Service, Registration, Category, Weight


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    show_on_dispaly = ('user_id', 'name', 'username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    show_on_dispaly = ('name')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    show_on_dispaly = ('registrated', 'service_id', 'time', 'date_of_reception', 'time_of_reception', 'phone_number')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    show_on_dispaly = ('name', 'price', 'description', 'category', 'weight')


@admin.register(Weight)
class UserAdmin(admin.ModelAdmin):
    show_on_dispaly = ('name')
