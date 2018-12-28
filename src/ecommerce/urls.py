
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from carts.views import cart_detail_api_view
from . import views
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from accounts.views import LoginView,RegisterView,guest_register_view

#from products.views import ProductListView , ProductDetailView , ProductFeaturedListView , ProductFeaturedDetailView , ProductDetailSlugView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('login/', LoginView.as_view(),name='login'),
    path('register/guest', guest_register_view,name='guest_register'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path('cart/api/cart/', cart_detail_api_view,name='api-cart'),
    path('contact/', views.contact,name='contact'),
    path('checkout/address/create',checkout_address_create_view,name='checkout_address_create'),
    path('checkout/address/reuse',checkout_address_reuse_view,name='checkout_address_reuse'),
    path('products/', include(('products.urls','products'),namespace='products')),
    path('cart/', include(('carts.urls','carts'),namespace='cart')),
    path('search/', include(('search.urls','search'),namespace='search')),
    #url(r'^products/', include('products.urls' ,namespace='products')),
    #path('products/<int:pk>/', ProductDetailView.as_view()),
    #path('products/<slug:slug>/', ProductDetailSlugView.as_view()),
    #path('featured/', ProductFeaturedListView.as_view()),
    #path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
]

if settings.DEBUG:
    urlpatterns=urlpatterns+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
