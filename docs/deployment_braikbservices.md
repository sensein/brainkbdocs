# Deployment of BrainKB Services

BrainKB consists of multiple service components, as highlighted in the {ref}`brainkb_architecture_figure` All of the service components can be deployed independently. However, there are a few dependencies, such as setting up the PostgreSQL database that is used by JWT Users and Scope Manager, that need to be setup first. 

<b style="color:red;">Note:</b> The installation of Docker is necessary due to its use in deployment.


## Dependencies 

The following are the core dependencies: software and service components that need to be installed in the order specified below.

### JWT User & Scope Manager
The JWT User & Scope Manager helps to simplify the management of permissions and users for API endpoint access. It needs to be setup as a first step in order to use JWT based authentication. 

**Installation:**
- Navigate to `APItokenmanager` directory.
- Install PostgreSQL databse by running the Docker Compose file present inside _docker-postgresql_ folder.
	- **Important:** You need to create an `.env` file to hold the following information.

		- POSTGRES_USER: PostgreSQL database user name.
		- POSTGRES_PASSWORD: Password for PostgreSQL database user.
		- POSTGRES_DB: Database name.
		- PGADMIN_DEFAULT_EMAIL: Email address for [pgAdmin](https://www.pgadmin.org).  
		- PGADMIN_DEFAULT_PASSWORD: Password for pgAdmin user.
	- Additionally, set the following environment variables in `.env` files for Django that are required to create Django superuser.
		- DJANGO_SUPERUSER_USERNAME: Username that you will use to login to JWT User & Scope Manager.
		- DJANGO_SUPERUSER_EMAIL: Email address of the user.
		- DJANGO_SUPERUSER_PASSWORD: Password of the Django superuser.
- Assign the environment variables specified below and deploy the application by executing the Docker Compose file, selecting either development (`docker-compose-dev.yml`) or production (`docker-compose-prod.yml`) depending on your environemnt.
	- DB_NAME: Name of the database.
	- DB_USER: User name.
	- DB_PASSWORD: Password.
	- DB_HOST: Database connection URL, default is localhost.
	- DB_PORT: Database port number, default is 5432.

Upon successful deployment, you should following home screen as shown in {numref}`jwtuserhome` and manage users and permissions (see {numref}`jwtuserupdateinfo`).

```{figure} jwtuserhome.png
:name: jwtuserhome
JWT User & Scope Manager landing page.
```

```{figure} jwtuserupdateinfo.png
:name: jwtuserupdateinfo
JWT User & Scope Manager - Updating user information.
```

### RabbitMQ
RabbitMQ is an open-source messaging broker software that is used in the ingestion process. Other microservices, i.e., workers, then consume the data that RabbitMQ holds in the messaging queue. 

**Installation:**
- Navigate to `rabbit-mq` directory.
- Run the `docker-compose.yml`, issuing `docker compose up` command.
	- **Important:** You need to create an `.env` file and provide the following information.
	- RABBITMQ_DEFAULT_USER: Username for the RabbitMQ that will be use to login.
	- RABBITMQ_DEFAULT_PASS: Password for the RabbitMQ.
- After successful deployment, you should be able to see the screen shown in {numref}`rabbitmqlogin`. Use the username and password specified earlier to login. 
```{figure} rabbitmqlogin.png
:name: rabbitmqlogin
RabbitMQ after successful deployment.
``` 
### GraphDB
We use GraphDB to store our KGs. 

**Installation:**
- Navigate to `graphdb` directory.
- Run the `docker-compose.yml`, issuing `docker compose up` command. After successful deployment, you should be able to see the following screen (see {numref}`graphdbwelcome`). 

```{figure} graphdb.png
:name: graphdbwelcome
GraphDB Screen.
``` 
- Access to the GraphDB is available to all users by default. To enable password based access, navigate to setup `→` users and access and enable security (see {numref}`setaccesscontrol`).

```{figure} setaccesscontrol.png
:name: setaccesscontrol
Enabling Access Control.
``` 

### Query Service
The query service provides the endpoints and the functionalities necessary for querying (and updating) the knowledge graphs from the graph database.

- Navigate to `query_service` directory.
- Run either `docker-compose-dev.yml` or `docker-compose-prod.yml` depending on your environment, issuing `docker compose up` command.
	- **Important:** You need to create an environment file `.env.development` to hold the following information.
	- ENV_STATE: The state, either, environment and production. Use `prod` for production.
	- DATABASE_URL: Use `sqlite:///data.db`.
	- LOGTAIL_API_KEY: [Log Tail](https://betterstack.com) API key. {numref}`logtaildemo` shows the logging of the information. 
	- JWT_POSTGRES_DATABASE_HOST_URL: PostgreSQL database (`the same database from JWT User & Scope Manager`) URL.
	- JWT_POSTGRES_DATABASE_NAME: Database name.
	- JWT_POSTGRES_DATABASE_PORT: Port number of the PostgreSQL database.
	- JWT_POSTGRES_DATABASE_USER: Username for the PostgreSQL database.
	- JWT_POSTGRES_DATABASE_PASSWORD: Password for PostgreSQL database user.
	- JWT_POSTGRES_TABLE_USER: Name of the table to store the user information. The default is `Web_jwtuser`.
	- JWT_POSTGRES_TABLE_SCOPE: Name of the table to store the scope (or permission) information. The default is `Web_scope`.
	- JWT_POSTGRES_TABLE_USER_SCOPE_REL: Name of the table to store the relationship information between scope (or permissions) and user. The default is `Web_jwtuser_scopes`.
	- JWT_ALGORITHM: Algorithm to be used in JWT. The default is `HS256`.
	- JWT_SECRET_KEY: Secret key to be used in JWT.
	- GRAPHDATABASE_USERNAME: Username for the graph database, i.e., `GraphDB` in our case.
	- GRAPHDATABASE_PASSWORD: GraphDB password. 
	- GRAPHDATABASE_HOSTNAME: Hostname for the graph database. Default is `http://localhost`.
	- GRAPHDATABASE_PORT: Graph database port number. Default is `7200`.
	- GRAPHDATABASE_TYPE: Graph database type. Default is `GRAPHDB`, representing `GraphDB`. 
	- GRAPHDATABASE_REPOSITORY: The name of the repository (same as table in relational database). This may not be use in all graphdatabase but for GraphDB, which we use, it is a must.

```{figure} logtaildemo.png
:name: logtaildemo
[Snapshots of the BrainKB logs from Log Tail](https://betterstack.com).
``` 

<b style="color:red;">Note:</b>

