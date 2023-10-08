from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
    priority = data['priority']

    exist = TudoList.objects.filter(user=user, title=title).exists()
    if exists:
        exist = False

    if not title or exist:
        raise ValidationError("Título incorreto ou já em uso.")

    if not content:
        raise ValidationError("A Conteudo está vazia!")

    if not priority:
        data['priority'] = 1
    elif priority < 1 or priority > 10:
        raise ValidationError("A prioridade deve ser entre 1 e 10")

    if len(content) > 200:
        raise ValidationError("O Conteudo está muito longo")

    data.update({'user': user})
    return data
