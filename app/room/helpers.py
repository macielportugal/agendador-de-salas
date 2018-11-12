from room.models import Scheduling
from django.utils.translation import gettext as _
from django.db.models import Q


def date_validation(room, schedule_id, start_date, end_date):
    messages = []

    if start_date > end_date:
        messages.append(_('Dates are incorrect'))

    scheduling = Scheduling.objects.filter(room=room).filter(
        Q(start_date__lte=start_date, end_date__gte=end_date) | 
        Q(start_date__gte=start_date, start_date__lte=end_date) |
        Q(end_date__gte=start_date, end_date__lte=end_date)
    )

    if schedule_id:
        scheduling = scheduling.exclude(id=schedule_id)

    if scheduling.exists():
        for schedule in scheduling:
            messages.append(
                ' {0} | ID: {1} | {2}: {3} | {4}: {5}'.format(
                    _('Schedule already scheduled'),
                    schedule.id,
                    _('Start'),
                    schedule.start_date.strftime('%d/%m/%Y %H:%M:%S'),
                    _('End'),
                    schedule.end_date.strftime('%d/%m/%Y %H:%M:%S')
                )
            )

    return messages
