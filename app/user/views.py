from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from django.core.exceptions import PermissionDenied

from user.serializers import EmployeeSerializer, AuthTokenSerializer, \
                             RestaurantSerializer


class CreateEmployeeView(generics.CreateAPIView):
    """Create a new employee in the system"""
    serializer_class = EmployeeSerializer


class CreateRestaurantView(generics.CreateAPIView):
    """Create a new restaurant in the system"""
    serializer_class = RestaurantSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageEmployeeView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated employee"""
    serializer_class = EmployeeSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        if self.request.user.is_employee:
            return self.request.user
        else:
            raise PermissionDenied()


class ManageRestaurantView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated restaurant"""
    serializer_class = RestaurantSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated restaurant user"""
        if self.request.user.is_restaurant:
            return self.request.user
        else:
            raise PermissionDenied()
