import uvicorn
from fastapi import FastAPI
from database.database import Base, engine
from api import router

app = FastAPI()
app.include_router(router.routers)

if __name__ == '__main__':
    uvicorn.run('main:app', host='192.168.177.2', port=8000, reload=True, workers=4)