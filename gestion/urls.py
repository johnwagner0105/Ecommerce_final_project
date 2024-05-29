from django.urls import path
from .views import CreateProductView, DeleteProductView, SaleCreateView, SaleView, UpdateProductView,  CreateUserView, ListProductView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('createproducto', CreateProductView.as_view()),
    path('listarproducto', ListProductView.as_view()),
    # path('upload-image', ProductUploadImageView.as_view()),
    path('updateproducto/<int:pk>', UpdateProductView.as_view()),
    path('borrarproducto/<int:pk>', DeleteProductView.as_view()),
    path('createsale', SaleCreateView.as_view()),
    path('mostrarsales', SaleView.as_view()),
    path('createuser', CreateUserView.as_view()),
    path('login', TokenObtainPairView.as_view())
]
