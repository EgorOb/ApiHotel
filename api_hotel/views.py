from .models import Hotel, Room, Booking, Review
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer, ReviewSerializer, RegisterSerializer
from rest_framework import viewsets, permissions, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Только админ может создавать, изменять, удалять
        return [permissions.AllowAny()]  # Пользователь может только смотреть


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['room_type']
    filterset_fields = ['hotel', 'room_type']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Только админ может создавать, изменять, удалять
        return [permissions.AllowAny()]  # Пользователь может только смотреть


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'create', 'retrieve', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hotel']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.serializer_class(data=request.data)
        user.is_valid(raise_exception=True)
        created_user = user.save()
        refresh = RefreshToken.for_user(created_user)
        return Response({
            "user": user.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

