# Generated by Django 4.2.9 on 2024-01-19 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCulinaryLocation', '0003_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatbotModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
        ),
    ]
