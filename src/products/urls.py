
from django.urls import path
from .views import ProductListView , ProductDetailView , ProductFeaturedListView , ProductFeaturedDetailView , ProductDetailSlugView

urlpatterns = [

    path('', ProductListView.as_view(), name='list'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='details'),
    #path('featured/', ProductFeaturedListView.as_view()),
    #path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
    #path('products/<int:pk>/', ProductDetailView.as_view()),
]


