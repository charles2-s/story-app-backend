from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db, get_current_user, get_current_user_optional
from crud import (
    create_story, get_stories, get_story, update_story, delete_story,
    create_comment, get_comments_for_story, delete_comment,
    like_story, unlike_story, has_user_liked_story
)
from schemas import StoryCreate, StoryUpdate, Story, CommentCreate, Comment, LikeResponse
from models import User

router = APIRouter()

@router.post("/")
def create_story_endpoint(story: StoryCreate,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    created_story = create_story(db, story, user)
    return {"id": created_story.id, "title": created_story.title, "content": created_story.content, "owner_id": created_story.owner_id}

@router.get("/")
def read_stories(db: Session = Depends(get_db)):
    stories = get_stories(db)
    return [{"id": s.id, "title": s.title, "content": s.content, "owner_id": s.owner_id, "likes_count": len(s.likes) if s.likes else 0, "comments_count": len(s.comments) if s.comments else 0} for s in stories]

@router.get("/{story_id}", response_model=Story)
def read_story(story_id: int, db: Session = Depends(get_db)):
    story = get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    story.likes_count = len(story.likes) if story.likes else 0
    return story

@router.put("/{story_id}", response_model=Story)
def update_story_endpoint(story_id: int,
                         story_update: StoryUpdate,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    updated_story = update_story(db, story_id, story_update, user)
    if not updated_story:
        raise HTTPException(status_code=404, detail="Story not found or not authorized")
    updated_story.likes_count = len(updated_story.likes) if updated_story.likes else 0
    return updated_story

@router.delete("/{story_id}")
def delete_story_endpoint(story_id: int,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    success = delete_story(db, story_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Story not found or not authorized")
    return {"message": "Story deleted successfully"}

# Comment endpoints
@router.post("/{story_id}/comments", response_model=Comment)
def create_comment_endpoint(story_id: int,
                           comment: CommentCreate,
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    # Check if story exists
    story = get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    created_comment = create_comment(db, story_id, comment, user)
    # Reload with author relationship
    db.refresh(created_comment)
    return created_comment

@router.get("/{story_id}/comments", response_model=list[Comment])
def read_comments(story_id: int, db: Session = Depends(get_db)):
    # Check if story exists
    story = get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return get_comments_for_story(db, story_id)

@router.delete("/comments/{comment_id}")
def delete_comment_endpoint(comment_id: int,
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    success = delete_comment(db, comment_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    return {"message": "Comment deleted successfully"}

# Like endpoints
@router.post("/{story_id}/like", response_model=LikeResponse)
def like_story_endpoint(story_id: int,
                       db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    # Check if story exists
    story = get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    like = like_story(db, story_id, user)
    if not like:
        raise HTTPException(status_code=400, detail="Story already liked")
    return like

@router.delete("/{story_id}/like")
def unlike_story_endpoint(story_id: int,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    success = unlike_story(db, story_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"message": "Story unliked successfully"}

@router.get("/{story_id}/like")
def check_like_status(story_id: int,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user_optional)):
    # Check if story exists
    story = get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if not user:
        return {"liked": False}

    liked = has_user_liked_story(db, story_id, user.id)
    return {"liked": liked}



