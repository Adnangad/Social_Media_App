# Generated by Django 5.1.4 on 2025-01-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='profile_pic',
            field=models.ImageField(blank=True, default='fallback.jpg', upload_to=''),
        ),
    ]
