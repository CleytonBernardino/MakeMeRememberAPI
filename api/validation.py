from django.contrib.auth import authenticate, get_user_model
from rest_framework.serializers import ValidationError

from .models import TudoList

userModel = get_user_model()


def custom_validation(data):
    user = data['username'].strip()
    password = data['password'].strip()

    if not user or userModel.objects.filter(username=user).exists():
        raise ValidationError('Usuario já existe')

    if not password or len(password) < 8:
        raise ValidationError('A senha deve conter 8 caracteres no mínimo.')

    return data


def user_exist(username: str, password: str):
    return authenticate(
        username=username,
        password=password
    )


def user_validation(data):
    username = data['username']
    password = data['password']

    if not username:
        raise ValidationError("Usuario está em branco")

    if not password:
        raise ValidationError("Senha está em branco")

    return data


def list_validation(user, data: dict, exists: bool = False):
    title = data['title']
    content = data['content']
    priority = data.get('priority', 1)
    tag = data['tag']

    exist = TudoList.objects.filter(user=user, title=title).exists()
    if exists:
        exist = False

    if not title or exist:
        raise ValidationError("Título incorreto ou já em uso.")

    if not content:
        raise ValidationError("Conteudo está vazio.")

    try:
        priority = int(priority)
        if priority < 0 or priority > 10:
            raise ValidationError("A prioridade deve ser entre 1 e 10")
    except ValueError:
        raise ValidationError("A prioridade deve ser um número inteiro")

    if not tag:
        data['tag'] = 'Task'

    if len(content) > 200:
        raise ValidationError("O Conteudo está muito longo")

    data['priority'] = priority
    data.update({'user': user})
    return data
