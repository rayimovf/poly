from django.core import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from utils.finance_updater import update_expense, update_income
from utils.product_updater import handle_material_change
from utils.finance_creater import create_expense, create_income
from utils.material_updater import update_material
from utils.category_updater import update_category, handle_category_change
from utils.fields import get_product_data
from utils.render_response import render_message, render_data
from ...models import Product
from ...serializers import ProductListSerializer, ProductSerializer

class ProductGenericAPIView(GenericAPIView):
    queryset = Product
    serializer_class = ProductSerializer


class ListProduct(APIView):
    serializer_class = ProductListSerializer
    queryset = Product

    def get(self, request):
        try:
            product = self.queryset.objects.all().order_by('-id')
            serializer = self.serializer_class(product, many=True)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class DetailProductView(ProductGenericAPIView):

    def get(self, request, product_id):
        try:
            product = self.queryset.objects.get(id=product_id)
            serializer = self.serializer_class(product, many=False)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class AddProductView(ProductGenericAPIView):

    def post(self, request):
        try:
            data = get_product_data(request)
            if not update_material(material=data['material'], quantity=data['quantity']):
                return Response(
                    render_message(message="Material update failed", success='false'),
                    status = status.HTTP_400_BAD_REQUEST
                )
            update_category(category=data['category'], quantity=1, total_price=data['total_price'])
            product = self.queryset.objects.create(
                owner_full_name=data['owner_full_name'],
                owner_phone_number=data['owner_phone_number'],
                about=data['about'],
                image=data['image'],
                documentation=data['documentation'],
                quantity=data['quantity'],
                is_list_price=data['is_list_price'],
                list_price=data['list_price'],
                total_price=data['total_price'],
                material=data['material'],
                category=data['category'],
            )
            expense = create_expense(product_id=product.id)
            income = create_income(product_id=product.id)
            serializer = self.serializer_class(product, many=False)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_201_CREATED
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
            )


class UpdateProductView(ProductGenericAPIView):

    def patch(self, request, product_id):
        try:
            product = self.queryset.objects.get(id=product_id)
            data = get_product_data(request)
            handle_material_change(product=product, data=data)
            handle_category_change(product=product, data=data)
            serializer = self.serializer_class(instance=Product, data=data, partial=True)
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
            update_expense(product=product)
            update_income(product=product)
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class SoftDeleteProductView(ProductGenericAPIView):

    def delete(self, request, product_id):
        try:
            product = self.queryset.objects.get(id=product_id)
            product.soft_delete()
            return Response(
                render_message(message="Product was deleted", success='true'),
                status = status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as error:
            return Response(
                render_message(message="Product does not exist", success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class RestoreProductView(ProductGenericAPIView):

    def post(self, product_id):
        try:
            product = self.queryset.objects.get(id=product_id)
            product.restore()
            return Response(
                render_message(message="Product was restored", success='true'),
                status = status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as error:
            return Response(
                render_message(message="Product does not exist", success='false'),
            )


class DeleteProductView(ProductGenericAPIView):

    def delete(self, request, product_id):
        try:
            product = self.queryset.objects.get(id=product_id)
            product.delete()
            return Response(
                render_message(message="Product was deleted", success='true'),
                status = status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as error:
            return Response(
                render_message(message="Product does not exist", success='false'),
            )