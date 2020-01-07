import importlib


def lazy_load_class(module_name):
    loaded_module = importlib.import_module(module_name)

    return loaded_module
