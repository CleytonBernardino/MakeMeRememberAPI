from json import dumps as json_dumps

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from yaml import safe_load as yaml_safe_load

from .serializer import ListSerializer, UserRegisterSerializer
from .validation import custom_validation, list_validation, user_exist


class Login(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = user_exist(username, password)
        if not user:
            return Response({"msg": "Usuário ou senha inválida"}, status=400)

        return Response({
            "token": str(AccessToken.for_user(user)),
            "user": user.get_username()
        })


class Register(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
        except ValidationError as e:
            return Response(e, status=422)

        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.create(clean_data)
            if user:
                return Response({"msg": "Conta registrada com sucesso"}, status=201)  # noqa: E501
            return Response(status=400)


class Tasks(APIView):
    permission_classes = (IsAuthenticated, )
    serializer = ListSerializer()

    def get(self, request, id: int = 0):
        completed = request.GET.get('completed', None)
        if completed is not None:
            completed = True if completed == 'true' else False

        if id == 0:
            data = self.serializer.get_all(
                request.user, completed
            )
            return Response(data)

        item = self.serializer.get_item(user=request.user, id=id)
        return Response(item)

    def post(self, request):
        try:
            clean_data = list_validation(request.user, request.data)
        except ValidationError as e:
            return Response({"msg": e}, status=422)

        serializer = ListSerializer(data=clean_data)
        if serializer.is_valid():
            tlist = serializer.create(clean_data)
            if tlist:
                return Response({"msg": "Tarefa criada com sucesso"}, status=201)  # noqa: E501
            return Response(status=400)

    def put(self, request):
        try:
            clean_data = list_validation(
                request.user, request.data, exists=True
            )
        except ValidationError as e:
            return Response(e, status=422)

        item = self.serializer.update(request.data['id'], clean_data)
        if item:
            return Response({"msg": "Tarefa atualizada com sucesso"})  # noqa: E501

        return Response(
            {'msg': 'Não foi possível atualizar a tarefa'}, status=400
        )

    def delete(self, request, id: int):
        try:
            task = self.serializer.delete(
                user=request.user,
                id=id
            )
            return Response({"msg": task})
        except ValueError as err:
            return Response(
                {"msg": str(err)}, status=404
            )


def loadjson(request):
    with open('api/doc/doc.yaml', 'r') as file:
        json_content = json_dumps(yaml_safe_load(file))

    return HttpResponse(
        json_content,
        content_type='application/json',
        status=200
    )
