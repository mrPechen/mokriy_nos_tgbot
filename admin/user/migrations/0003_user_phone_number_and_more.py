# Generated by Django 4.1.7 on 2023-03-03 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_registration_service_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=100, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='date_of_reception',
            field=models.DateField(verbose_name='Дата записи'),
        ),
    ]
