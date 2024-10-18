import os


class BaseConfig:
    PROPAGATE_EXCEPTIONS = True


class DevelopConfig(BaseConfig):
    WEATHER_API_KEY=os.getenv("WEATHER_API_KEY")
