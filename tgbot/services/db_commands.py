
from admin.user.models import *
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, full_name, username):
    try:
        return User(user_id=int(user_id), name=full_name, username=username).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def search_groomer_for_mini_pet():

    result = Service.objects.filter(weight__name='Маленькие', category__name='Косметолог').all()
    return result


@sync_to_async
def search_groomer_for_middle_pet():

    result = Service.objects.filter(weight__name='Средние', category__name='Косметолог').all()
    return result


@sync_to_async
def search_groomer_for_big_pet():

    result = Service.objects.filter(weight__name='Большие', category__name='Косметолог').all()
    return result


@sync_to_async
def search_vet_for_mini_pet():

    result = Service.objects.filter(weight__name='Маленькие', category__name='Ветврач').all()
    return result


@sync_to_async
def search_vet_for_middle_pet():

    result = Service.objects.filter(weight__name='Средние', category__name='Ветврач').all()
    return result


@sync_to_async
def search_vet_for_big_pet():

    result = Service.objects.filter(weight__name='Большие', category__name='Ветврач').all()
    return result


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
def count_psycho_time(date):
    category = Category.objects.get(name='Психолог').id
    result = Registration.objects.filter(service_id__category=category, date_of_reception=date).count()
    return result


@sync_to_async
def psycho_category_filter(date):
    category = Category.objects.get(name='Психолог').id
    result = Registration.objects.filter(service_id__category=category, date_of_reception=date)
    return result


@sync_to_async
def save_psycho_registration(user_id, date_of_reception, time_of_reception):
    user = User.objects.get(user_id=user_id)
    service = Service.objects.get(name='Зоопсихолог')
    phone = User.objects.get(user_id=user_id).phone_number
    save_all = Registration(registrated=user, service_id=service, date_of_reception=date_of_reception,
                            time_of_reception=time_of_reception, phone_number=phone).save()
    return save_all


@sync_to_async
def vet_groomer_category_filter(date):
    cat = Category.objects.get(name='Психолог').id
    res = Registration.objects.exclude(service_id__category=cat).filter(date_of_reception=date)
    return res


@sync_to_async
def vet_groomer_category_count(date):
    cat = Category.objects.get(name='Психолог').id
    res = Registration.objects.exclude(service_id__category=cat).filter(date_of_reception=date).count()
    return res