# Patched for Python 3.12+ compatibility
import importlib
import importlib.util
import pkgutil

def _import_modules():
    package = __name__
    for _, moduleName, _ in pkgutil.iter_modules(__path__):
        # Cek apakah modul tersedia dengan find_spec (pengganti find_module)
        spec = importlib.util.find_spec(f"{package}.{moduleName}")
        if spec is not None:
            importlib.import_module(f"{package}.{moduleName}")

_import_modules()