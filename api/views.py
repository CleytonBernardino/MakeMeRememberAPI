from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import ListSerializer, UserRegisterSerializer
from .validation import custom_validation, list_validation


class Register(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
        except ValidationError as e:
            return Response(e, status=status.HTTP_409_CONFLICT)

        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.create(clean_data)
            if user:
                return Response({"msg": "Conta criado com sucesso"}, status=status.HTTP_201_CREATED)  # noqa: E501
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Tasks(APIView):
    permission_classes = (IsAuthenticated, )
    serializer = ListSerializer()

    def get(self, request):
        title = request.GET.get('title', None)

        if not title:
            data = self.serializer.get_all(request.user)
            return Response(data)

        item = self.serializer.get_item(request.user, title)
        return Response(item)

    def post(self, request):
        try:
            clean_data = list_validation(request.user, request.data)
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        serializer = ListSerializer(data=clean_data)
        if serializer.is_valid():
            tlist = serializer.create(clean_data)
            if tlist:
                return Response({"msg": "Tarefa criada com sucesso"}, status=status.HTTP_201_CREATED)  # noqa: E501
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            clean_data = list_validation(
                request.user, request.data, exists=True
            )
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        item = self.serializer.update(clean_data)
        if item:
            return Response({"Atualizado": "O item foi atualizado com sucesso"})  # noqa: E501

        return Response(
            {'Não encontrado': 'Não foi possível atualizar o item'},
            status=status.HTTP_409_CONFLICT
        )

    def delete(self, request):
        try:
            data = self.serializer.delete(
                user=request.user,
                title=request.GET['title']
            )
            return Response(data)
        except ValueError:
            msg = {'msg': 'Não foi possivel apagar a tarefa'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


def loadjson(request):
    with open('api/doc/swagger.json', 'r') as json:
        json_content = json.read()

    return HttpResponse(
        json_content,
        content_type='application/json',
        status=200
    )
