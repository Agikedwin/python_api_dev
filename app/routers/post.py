from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import  models, schemas, auth2
from .. database import get_db
from sqlalchemy.orm import  Session
from  sqlalchemy import func
from typing import  List, Optional


router = APIRouter(
    prefix="/post", tags=['Post']
)

@router.get("/", response_model=List[schemas.PostOut])
def root(db: Session = Depends(get_db),current_user: int = Depends(auth2.get_current_user), limit: int =100, skip: int = 0, search: Optional[str] = ""):
    #Get user specific
    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    #get all posts
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).
              filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())
    return result
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user) ):
    #new_post = post.dict()
    #new_post['id'] = randrange(0,1000)
    #my_post.append(new_post)
    #print(my_post)
    #use **to unpack the post dict
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/{id}",  response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db) , current_user: int = Depends(auth2.get_current_user) ):
    #post = find_post(int(id))
    #post =  db.query(models.Post).filter(models.Post.id==id).first()

    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).
            filter(models.Post.id==id).first())
    print('-------------------------------------------------------------------------------------------')
    print(post)
    print('-------------------------------------------------------------------------------------------')


    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with  Id {id} not found")
        #response.status_code= status.
        #return  {'message': f"Post Id :{id} not found"}

    #if post.Post.owner_id != current_user.id:
    #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform the requested action")

    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db) , current_user: int = Depends(auth2.get_current_user) ):
    #index = find_index_post(int(id))
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with if {id} does not exits")
    #my_post.pop(index)
    # return nothing after deletion

    if post.owner_id != current_user.id:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform the requested action")

    post_query.delete(synchronize_session = False)
    db.commit()
    return  Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",  response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db),current_user: int = Depends(auth2.get_current_user)):
    #print(post)
    #index = find_index_post(int(id))
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with if {id} does not exits")

    if post.owner_id != current_user.id:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform the requested action")

    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_post[index] = post_dict
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()