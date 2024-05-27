from rest_framework import serializers
from .models import ProductModel, SaleDetailModel, SaleModel, UsuarioModel


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioModel
        fields = "__all__"


class productSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.image:
    #         representation['image'] = instance.image
    #     return representation

    def get_image(self, obj):
        return obj.image.url if obj.image else None


class saleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetailModel
        fields = "__all__"


class saleSerializer(serializers.ModelSerializer):
    details = saleDetailSerializer(source='saleDetails', many=True)

    class Meta:
        model = SaleModel
        fields = "__all__"


class productUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    price = serializers.FloatField(required=False)
    stock = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)
    status = serializers.BooleanField(required=False)

    class Meta:
        model = ProductModel
        fields = "__all__"


class SaleDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetailModel
        exclude = ['sale_id', 'price', 'subtotal']


class SaleCreateSerializer(serializers.ModelSerializer):
    details = SaleDetailCreateSerializer(source='saleDetails', many=True)

    class Meta:
        model = SaleModel
        exclude = ['user', 'total']
