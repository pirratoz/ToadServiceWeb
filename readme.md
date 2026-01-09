# Toad Web Service

- A service for automating gaming bots in Telegram chat.

## Deploying a database
1. Installing PostgreSQL
```
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```
2. Log in as postgres
```
sudo -u postgres psql
```
3. Create a new user
```
CREATE USER user_example_THIS WITH PASSWORD 'user_password_THIS';
```
4. Create a database and grant rights
```
CREATE DATABASE db_name_THIS;
GRANT ALL PRIVILEGES ON DATABASE db_toads_THIS TO user_toad_THIS;
```

## Authors

- [@PirraToZ](https://t.me/PirraToZ)

