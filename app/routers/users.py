
from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import  get_db

router = APIRouter(
    prefix="/users",
    tags=['users']
)



@router.post("/",status_code= status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password
    hashed_password = utils.hash(user.password)
    print(hashed_password)
    utils.verify(user.password, hashed_password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with {id} not found")
    return user