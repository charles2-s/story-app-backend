from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from models import Story, User, Comment, Like
from schemas import StoryCreate, StoryUpdate, CommentCreate
from datetime import datetime

def create_story(db: Session, story: StoryCreate, user: User):
    try:
        db_story = Story(
            title=story.title,
            content=story.content,
            owner_id=user.id
        )
        db.add(db_story)
        db.commit()
        db.refresh(db_story)
        return db_story
    except Exception as e:
        db.rollback()
        print(f"Error creating story: {e}")
        raise

def get_stories(db: Session):
    return db.query(Story).options(
        joinedload(Story.likes),
        joinedload(Story.comments)
    ).order_by(Story.id.desc()).all()

def get_story(db: Session, story_id: int):
    return db.query(Story).options(
        joinedload(Story.owner),
        joinedload(Story.comments).joinedload(Comment.author),
        joinedload(Story.likes)
    ).filter(Story.id == story_id).first()

def update_story(db: Session, story_id: int, story_update: StoryUpdate, user: User):
    db_story = db.query(Story).filter(
        and_(Story.id == story_id, Story.owner_id == user.id)
    ).first()

    if not db_story:
        return None

    update_data = story_update.model_dump(exclude_unset=True)
    if update_data:
        update_data['updated_at'] = datetime.utcnow()
        for field, value in update_data.items():
            setattr(db_story, field, value)

    db.commit()
    db.refresh(db_story)
    return db_story

def delete_story(db: Session, story_id: int, user: User):
    db_story = db.query(Story).filter(
        and_(Story.id == story_id, Story.owner_id == user.id)
    ).first()

    if not db_story:
        return False

    db.delete(db_story)
    db.commit()
    return True

def create_comment(db: Session, story_id: int, comment: CommentCreate, user: User):
    try:
        db_comment = Comment(
            content=comment.content,
            author_id=user.id,
            story_id=story_id
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        db.rollback()
        print(f"Error creating comment: {e}")
        raise

def get_comments_for_story(db: Session, story_id: int):
    return db.query(Comment).options(joinedload(Comment.author)).filter(
        Comment.story_id == story_id
    ).order_by(Comment.created_at.asc()).all()

def delete_comment(db: Session, comment_id: int, user: User):
    db_comment = db.query(Comment).filter(
        and_(Comment.id == comment_id, Comment.author_id == user.id)
    ).first()

    if not db_comment:
        return False

    db.delete(db_comment)
    db.commit()
    return True

def like_story(db: Session, story_id: int, user: User):
    # Check if user already liked this story
    existing_like = db.query(Like).filter(
        and_(Like.story_id == story_id, Like.user_id == user.id)
    ).first()

    if existing_like:
        return None  # Already liked

    try:
        db_like = Like(
            user_id=user.id,
            story_id=story_id
        )
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like
    except Exception as e:
        db.rollback()
        print(f"Error liking story: {e}")
        raise

def unlike_story(db: Session, story_id: int, user: User):
    db_like = db.query(Like).filter(
        and_(Like.story_id == story_id, Like.user_id == user.id)
    ).first()

    if not db_like:
        return False  # Not liked

    db.delete(db_like)
    db.commit()
    return True

def has_user_liked_story(db: Session, story_id: int, user_id: int):
    return db.query(Like).filter(
        and_(Like.story_id == story_id, Like.user_id == user_id)
    ).first() is not None