# Generated by Django 5.0.7 on 2024-07-29 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_picture',
            field=models.ImageField(default='default_cover_pic.jpg', upload_to=''),
        ),
    ]
