import importlib


def lazy_load_class(app_name):
    loaded_module = importlib.import_module(mudule_name)

    return loaded_module
