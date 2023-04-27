from django.db.models import Model
from django.http import HttpRequest
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.viewsets import ViewSet


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(
        self,
        request: HttpRequest,
        _view: ViewSet,
        obj: Model,
    ) -> bool:
        return request.method in SAFE_METHODS or obj.author == request.user
