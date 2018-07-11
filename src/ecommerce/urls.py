
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views
#from products.views import ProductListView , ProductDetailView , ProductFeaturedListView , ProductFeaturedDetailView , ProductDetailSlugView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('login/', views.login_page,name='login'),
    path('register/', views.register_page,name='register'),
    path('contact/', views.contact,name='contact'),
    path('products/', include('products.urls')),
    #url(r'^products/', include('products.urls' ,namespace='products')),
    #path('products/<int:pk>/', ProductDetailView.as_view()),
    #path('products/<slug:slug>/', ProductDetailSlugView.as_view()),
    #path('featured/', ProductFeaturedListView.as_view()),
    #path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
]

if settings.DEBUG:
    urlpatterns=urlpatterns+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
