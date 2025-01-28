# Generated by Django 5.1.4 on 2025-01-17 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0005_posts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_comment', models.TextField(null=True)),
                ('image_comment', models.ImageField(blank=True, upload_to='')),
                ('date_comment', models.DateTimeField(auto_now=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.posts')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.people')),
            ],
        ),
    ]
