from django.db import models


class User(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID Пользователя в Telegram")
    name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    username = models.CharField(max_length=100, verbose_name="Username пользователя", null=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=100, null=True)

    def __str__(self):
        return f"User id: {self.id} ({self.user_id} - {self.name})"


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    name = models.CharField(max_length=100, verbose_name="Название услуги")

    def __str__(self):
        return self.name


class Weight(models.Model):
    class Meta:
        verbose_name = "Вес питомца"
        verbose_name_plural = "Вес питомцев"
    name = models.CharField(max_length=100, verbose_name="Вес питомца")

    def __str__(self):
        return self.name


class Service(models.Model):
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название услуги", max_length=50)
    price = models.CharField(verbose_name="Цена", max_length=50)
    description = models.TextField(verbose_name="Описание", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE)

    def __str__(self):
        return self.name





class Registration(models.Model):
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Запись"

    registrated = models.ForeignKey(User, verbose_name="Имя клиента", on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, verbose_name="Название услуги", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="Время составления записи", auto_now_add=True)
    date_of_reception = models.DateField(verbose_name="Дата записи")
    time_of_reception = models.CharField(verbose_name="Время записи", max_length=100)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=100)

