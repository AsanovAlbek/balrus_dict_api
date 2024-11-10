from fastapi_mail import ConnectionConfig

mailconf = ConnectionConfig(
    MAIL_USERNAME="dictonary_inform@intigris.ru",
    MAIL_PASSWORD="Asdf0886",
    MAIL_FROM="dictonary_inform@intigris.ru",
    MAIL_PORT=587,
    MAIL_SERVER="mail.nic.ru",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)