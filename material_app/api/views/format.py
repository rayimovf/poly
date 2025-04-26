from django.core import exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from utils.render_response import render_message, render_data
from ...models import Format
from ...serializers import FormatSerializer


class FormatGenericAPIView(GenericAPIView):
    queryset = Format
    serializer_class = FormatSerializer


class ListFormatView(FormatGenericAPIView):

    def get(self, request):
        try:
            format = self.queryset.objects.all().order_by('name')
            serializer = FormatSerializer(format, many=True)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class AddFormatView(FormatGenericAPIView):

    def post(self, request):
        try:
            format = self.queryset.objects.create(
                name=request.data['name'],
                size=request.data['size'],
                gram=request.data['gram'],
                type=request.data['type']
            )
            serializer = self.serializer_class(format, many=False)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_201_CREATED
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class UpdateFormatView(FormatGenericAPIView):

    def patch(self, request, format_id):
        try:
            format = self.queryset.objects.get(id=format_id)
            serializer = self.serializer_class(instance=format, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    render_data(data=serializer.data, success='true'),
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    render_message(message=serializer.errors, success='false'),
                    status = status.HTTP_400_BAD_REQUEST
                )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class DeleteFormatView(FormatGenericAPIView):

    def delete(self, request, format_id):
        try:
            format = self.queryset.objects.get(id=format_id)
            format.delete()
            return Response(
                render_message(message="format was deleted", success='true'),
                status = status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response(
                render_message(message="format does not exist", success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )