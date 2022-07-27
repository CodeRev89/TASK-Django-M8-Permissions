import datetime

from rest_framework import generics
from rest_framework import isAuthenticated, IsAdminUser
from flights import serializers
from flights.models import Booking, Flight
from permissions import HasAuthority, IsNotTooSoon


class FlightsList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class BookingsList(generics.ListAPIView):
    serializer_class = serializers.BookingSerializer
    permission_classes= [isAuthenticated]
    def get_queryset(self):
        today = datetime.date.today()
        return Booking.objects.filter(user=self.request.user, date__gte=today)


class BookingDetails(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingDetailsSerializer
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"
    permission_classes=[ HasAuthority]


class UpdateBooking(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"
    permission_classes=[HasAuthority, istNotToosoon]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.AdminUpdateBookingSerializer

        return serializers.UpdateBookingSerializer


class CancelBooking(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"
    permission_classes=[HasAuthority, IsNotTooSoon]


class BookFlight(generics.CreateAPIView):
    serializer_class = serializers.AdminUpdateBookingSerializer
    permission_classes= [isAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, flight_id=self.kwargs["flight_id"])


class Register(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
