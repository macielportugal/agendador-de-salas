from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from room.models import Scheduling


class Command(BaseCommand):
    help = _('Create the token for the user to use in the API.')

    def add_arguments(self, parser):
        parser.add_argument('--username', dest='username', help=_('User is allowed to access the api'), required=True)

    def handle(self, *args, **options):
        if 'username' in options:
            user = User.objects.filter(username=options['username'])

            if user.exists():
                user = user.first()
                if not Token.objects.filter(user=user).exists():
                    token = Token.objects.create(user=user)
                    self.stdout.write(self.style.SUCCESS('Token: "{}"'.format(token)))
                else:
                    raise CommandError(_('Already exists'))
            else:
                raise CommandError(_('User') + ' "{}" '.format(options['username']) + _('does not exist'))