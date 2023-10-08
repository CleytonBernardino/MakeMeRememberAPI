from django.contrib.auth.models import User
from django.db import models


class TudoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=50)
    content = models.TextField('Conteudo', max_length=255)
    priority = models.IntegerField('Prioridade', default=1)
    url_img = models.URLField('URL da imagem', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.user.username} ({self.title})'
