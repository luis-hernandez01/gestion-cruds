# from starlette.middleware.base import BaseHTTPMiddleware
# from fastapi import Request

# class SchemaMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Ej: /actividades/Waira/all -> ["actividades", "Waira", "all"]
#         path_parts = request.url.path.strip("/").split("/")

#         if len(path_parts) >= 2:
#             request.state.schema = path_parts[1]
#         else:
#             request.state.schema = None

#         response = await call_next(request)
#         return response




from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class SchemaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ej: /Waira/actividades/all -> ["Waira", "actividades", "all"]
        path_parts = request.url.path.strip("/").split("/")

        if len(path_parts) >= 1:
            request.state.schema = path_parts[0]
        else:
            request.state.schema = None

        response = await call_next(request)
        return response