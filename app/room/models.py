from django.db import models
from django.utils.translation import gettext as _


class Room(models.Model):
    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    name = models.CharField(_('Name'), max_length=50, unique=True)
    capacity = models.IntegerField(_('Capacity'))
    description = models.TextField(_('Description'), blank=True, null=True)

    def __str__(self):
        return self.name


class Scheduling(models.Model):
    class Meta:
        verbose_name = _('Scheduling')
        verbose_name_plural = _('Schedules')

    start_date = models.DateTimeField(
        _('Start Date'), auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(
        _('End Date'), auto_now=False, auto_now_add=False)
    room = models.ForeignKey(Room, verbose_name=_(
        'Room'), on_delete=models.CASCADE)
    username = models.CharField(_('Username'), max_length=100)
    email = models.EmailField(_('Email'), max_length=254)

    def __str__(self):
        return '{} à {} - {}'.format(self.start_date, self.end_date, self.room)