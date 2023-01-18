import os

from dotenv import find_dotenv, load_dotenv

from typing import Any


class BaseConfig:

    @classmethod
    def configure(cls, config_class: Any):
        config_classes: set = set(config_class.__bases__)
        config_classes.add(config_class)
        for config_class_ in config_classes:
            cls.__find_value_and_set_in_class(config_class_)

    @staticmethod
    def __find_value_and_set_in_class(config_class: Any):
        load_dotenv(find_dotenv())
        for attr_name in dir(config_class):
            if attr_name.startswith("__") or callable(getattr(config_class, attr_name)):
                continue
            if env_value := os.getenv(attr_name):
                class_value = getattr(config_class, attr_name)
                if isinstance(class_value, str):
                    setattr(config_class, attr_name, env_value)
                else:
                    setattr(config_class, attr_name, eval(env_value))