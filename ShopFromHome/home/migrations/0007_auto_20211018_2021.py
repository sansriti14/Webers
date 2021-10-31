# Generated by Django 3.2.8 on 2021-10-18 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_responses_requestid'),
    ]

    operations = [
        migrations.AddField(
            model_name='responses',
            name='customer',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='responses',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]