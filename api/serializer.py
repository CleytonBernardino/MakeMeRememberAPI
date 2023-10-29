from random import choice
from string import ascii_letters

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import TudoList

userModel = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    class Meta:
        model = userModel
        fields = ['usenarme', 'password']

    def password_hasher(self, password: str):
        chars = ascii_letters
        salt = ''.join(choice(chars) for _ in range(10))  # pode ser que não funcione # noqa: E501
        return make_password(password, salt)

    def create(self, clean_data: dict):
        password = make_password(clean_data['password'])
        user_obj = userModel.objects.create(
            username=clean_data['username'],
            password=password,
        )
        user_obj.save()
        return user_obj


class userSerializer(serializers.Serializer):
    class Meta:
        model = userModel
        fields = ('username', 'password')


class ListSerializer(serializers.Serializer):
    class Meta:
        model = TudoList
        fields = ('title', 'content')

    def create(self, clean_data: dict):
        obj = TudoList.objects.create(
            user=clean_data['user'],
            title=clean_data['title'],
            content=clean_data['content'],
            priority=clean_data['priority'],
            tag=clean_data['tag'],
            url_img=clean_data.get('url', 'None'),
            completed=False,
        )
        obj.save()
        return obj

    def get_item(self, user, id: int):
        try:
            item = TudoList.objects.get(
                user=user,
                pk=id
            )
            obj = {
                "id": item.pk,
                "title": item.title,
                "content": item.content,
                "priority": item.priority,
                "tag": item.tag,
                "url": item.url_img,
                "completed": item.completed,
            }
            return obj
        except TudoList.DoesNotExist:
            return {
                'Não encontrado': f'Nenhum item com o id: {id} foi encontrado.'
            }

    def get_all(self, user, completed=None):
        if completed is not None:
            tasks = TudoList.objects.filter(
                user=user, completed=completed
            ).order_by('-priority')
        else:
            tasks = TudoList.objects.filter(
                user=user
            ).order_by('-priority')
        return tasks.values()

    def update(self, id: int, clean_data: dict):
        try:
            item = TudoList.objects.get(
                user=clean_data['user'],
                pk=id
            )
        except TudoList.DoesNotExist:
            return None
        item.title = clean_data['title']
        item.content = clean_data['content']
        item.priority = clean_data['priority']
        item.tag = clean_data['tag']
        item.url_img = clean_data['url']
        item.completed = clean_data['completed']
        item.save()
        return item

    def delete(self, user, id: int):
        try:
            task = TudoList.objects.get(
                user=user,
                pk=id
            )
            task.delete()
            return "Tarefa apagada com sucesso"
        except TudoList.DoesNotExist:
            raise ValueError("Tarefa não encontrada")
