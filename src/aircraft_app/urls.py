from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from aircraft_app.apps.parts.views import PartViewSet
from aircraft_app.apps.aircraft.views import AircraftViewSet, assemble_aircraft
from django.urls import path
from aircraft_app.apps.accounts.frontend_views import CustomLoginView
from aircraft_app.apps.aircraft.frontend_views import aircraft_list_view
from aircraft_app.apps.parts.frontend_views import parts_list_view
from aircraft_app.apps.assembly.frontend_views import assemble_view
from aircraft_app.apps.frontend_views import dashboard_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('parts', PartViewSet, basename='parts')
router.register('aircraft', AircraftViewSet, basename='aircraft')


urlpatterns = [
    # Root redirects to login
    path('', CustomLoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/assemble/', assemble_aircraft, name='assemble-aircraft'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'),
         name='logout'),  # Redirect to login after logout
    path('dashboard/', dashboard_view, name='dashboard'),
    path('parts/', parts_list_view, name='parts_list'),
    path('assemble/', assemble_view, name='assemble'),
    path('aircraft/', aircraft_list_view, name='aircraft_list'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Aircraft Production API",
        default_version='v1',
        description="API documentation for the Aircraft Production App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
]

# This is for production static url configuration.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
