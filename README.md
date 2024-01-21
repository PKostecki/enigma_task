## To install project:
1. Create venv
2. Run `make init`

## Run project
1. Set your own environment variables like email in `.env`. Listed below:
```
    EMAIL_HOST = 
    EMAIL_PORT = 
    EMAIL_USE_TLS = 
    EMAIL_HOST_USER = 
    EMAIL_HOST_PASSWORD = 
```
2. Run `make run`
3. Remember that you need Redis and Celery.