# Generated by Django 4.1.3 on 2022-12-10 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodation', '0010_alter_book_apartment'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='booked',
            field=models.BooleanField(default=False),
        ),
    ]
