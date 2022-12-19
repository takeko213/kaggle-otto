# ref : https://k-ptl.hatenablog.com/entry/2021/02/25/Python%E3%81%AE%E5%A4%89%E6%95%B0%E7%A9%BA%E9%96%93%E6%B1%9A%E6%9F%93%E3%81%A8%E3%81%AE%E6%88%A6%E3%81%84%E3%83%BB%E5%AE%8C%E7%B5%90%E7%B7%A8_~_noglobal

from functools import partial
import inspect
from typing import List, Dict, Optional, Callable, Any
from types import FunctionType


def globals_with_module_and_callable(globals_: Optional[Dict[str, Any]] = None,
                                     excepts: Optional[List[str]] = None) -> Dict[str, Any]:
    def need(name, attr):
        if name in excepts:
            return True
        if inspect.ismodule(attr):
            return True
        if callable(attr):
            return True
        return False

    if globals_ is None:
        globals_ = globals()
    if excepts is None:
        excepts = []
    filtered_globals = {
        name: attr
        for name, attr in globals_.items()
        if need(name, attr)
    }
    
    if not inspect.ismodule(globals_["__builtins__"]):
        for name, attr in globals_["__builtins__"].items():
            if need(name, attr): filtered_globals[name] = attr
    
    return filtered_globals


def bind_globals(globals_: Dict[str, Any]) -> Callable:
    def _bind_globals(func: FunctionType) -> FunctionType:
        bound_func = FunctionType(code=func.__code__,
                                  globals=globals_,
                                  name=func.__name__,
                                  argdefs=func.__defaults__,
                                  closure=func.__closure__,
                                  )
        return bound_func
    return _bind_globals


def no_global_variable_decorator(globals_: Optional[Dict[str, Any]] = None):
    partialled = partial(globals_with_module_and_callable, globals_=globals_)

    def _no_global_variable(excepts: Optional[List[str]] = None):
        partialled_globals_ = partialled(excepts=excepts)
        bound_func = bind_globals(globals_=partialled_globals_)
        return bound_func

    return _no_global_variable

global noglobal
class noglobal:
    def __init__(self, excepts=None):
        self.excepts = excepts
    
    def __call__(self, _func):
        return no_global_variable_decorator(
            globals_=_func.__globals__
          )(excepts=self.excepts # arg of _no_global_variable
          )(func=_func)          # arg of _bind_globals 