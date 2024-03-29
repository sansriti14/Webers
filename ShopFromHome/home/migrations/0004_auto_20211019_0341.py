# Generated by Django 3.2.3 on 2021-10-18 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20211019_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopkeeper',
            name='contactNum',
            field=models.CharField(max_length=10, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='password',
            field=models.CharField(max_length=30, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='resAddress',
            field=models.TextField(verbose_name='Residential Address'),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='shopAddress',
            field=models.TextField(verbose_name='Shop Address'),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='shopName',
            field=models.CharField(max_length=100, verbose_name='Shop Name'),
        ),
    ]
