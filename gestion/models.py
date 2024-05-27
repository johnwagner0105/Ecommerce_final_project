from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .auth_manager import UsuarioManager

# Create your models here.


class ProductModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('image')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'


class UsuarioModel(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True, null=False)
    password = models.TextField(null=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')

    USERNAME_FIELD = 'correo'

    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'


class SaleModel(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.FloatField()
    user = models.ForeignKey(UsuarioModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sales'


class SaleDetailModel(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    subtotal = models.FloatField()
    products_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    sale_id = models.ForeignKey(
        SaleModel, on_delete=models.CASCADE, related_name='saleDetails')

    class Meta:
        db_table = 'sale_details'
