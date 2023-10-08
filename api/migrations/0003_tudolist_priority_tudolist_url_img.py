# Generated by Django 4.2.4 on 2023-10-08 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_userid_tudolist_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tudolist',
            name='priority',
            field=models.IntegerField(default=1, verbose_name='Prioridade'),
        ),
        migrations.AddField(
            model_name='tudolist',
            name='url_img',
            field=models.URLField(blank=True, verbose_name='URL da imagem'),
        ),
    ]
