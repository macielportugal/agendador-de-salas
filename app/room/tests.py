from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from room.models import Room, Scheduling
from datetime import datetime, timedelta
from django.utils import timezone


class SchedulerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste', email='teste@teste.com', password='123456')
        self.token = Token.objects.create(user=self.user)
        self.client_with_token = APIClient()
        self.client_with_token.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.room = Room(name='Room1', capacity=2)
        self.room.save()


class RoomTestCase(SchedulerTestCase):
    def setUp(self):
        super(RoomTestCase, self).setUp()
        self.url_list = reverse('room-list')
        self.url_update = '{0}{1}/'.format(self.url_list, self.room.id)

    def test_create_room(self):
        """
        Teste de criação de sala.
        1 - Tenta criar uma sala sem token a tentativa deve se negada.
        2 - Tenta criar uma sala com token a tentativa deve se bem-sucedida.
        3 - Tenta criar uma sala com token mas com campos vazios a tentativa deve se negada.
        """

        data = {
            'name': 'Room2',
            'capacity': 2,
            'description': ''
        }

        # 1° teste
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 2º teste
        response = self.client_with_token.post(
            self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.filter(name='Room2').count(), 1)

        data = {
            'name': '',
            'capacity': '',
            'description': ''
        }

        # 3º teste
        response = self.client_with_token.post(
            self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0].code, 'blank')
        self.assertEqual(response.data['capacity'][0].code, 'invalid')

    def test_update_room(self):
        """
        Teste de atualização de sala.
        """

        data = {
            'id': self.room.id,
            'name': 'Room3',
            'capacity': self.room.capacity,
            'description': self.room.description
        }

        response = self.client_with_token.put(
            self.url_update, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Room.objects.get(pk=self.room.pk).name, 'Room3')

    def test_list_rooms(self):
        """
        Teste de listagens de salas.
        """

        response = self.client.get(self.url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_room(self):
        """
        Teste de filtragem de sala.
        1 - Filtro por ID
        2 - Filtro por Nome
        3 - Filtro por Capacidade
        """

        # 1º teste
        response = self.client.get(self.url_list + '?id={}'.format(self.room.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 2º teste
        response = self.client.get(self.url_list + '?name={}'.format(self.room.name), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 3º teste
        response = self.client.get(self.url_list + '?capacity={}'.format(self.room.capacity), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_delete_room(self):
        """
        Teste de delete de sala.
        """

        response = self.client_with_token.delete(
            self.url_update, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.filter(pk=self.room.pk).exists(), False)


class SchedulingTestCase(SchedulerTestCase):
    def setUp(self):
        super(SchedulingTestCase, self).setUp()
        self.scheduling = Scheduling(start_date=timezone.now(), end_date=timezone.now(
        ), room=self.room, username='Fulano01', email='fulano@fulano.com.br')
        self.scheduling.save()
        self.url_list = reverse('scheduling-list')
        self.url_update = '{0}{1}/'.format(self.url_list, self.scheduling.id)
        self.data = {
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(hours=5),
            'room': self.room.id,
            'username':  'Fulano',
            'email': 'fulano@fulano.com.br'
        }

    def test_create_scheduling(self):
        """
        Teste de criação de agendamento.
        """

        response = self.client.post(self.url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client_with_token.post(
            self.url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Scheduling.objects.filter(
            username='Fulano').count(), 1)

        old_start_time = self.data['start_date']
        old_end_time = self.data['end_date']

        # Agendamento dentro de horário ocupado
        self.data['start_date'] = old_start_time + timedelta(minutes=5)
        self.data['end_date'] = old_end_time - timedelta(minutes=5)
        response = self.client_with_token.post(self.url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0].code, 'invalid')

        # Agendamento começa dentro do horário já ocupado
        self.data['start_date'] = old_start_time + timedelta(hours=1)
        self.data['end_date'] = old_end_time + timedelta(hours=5)
        response = self.client_with_token.post(self.url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0].code, 'invalid')

        # Agendamento termina dentro horário já ocupado
        self.data['start_date'] = old_start_time - timedelta(hours=5)
        self.data['end_date'] = old_end_time - timedelta(hours=1)
        response = self.client_with_token.post(self.url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0].code, 'invalid')

        data = {
            'start_date': '',
            'end_date': '',
            'room': '',
            'username': '',
            'email': ''
        }

        response = self.client_with_token.post(
            self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['start_date'][0].code, 'invalid')
        self.assertEqual(response.data['end_date'][0].code, 'invalid')
        self.assertEqual(response.data['username'][0].code, 'blank')
        self.assertEqual(response.data['email'][0].code, 'blank')
        self.assertEqual(response.data['room'][0].code, 'null')

    def test_update_scheduling(self):
        """
        Teste de atualização de agendamento.
        """

        self.data['username'] = 'Fulano02'
        response = self.client_with_token.put(self.url_update, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Scheduling.objects.get(pk=self.scheduling.id).username, 'Fulano02')

    def test_list_scheduling(self):
        """
        Teste de listagem de agendamentos.
        """

        response = self.client.get(self.url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_scheduling(self):
        """
        Teste de filtragem de sala.
        1 - Filtro por ID
        2 - Filtro por Usuário
        3 - Filtro por Email
        4 - Filtro por Room ID
        5 - Filtro por Room Nome
        """

        # 1º teste
        response = self.client.get(self.url_list + '?id={}'.format(self.scheduling.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 2º teste
        response = self.client.get(self.url_list + '?username={}'.format(self.scheduling.username), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 3º teste
        response = self.client.get(self.url_list + '?email={}'.format(self.scheduling.email), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 4º teste
        response = self.client.get(self.url_list + '?room_id={}'.format(self.room.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 5º teste
        response = self.client.get(self.url_list + '?room_name={}'.format(self.room.name), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_delete_scheduling(self):
        """
        Teste de delete de agendamento.
        """

        response = self.client_with_token.delete(self.url_update, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Scheduling.objects.filter(pk=self.scheduling.id).exists(), False)
