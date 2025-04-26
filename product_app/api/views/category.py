from django.core import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from utils.render_response import render_data, render_message
from ...models import Category
from ...serializers import CategorySerializer


class CategoryGenericAPIView(GenericAPIView):
    queryset = Category
    serializer_class = CategorySerializer


class ListCategoryView(CategoryGenericAPIView):

    def get(self, request):
        try:
            category = self.queryset.objects.all().order_by('-id')
            serializer = self.serializer_class(category, many=True)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class AddCategoryView(CategoryGenericAPIView):

    def post(self, request):
        try:
            category = self.queryset.objects.create(
                name=request.data['name']
            )
            category.save()
            serializer = self.serializer_class(category, many=False)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_201_CREATED
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class UpdateCategoryView(CategoryGenericAPIView):

    def patch(self, request, category_id):
        try:
            category = self.queryset.objects.get(id=category_id)
            serializer = self.serializer_class(instance=category, data=request.data, partial=True)
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


class DeleteCategoryView(CategoryGenericAPIView):

    def delete(self, request, category_id):
        try:
            category = self.queryset.objects.get(id=category_id)
            category.delete()
            return Response(
                render_message(message="Category was deleted", success='true'),
                status = status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response(
                render_message(message="Category does not exist", success="false"),
                status = status.HTTP_400_BAD_REQUEST
            )