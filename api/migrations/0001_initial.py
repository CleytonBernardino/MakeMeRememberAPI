# Generated by Django 4.2.4 on 2023-10-13 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TudoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Título')),
                ('content', models.TextField(max_length=255, verbose_name='Conteudo')),
                ('priority', models.IntegerField(default=1, verbose_name='Prioridade')),
                ('tag', models.CharField(default='Task', max_length=15, verbose_name='Tag')),
                ('url_img', models.URLField(blank=True, verbose_name='URL da imagem')),
                ('completed', models.BooleanField(default=False, verbose_name='Concluido')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
