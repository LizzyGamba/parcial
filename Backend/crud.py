from sqlalchemy.orm import Session
from Backend.models import User, Review
from Backend.security import verify_password

def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db, email: str, hashed_password: str):
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_review(db: Session, user_id: int, producto: str, texto_resena: str, sentimiento: str):
    review = Review(
        producto=producto,
        texto_resena=texto_resena,
        sentimiento=sentimiento,
        user_id=user_id
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews_by_producto(db: Session, producto: str):
    return (
        db.query(Review)
        .filter(Review.producto == producto)
        .order_by(Review.created_at.desc())
        .all()
    )

def get_all_reviews(db: Session):
    return (
        db.query(Review)
        .order_by(Review.created_at.desc())
        .all()
    )
    
    