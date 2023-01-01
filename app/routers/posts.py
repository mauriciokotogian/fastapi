

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


#@router.get("/", response_model=List[schemas.PostOut])
@router.get("/")
def get_posts(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user), 
              limit: int = 10,
              skip: int = 0, 
              search: Optional[str]=""):
   
   # with connection to database
   # cursor.execute(""" select * from posts""")
   # posts = cursor.fetchall()
   # return {"data": posts} 

    # with orm


    # fetch the votes asociated
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()


    return results

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    
   # sql connection
    # cursor.execute(""" select * from posts p where p.id = %s  """,(str(id)))
    # target = cursor.fetchone()
    # if target == None:
    #    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found") 

    # return {"data":target}

    # sqlalechemy orm
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post

    """   for post in my_posts:
        if post['id'] == id:
            return post
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found") """

#status_code is the default status in the response
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # with connection to database
    # cursor.execute(""" insert into posts(title, content, published) values(%s,%s,%s) returning *""",
    # (post.title,post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data":new_post}

    # with sqlalchemy
    print("creating post..")
    print(f"user {current_user.email} ")
    new_post=models.Post(**post.dict())
    new_post.owner_id=current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    """   post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict) 
    return {"data":post_dict}  """




@router.delete("/{id}", response_model=schemas.PostResponse)
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    #sql connection
    #cursor.execute(""" delete from posts where id = %s""",(str(id)))
    #deleted = cursor.fetchone()
    # conn.commit()
    #if deleted == None:
    #    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found")


    # sqlalchemy orm
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if(post_query.first() == None):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found")

    post = post_query.first() 
    #validate the user is deleting a post that belongs to the user
    if current_user.id == post.owner_id: 
         post_query.delete(synchronize_session=False)
         db.commit()
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Post with {id} not deleted") 

    """  for post in my_posts:
        if post['id'] == id:
            my_posts.remove(post)
            return {"message": f" post with {id} is deleted"}
           
     raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found") """

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    #sql connection
    #cursor.execute(""" update posts set title =%s, content=%s, published=%s where id = %s returning *""", (post.title,post.content, post.published,id))
    #updated = cursor.fetchone()
    #conn.commit()
    #if updated == None:
     #    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found")

    # sql alchemy
    query = db.query(models.Post).filter(models.Post.id==id)
    p = query.first()

    if p == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found")
    
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    post_updated = query.first()
    return post_updated

    """  post_dict = post.dict()
     for p in my_posts:
        if p['id'] == id:
            my_posts.remove(p)
            my_posts.append(post_dict)
            return {"data":post_dict}
     raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {id} not found")

 """
