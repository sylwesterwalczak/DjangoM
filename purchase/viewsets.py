from datetime import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.views import APIView
from authx.permissions import IsCashierUser
from utils.mixins import CustomLoggingViewSetMixin
from .serializers import (
    CreatePurchaseOrderSerializer,
    PurchaseOrderSerializer,
    ListPurchaseOrderSerializer,
    PurchaseOrderSerializerCancelling
)
from .models import PurchaseOrder


class PurchseListView(CustomLoggingViewSetMixin, ListAPIView):
    """
    PurchseListView

    Returns the list of current orders.

    /users?status=1,2,3

    """
    serializer_class = ListPurchaseOrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        today = datetime.now()
        queryset = PurchaseOrder.objects.filter(
            created_date__date=today
        )
        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status__in=status.split(','))
        return queryset


class PurchseViewSet(CustomLoggingViewSetMixin,
                     CreateModelMixin,
                     ListModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     GenericViewSet):

    """
    PurchseViewSet

    """

    queryset = PurchaseOrder.objects.all()
    permission_classes = [IsCashierUser]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'create']:
            return CreatePurchaseOrderSerializer
        else:
            return PurchaseOrderSerializer


class CancellingPurchase(CustomLoggingViewSetMixin, APIView):
    permission_classes = [IsCashierUser]

    def _get_purchase_id(self):
        return self.kwargs.get('pk', None)

    def _get_purchase(self):
        obj = get_object_or_404(PurchaseOrder, id=self._get_purchase_id())
        return obj

    def patch(self, request, *args, **kwargs):
        purchase = self._get_purchase()
        self.check_object_permissions(request, purchase)
        purchase.items.set([])
        purchase.status = 5
        purchase.save()
        res = PurchaseOrderSerializerCancelling(purchase, many=False)
        return Response(res.data, status=HTTP_200_OK)
