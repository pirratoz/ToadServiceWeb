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

## JWT Auth
1. Generating a private key
```
openssl genrsa -out jwt-private.pem 2048
```
2. Generating a public key
```
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```


## Authors

- [@PirraToZ](https://t.me/PirraToZ)

