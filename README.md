### Hexlet tests and linter status:
[![Actions Status](https://github.com/zhukata/Page_analyzer/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/zhukata/Page_analyzer/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/b9aa6036d423b63cc674/maintainability)](https://codeclimate.com/github/zhukata/Page_analyzer/maintainability)

[Page Analyzer](https://page-analyzer-qlcp.onrender.com) – это сайт, который анализирует указанные страницы на SEO-пригодность.

### Technologies Used:

* Backend: Python (Flask framework)

* Database: PostgreSQL

* Task Runner: Poetry

* Web Server: Gunicorn

* Containerization: Docker and Docker Compose

### How to install the app:  
For install and use the application you will need the following applications: 
[git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git),
[poetry](https://python-poetry.org/docs/), 
[postgresql](https://www.postgresql.org/). 
You can install them:  
```
$ sudo apt update
$ sudo apt install git-all  
$ sudo apt install curl
$ curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
```

Clone the application from GitHub and install the necessary
libraries using the 'make install' command.  
All commands starting with '$ make' are executed in the application directory.  
```
$ git clone git@github.com:serVmik/Page_analyzer.git  
$ cd Page_analyzer  
$ make install
$ make shell 
```

Install postgresql:  
```
$ sudo apt install postgresql
```

You need create a user:
```
$ sudo -u postgres createuser --createdb {user_name}  
```

You need to set a password for the user_name.  
```
$ sudo -u postgres psql  
postgres=# ALTER ROLE {user_name} PASSWORD '{password}';
postgres=# \q
```

Create '.env' file in the root folder and add the following variables to it.  
Set the secret key.  
Enter password for user_name.
```  
SECRET_KEY={secret_key}  
DATABASE_URL=postgresql://{user_name}:{password}@localhost:5432/urls
POSTGRES_USER={username}
POSTGRES_PASSWORD={password}
POSTGRES_DB=urls
```  

Run the application with Docker-compose:  
```
$ make docker-compose
```

Go to the browser address http://localhost:8000/  
### How to use the app:  
#### Enter a verified address.
![index_1](https://github.com/zhukata/Page_analyzer/blob/assets/255515125-1410a83a-fd85-4e4a-beb8-e2f8ee7ab3b3.png)
#### Run a check.  
![urls_1](https://github.com/zhukata/Page_analyzer/blob/assets/255515219-e9f7a290-380f-43a7-85ec-ae6b8882b6be.png)
#### Get results.
![urls_2](https://github.com/zhukata/Page_analyzer/blob/assets/255515298-39503faf-41fe-4936-91a6-68aafb190ea0.png)
#### The application saves verified sites.
![urls_3](https://github.com/zhukata/Page_analyzer/blob/assets/255515374-52a36c71-5c0f-4ead-bb4d-e39735f5671d.png)
