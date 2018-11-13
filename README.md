# Agendador de salas

## Resumo

O agendador permite criar e gerenciar agendamentos de salas de reuniões atráves de API ou pela Interface web.

## Requisitos
* <a href="https://www.docker.com/">Docker</a>
* <a href="https://docs.docker.com/compose/">Docker Compose</a>

## Instalação
```bash
git clone git@github.com:macielportugal/agendador-de-salas.git
cd agendador-de-salas
docker-compose build
docker-compose up -d
```

## Uso
O sistema pode se gerenciado pela interface web na url <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> ou por <a href="http://127.0.0.1:8000/api">API</a>.

Em ambos os casos é necessário criar um usuário e um token de acesso, os mesmos
podem se criados com os comandos abaixo.

```bash
docker-compose exec web sh 
# Dentro do container web
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@admin.com
python manage.py createtoken --username admin
```
<br />

### API

#### Salas

Listagem de salas:

```bash
curl -X GET http://127.0.0.1:8000/api/rooms/
```

Criação de sala:

```bash
curl -X POST  http://127.0.0.1:8000/api/rooms/  -H "Authorization: Token cff0071b78232725662b7726c5de2809c90749d5"  -H "Content-Type:application/json"  -d '{"name": "Sala Teste", "capacity": 8, "description": "Com TV e Ar Condicionado" }'
```

Atualização de sala:

```bash
curl -X PUT  http://127.0.0.1:8000/api/rooms/7/  -H "Authorization: Token cff0071b78232725662b7726c5de2809c90749d5"  -H "Content-Type:application/json"  -d '{"name": "Sala Teste 2", "capacity": 8, "description": "Com TV e Ar Condicionado" }'
```

Remoção da sala:

```bash
curl -X DELETE  http://127.0.0.1:8000/api/rooms/7/  -H "Authorization: Token cff0071b78232725662b7726c5de2809c90749d5"
```

Filtros:

Campos disponivéis id, name e capacity.

```bash
curl -X GET http://127.0.0.1:8000/api/rooms/?name=Sala%2003
```


#### Agendamento

Listagem de agendamentos:

```bash
curl -X GET http://127.0.0.1:8000/api/scheduling/
```

Criação de agendamento:

```bash
curl -X POST  http://127.0.0.1:8000/api/scheduling/  -H "Authorization: Token cff0071b78232725662b7726c5de2809c90749d5"  -H "Content-Type:application/json"  -d '{"start_date": "2018-11-12T08:00:00", "end_date": "2018-11-12T10:00:00", "username": "teste", "email": "teste@teste.com", "room": 3}'
```

Atualização de sala:

```bash
curl -X PUT  http://127.0.0.1:8000/api/scheduling/11/  -H "Authorization: Token cff0071b78232725662b7726c5de2809c90749d5"  -H "Content-Type:application/json"  -d '{"start_date": "2018-11-12T08:00:00", "end_date": "2018-11-12T10:00:00", "username": "teste2", "email": "teste@teste.com", "room": 3}'
```

Remoção da sala:

```bash
curl -X DELETE  http://127.0.0.1:8000/api/scheduling/11/  -H "Authorization: Token cff0071b78232725662b7726c5de2809c90749d5"
```

Filtros:

Campos disponivéis id, username, email e start_date, end_date e check_schedules.

Quando o campo check_schedules, start_date e end_date são usados no mesmo filtro é verificado se naquele intervalo
possue alguma reunião acontecendo ou preste a acontece.

```bash
curl -X GET http://127.0.0.1:8000/api/scheduling/?username=fulano
curl -X GET http://127.0.0.1:8000/api/scheduling/?check_schedules=true&start_date=2018-11-01T08:00:00&end_date=2018-11-02T10:00:00
```

### Web

Sala

Início › Sala › Salas 

<img src="doc/images/scheduling.png">

Agendamento

Início › Sala › Agendamentos 

<img src="doc/images/room.png">

Token

Início › Token de autenticação › Tokens 

<img src="doc/images/token.png">

## Log

Todos os logs de consulta da API são salvos no banco de dados, seu acesso pode se feito por query ou pela interface web.

Web

Início › REST Framework Tracking › API Request Logs 

<img src="doc/images/loggers.png">

Database

docker-compose exec --user postgres db psql -d django

```sql
-- Dentro do container db
select * from django_admin_log;
```

## Testes

Os testes cobrem todas as etapas da API.

Arquivo com os testes app/room/tests.py

```bash
docker-compose exec web sh 
# Dentro do container web
python manage.py test
```
