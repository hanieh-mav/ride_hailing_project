class RuntimeConfig:
    DATABASE_DRIVER_NAME: str = ''
    DATABASE_USERNAME: str = ''
    DATABASE_PASSWORD: str = ''
    DATABASE_HOST: str = ''
    DATABASE_PORT: int = 0
    DATABASE_NAME: str = ''
    DATABASE_POOL_SIZE: int = 0
    DATABASE_MAX_OVERFLOW: int = 0

    CACHE_HOST: str = ''
    CACHE_PORT: int = 0
    CACHE_DB_NUMBER: int = 0

    FLASK_HOST: str = ''
    FLASK_PORT: int = 0

    KAFKA_BROKERS_LIST: list[str] = ['']
    KAFKA_USER_NAME: str = ''
    KAFKA_PASSWORD: str = ''
    KAFKA_CERT_PEM: str = ''
    KAFKA_TOPIC: str = ''
