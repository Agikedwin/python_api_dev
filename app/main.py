
from fastapi import FastAPI

from app.database import engine
from app import  models
from  app.routers import  post, user, auth, vote
from  app.config import settings

models.Base.metadata.create_all(engine)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get('/')
def root_user():
    return {'message':'This is a default message'}



"""

my_post = [{"title": "Lakes", "content": "Beautiful lakes", "id": 2}]

def find_post(id):
    for p  in my_post:
        if p['id'] == id:
            return  p

def find_index_post(id):

    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

"""
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




