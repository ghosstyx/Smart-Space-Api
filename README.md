# Smart-Space-Api

### Setup

Clone the repository:
```sh
$ git clone https://github.com/azizbek-kobilov/smart-space-backend.git
$ cd smart-space-backend
```

Create a virtual environment:
```sh
$ python -m venv env
$ source env/bin/activate
```

Install the dependencies:
```sh
(env)$ pip install -r requirements.txt
```

In the root of the project create a .env file and set the environment variables
```sh
ENVIRONMENT = 'production'
# Django Secret Key
SECRET_KEY = 
# Database configs
DB_NAME =
DB_USERNAME =
DB_PASSWORD =
DB_HOSTNAME =
DB_PORT =
```

Migrate database:
```sh
(env)$ python manage.py migrate
```

Create superuser:
```sh
(env)$ python manage.py createsuperuser
```

Run project:
```sh
(env)$ python manage.py runserver
```
>>>>>>> ef00b60 (Первый коммит)
