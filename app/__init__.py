
import time
from concurrent.futures import process

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import api_router
from pydantic_settings import BaseSettings

app=FastAPI(
    title='job_management_eka_group',
    version='1.0.0',
)

app.include_router(api_router)

# midlewware
class MyMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)

        return response


# origin = ["https://be.ekaroup.co", "http://202.149.70.68","http://localhost", "http://localhost:80",
#           "http://127.0.0.1:3000", "202.149.70.68"]

# origin = ["https://be.ekaroup.co",
#           "https://bspnwonosobo.com", "https://bspnwonosobo.com/", "https://localhost:3000"]


# ,"http://localhost:3000","http://127.0.0.1:3000"
origin = ["https://be.ekaroup.co",
          "https://ekagroup.co", "https://ekagroup.co/","http://localhost:3000","http://127.0.0.1:3000"]
app.add_middleware(MyMiddleWare)
app.add_middleware(CORSMiddleware, allow_origins=origin,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)