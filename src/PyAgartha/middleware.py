from typing import Callable, List, Any, Optional

class Middleware:
    def __init__(self):
        self.b4_req: List[Callable[..., Any]] = []
        self.after_req: List[Callable[..., Any]] = []
        
    def add_b4(self, func: Callable[..., Any]) -> None:
        self.b4_req.append(func)
    
    def add_after(self, func: Callable[..., Any]) -> None:
        self.after_req.append(func)
        
    def b4(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.add_b4(func)
        return func
    
    def after(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.add_after(func)
        return func
    
    def execute_b4(self, request) -> Optional[Any]:
        for func in self.b4_req:
            res =  self._call(func, request)
            if res is not None:
                return res
        return None
                
    def execute_after(self, request, response) -> Any:
        current = response
        for func in self.after_req:
            res = self._call(func, request, current)
            if res is not None:
                current = res
        return current
    
    def _call(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        result = func(*args, **kwargs)
        return result