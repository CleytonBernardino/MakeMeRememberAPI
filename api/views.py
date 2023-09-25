from django.core.exceptions import ValidationError
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
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # noqa: E501
            return Response(status=status.HTTP_400_BAD_REQUEST)


class InsertList(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            clean_data = list_validation(request.user, request.data)
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        serializer = ListSerializer(data=clean_data)
        if serializer.is_valid():
            tlist = serializer.create(clean_data)
            if tlist:
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # noqa: E501
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        title = request.GET.get('title', None)
        if not title:
            return Response({
                "Informação necessaria": "O título deve ser mandado na requisição"  # noqa: E501
            })

        serializer = ListSerializer()
        item = serializer.get_item(request.user, title)
        return Response(item)

    def post(self, request):
        try:
            clean_data = list_validation(
                request.user, request.data, exists=True
            )
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        serializer = ListSerializer()
        item = serializer.update(clean_data)
        if item:
            return Response({"Atualizado": "O item foi atualizado com sucesso"})  # noqa: E501

        return Response(
            {'Não encontrado': 'Não foi possível atualizar o item'},
            status=status.HTTP_409_CONFLICT
        )
