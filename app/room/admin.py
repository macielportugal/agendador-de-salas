from django.contrib import admin
from rest_framework.authtoken.models import Token
from rangefilter.filter import DateRangeFilter
from room.models import Room, Scheduling
from room.forms import SchedulingForm


admin.site.site_header = 'Administração Agendador'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'description')
    search_fields = ('name',)


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    form = SchedulingForm
    list_filter = (('start_date', DateRangeFilter), ('end_date', DateRangeFilter))
    list_display = ('start_date', 'end_date', 'room', 'username', 'email')
    search_fields = ('username', 'email')