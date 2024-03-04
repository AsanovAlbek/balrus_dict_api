import uvicorn
from fastapi import FastAPI
from database.database import Base, engine
from api import router

app = FastAPI()
app.include_router(router.routers)
#Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080, reload=True, workers=4)