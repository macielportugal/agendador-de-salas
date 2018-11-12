from rest_framework import serializers
from room.models import Room, Scheduling
from room.helpers import date_validation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class SchedulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduling
        fields = '__all__'

    def validate(self, data):
        object_id = (self.instance.id if self.instance else None)
        validation = date_validation(
            data['room'], object_id, data['start_date'], data['end_date'])
        if validation:
            raise serializers.ValidationError(','.join(validation))
        return data
