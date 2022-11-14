from fastapi import  Depends, HTTPException, status, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from ..import schemas, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/")
def vote( vote: schemas.Vote , db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    
    print(f"voting on post {vote.post_id} user {current_user.id}")
    #validate post id
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {vote.post_id} not found") 

    
    v = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id and models.Vote.user_id == current_user.id).first()

    #user already voted 
    if v != None:
        raise HTTPException(status.HTTP_412_PRECONDITION_FAILED, f"Vote found use delete for deleting")
    
    # create vote
    print(f"creating vote  on post {vote.post_id} user {current_user.id}")
    new_vote = models.Vote(**vote.dict())
    new_vote.user_id = current_user.id
    db.add(new_vote)
    db.commit()
    return{"thanks for voting"}

@router.delete("/")
def vote(vote: schemas.Vote , db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    print(f"deleting vote on post {vote.post_id} user {current_user.id}")
     #validate post id
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with {vote.post_id} not found") 

    # validate vote exist

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id and models.Vote.user_id == current_user.id)
    v = vote_query.first()

    if v == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Vote for post  not found") 

    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"vote deleted"}


