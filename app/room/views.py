from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework_tracking.mixins import LoggingMixin
from room.serializers import RoomSerializer, SchedulingSerializer
from room.models import Room, Scheduling


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class RoomViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    API que permite gerenciar as salas.
    """
    queryset = Room.objects.all().order_by('-name')
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_queryset(self):
        room = Room.objects.all()

        id = self.request.query_params.get('id', None)
        if id:
            room = room.filter(id=id)

        name = self.request.query_params.get('name', None)
        if name:
            room = room.filter(name__icontains=name)

        capacity = self.request.query_params.get('capacity', None)
        if capacity:
            room = room.filter(capacity=capacity)

        room = room.order_by('-name')
        return room


class SchedulingViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    API que permite gerenciar os agendamentos.
    """
    queryset = Scheduling.objects.all().order_by('-room__name')
    serializer_class = SchedulingSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_queryset(self):
        scheduling = Scheduling.objects.all()

        id = self.request.query_params.get('id', None)
        if id:
            scheduling = scheduling.filter(id=id)

        username = self.request.query_params.get('username', None)
        if username:
            scheduling = scheduling.filter(username=username)

        email = self.request.query_params.get('email', None)
        if email:
            scheduling = scheduling.filter(email=email)

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        check_schedules = self.request.query_params.get('check_schedules', None)

        if check_schedules and start_date and end_date:
            scheduling = scheduling.filter(
                Q(start_date__lte=start_date, end_date__gte=end_date) | 
                Q(start_date__gte=start_date, start_date__lte=end_date) |
                Q(end_date__gte=start_date, end_date__lte=end_date)
            )
        elif start_date and end_date:
            scheduling = scheduling.filter(start_date__gte=start_date, end_date__lte=end_date)
        else:
            if start_date:
                scheduling = scheduling.filter(start_date=start_date)

            if end_date:
                scheduling = scheduling.filter(end_date=end_date)

        scheduling = scheduling.order_by('-room__name')
        return scheduling