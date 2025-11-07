from rest_framework import viewsets, mixins
from cv_app.models import CV
from .serializers import CVSerializer

class CVViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CVSerializer

    def get_queryset(self):
        return (
            CV.objects.only("id", "firstname", "lastname", "bio", "skills", "projects", "contacts")
              .order_by("lastname", "firstname")
        )
