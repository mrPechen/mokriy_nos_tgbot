from django.db.models import Count
from django.db.models.functions import ExtractDay
from admin.user.models import *
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def get_or_create_user(user_id, full_name, username):
    try:
        return User(user_id=int(user_id), name=full_name, username=username).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def get_phone_number(user_id):
    phone = User.objects.get(user_id=user_id).phone_number
    return phone


@sync_to_async
def save_phone_number(user_id, phone_number):
    user = User.objects.get(user_id=user_id)
    user.phone_number = phone_number
    user.save()


@sync_to_async
def save_registration(user_id, service_id, date_of_reception, time_of_reception):
    user = User.objects.get(user_id=user_id)
    service = Service.objects.get(id=service_id)
    phone = User.objects.get(user_id=user_id).phone_number
    save_all = Registration(registrated=user, service_id=service, date_of_reception=date_of_reception,
                            time_of_reception=time_of_reception, phone_number=phone).save()
    return save_all


@sync_to_async
def get_service(service_id):
    service = Service.objects.get(id=service_id)
    return service


@sync_to_async
def show_my_appointments(user_id):
    result = Registration.objects.filter(registrated__user_id=user_id).all()
    return result


@sync_to_async
def cancel_appointments(user_id, service_id, date, time):
    user = User.objects.get(user_id=user_id)
    service = Service.objects.get(id=service_id)
    result = Registration.objects.filter(registrated=user, service_id=service, date_of_reception=date, time_of_reception=time).delete()
    return result


@sync_to_async
def get_category():
    result = Category.objects.all()
    return result


@sync_to_async
def appointments_by_category(category_id, date):
    category = Category.objects.get(id=category_id)
    result = Registration.objects.filter(service_id__category=category, date_of_reception=date)
    return result


@sync_to_async
def count_appointments_by_category(category_id, date):
    category = Category.objects.get(id=category_id)
    result = Registration.objects.filter(service_id__category=category, date_of_reception=date).count()
    return result


@sync_to_async
def vet_groomer_category_filter(date):
    result = Registration.objects.filter(date_of_reception=date)
    return result


@sync_to_async
def vet_groomer_category_count(date):
    result = Registration.objects.filter(date_of_reception=date).count()
    return result


@sync_to_async
def count_by_dates(year, month):
    dates = Registration.objects.annotate(date_of_reception__day=ExtractDay('date_of_reception')
                                          ).filter(date_of_reception__year=year, date_of_reception__month=month
                                                   ).values('date_of_reception__day').annotate(count=Count('*')).order_by('date_of_reception__day')
    return dates


@sync_to_async
def search_services_by_weight(weight_id, category):
    result = Service.objects.filter(weight__id=weight_id, category__id=category).all()
    return result


@sync_to_async
def get_weight():
    result = Weight.objects.all()
    return result


@sync_to_async
def get_employee():
    result = Employee.objects.get()
    return result
