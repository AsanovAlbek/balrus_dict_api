import uvicorn
from fastapi import FastAPI
from database.database import Base, engine
from api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router.routers)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
   allow_credentials = True,
   allow_methods = ["*"],
   allow_headers = ["*"],
   max_age = 60
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='192.168.177.2', port=8000, reload=True, workers=4)