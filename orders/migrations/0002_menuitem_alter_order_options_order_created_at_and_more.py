# Generated by Django 5.2.1 on 2025-05-25 19:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('category', models.CharField(choices=[('snack', 'Закуски'), ('main', 'Основные блюда'), ('soup', 'Супы'), ('salad', 'Салаты'), ('dessert', 'Десерты'), ('drink', 'Напитки')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['category', 'name'],
            },
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='orders_orde_status_c6dd84_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['table_number'], name='orders_orde_table_n_63e048_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['created_at'], name='orders_orde_created_0e92de_idx'),
        ),
        migrations.AddIndex(
            model_name='menuitem',
            index=models.Index(fields=['category'], name='orders_menu_categor_4bb923_idx'),
        ),
        migrations.AddIndex(
            model_name='menuitem',
            index=models.Index(fields=['is_available'], name='orders_menu_is_avai_1176cf_idx'),
        ),
    ]
