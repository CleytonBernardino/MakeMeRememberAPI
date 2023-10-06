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
        salt = None  # Mudar para algo!!!
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
        fields = ('email', 'password')


class ListSerializer(serializers.Serializer):
    class Meta:
        model = TudoList
        fields = ('title', 'content')

    def create(self, clean_data: dict):
        obj = TudoList.objects.create(
            user=clean_data['user'],
            title=clean_data['title'],
            content=clean_data['content'],
        )
        obj.save()
        return obj

    def get_item(self, user, title):
        try:
            item = TudoList.objects.get(
                user=user,
                title=title
            )
            obj = {
                "title": item.title,
                "content": item.content,
            }
            return obj
        except TudoList.DoesNotExist:
            return {
                'Não encontrado': f'Nenhum item com o nome de {title} foi encontrado.'  # noqa: E501
            }

    def update(self, clean_data):
        try:
            item = TudoList.objects.get(
                user=clean_data['user'],
                title=clean_data['title']
            )
        except TudoList.DoesNotExist:
            return None
        item.title = clean_data['title']
        item.content = clean_data['content']
        item.save()
        return item
