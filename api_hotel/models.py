from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# Пользователь
class User(AbstractUser):
    pass


# Отель
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.name


# Номер
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.hotel.name} - {self.room_number}"


# Бронирование
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Booking by {self.user.username} - Room {self.room.id}"


# Отзыв
class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.hotel.name}"
