from django.shortcuts import render
from rest_framework import generics, response, status, request, permissions
from .models import ProductModel, SaleDetailModel, SaleModel, UsuarioModel
from .serializers import productSerializer, saleDetailSerializer, saleSerializer, productUpdateSerializer, SaleCreateSerializer, SaleDetailCreateSerializer, userSerializer
from django.db import transaction
from cloudinary import uploader

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    def post(self, request: request.Request):
        serializador = userSerializer(data=request.data)
        if serializador.is_valid():
            nuevo_usuario = UsuarioModel(**serializador.validated_data)
            nuevo_usuario.set_password(
                serializador.validated_data.get('password'))
            nuevo_usuario.save()
            return response.Response(data={
                'mensaje': 'Usuario creado exitosamente',
            }, status=status.HTTP_201_CREATED)
        else:
            return response.Response(data={
                'message': 'Error al registrar al usuario',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class CreateProductView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductModel.objects.all()
    serializer_class = productSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = request.FILES.get('image')
        if image:
            uploaded_image = uploader.upload(image)
            serializer.validated_data['image'] = uploaded_image['secure_url']
        serializer.validated_data['status'] = True
        # print(serializer.validated_data)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListProductView(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = productSerializer

# class ProductUploadImageView(generics.GenericAPIView):
#     serializer_class = productSerializer

#     def post(self, request, *args, **kwargs):
#         try:
#             imageFile = request.FILES.get('image')

#             if not imageFile:
#                 raise Exception("no se ha enviado ninguna imagen")

#             uploadedImage = upload(imageFile)
#             imageName = uploadedImage['secure_url'].split('/')[-1]
#             imagePath = f'{uploadedImage["resource_type"]}/{uploadedImage["type"]}/v{uploadedImage["version"]}/{imageName}'
#             return response.Response({
#                 'url': imagePath,
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return response.Response({
#                 'errors': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProductView(generics.UpdateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = productUpdateSerializer


class DeleteProductView(generics.DestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = productSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.status = False
            instance.save()

            return response.Response({
                'message': 'Producto eliminado correctamente'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaleView(generics.ListAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = saleSerializer


class SaleCreateView(generics.CreateAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            data = request.data

            user = request.user

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            sale = SaleModel.objects.create(total=0, user=user)
            total = 0

            items = []

            for item in data['details']:
                productId = item['products_id']
                product = ProductModel.objects.get(id=productId)
                quantity = item['quantity']
                price = product.price

                if product.stock < quantity:
                    raise Exception(
                        f'No hay suficiente stock para el producto {product.name}')

                product.stock -= quantity
                product.save()

                subtotal = float(quantity)*float(price)

                total += subtotal

                saleDetail = SaleDetailModel.objects.create(
                    quantity=quantity,
                    price=price,
                    subtotal=subtotal,
                    products_id=product,
                    sale_id=sale
                )

                saleDetail.save()

            sale.total = total
            sale.save()

            return response.Response({
                'message': 'Venta realizada correctamente'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return response.Response({
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
