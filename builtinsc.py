# builtins.py
from typesys import Number, String, Bool, Nil

class CallError(Exception):
    pass

# Constantes por defecto
consts = {
    "true": True,
    "false": False,
    "nil": None,
}

# Funciones incorporadas
def _print(interp, *args):
    print(*args, end="")
    return None

def _input(interp):
    return input()

def _len(interp, value):
    try:
        return len(value)
    except Exception:
        raise CallError("len() solo se puede usar con cadenas o listas")

# Diccionario de funciones integradas
builtins = {
    "print": _print,
    "input": _input,
    "len": _len,
}