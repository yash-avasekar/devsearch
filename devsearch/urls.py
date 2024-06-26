"""
URL configuration for devsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,include('users.urls')),
    path('projects/' ,include('projects.urls')),

    # these are the default template provided by django (name should be exactly same)
    # to modify the default template style provide your template_name='template.html'
    path('reset-password/' ,auth_views.PasswordResetView.as_view(template_name='reset-password.html')
            ,name='reset_password'
    ),

    path('reset-password-sent/' ,auth_views.PasswordResetDoneView.as_view(template_name='reset-password-sent.html') 
            ,name='password_reset_done'
    ),

    path('reset/<uidb64>/<token>/' ,auth_views.PasswordResetConfirmView.as_view(template_name='reset.html') 
            ,name='password_reset_confirm'
    ),
            
    path('reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset-password-complete.html') 
            ,name='password_reset_complete'
    ),


    # api routes/endpoints
    path('api/' ,include('api.urls'))
]

urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)

# when debug is false (while in production phase) set this to url
urlpatterns += static(settings.STATIC_URL ,document_root = settings.STATIC_ROOT)
