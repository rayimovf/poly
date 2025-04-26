from django.core import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from utils.pagination import CustomPagination
from ...filter import MaterialFilter


from utils.price import get_price_values
from utils.render_response import render_data, render_message
from ...models import Format, Material
from ...serializers import MaterialListSerializer, MaterialSerializer


class ListMaterialView(APIView):
    queryset = Material
    serializer_class = MaterialListSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            material = self.queryset.fetch_available_materials()
            paginator = CustomPagination()
            page = paginator.paginate_queryset(material, request)
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST,
            )


class MaterialGenericAPIView(GenericAPIView):
    queryset = Material
    serializer_class = MaterialSerializer


class SingleMaterialView(MaterialGenericAPIView):

    def get(self, request, material_id):
        try:
            material = self.queryset.objects.get(id=material_id)
            serializer = self.serializer_class(material, many=False)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST,
            )


class AddMaterialView(MaterialGenericAPIView):

    def post(self, request):
        try:
            name = request.data.get('name')
            about = request.data.get('about')
            quantity = int(request.data['quantity'])
            is_list_price = request.data.get('is_list_price') == 'on'
            is_active = request.data.get('is_active') == 'on'
            image = request.FILES.get('image')
            format = request.data.get('format_id')
            list_price, total_price = get_price_values(request, quantity, material=None)
            material = self.queryset.objects.create(
                name=name,
                format_id=format,
                about=about,
                quantity=quantity,
                is_list_price=is_list_price,
                list_price=list_price,
                total_price=total_price,
                is_active=is_active,
                image=image,
            )
            serializer = self.serializer_class(material, many=False)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST,
            )


class UpdateMaterialView(MaterialGenericAPIView):

    def patch(self, request, material_id):
        try:
            material = self.queryset.objects.get(id=material_id)
            quantity = int(request.data.get('quantity')) if request.data.get('quantity') else material.quantity
            list_price, total_price = get_price_values(request, quantity, material)
            serializer = self.serializer_class(instance=material, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(
                    quantity=quantity,
                    list_price=list_price,
                    total_price=total_price,
                )
                return Response(
                    render_data(data=serializer.data, success='true'),
                    status = status.HTTP_200_OK,
                )
            else:
                return Response(
                    render_message(message=serializer.errors, success='false'),
                    status = status.HTTP_400_BAD_REQUEST,
                )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST,
            )



class SoftDeleteMaterialView(MaterialGenericAPIView):

    def delete(self, request, material_id):
        try:
            material = self.queryset.objects.get(id=material_id)
            material.soft_delete()
            return Response(
                render_message(message="Material was deleted", success='true'),
                status = status.HTTP_205_RESET_CONTENT
            )
        except exceptions.ObjectDoesNotExist:
            return Response(
                render_message(message="Material does not exist", success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class RestoreMaterialView(MaterialGenericAPIView):

    def post(self, request, material_id):
        try:
            material = self.queryset.objects.get(id=material_id)
            material.restore()
            return Response(
                render_message(message="Material was restored", success='true'),
                status = status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response(
                render_message(message="Material does not exist", success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class DeleteMaterialView(MaterialGenericAPIView):

    def delete(self, request, material_id):
        try:
            material = self.queryset.objects.get(id=material_id)
            material.delete()
            return Response(
                render_message(message="Material was deleted", success='true'),
                status = status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response(
                render_message(message="Material does not exist", success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class FilterMaterialView(GenericAPIView):
    serializer_class = MaterialListSerializer
    queryset = Material.fetch_available_materials()
    filterset_class = MaterialFilter
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)