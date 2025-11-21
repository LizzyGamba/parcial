from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from Backend import models, schemas, crud, security
from Backend.database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from Backend.gemini_client import analyze_sentiment

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UserResponse)
def register_user(data: schemas.UserRegister, db: Session = Depends(get_db)):
    user_db = crud.get_user_by_email(db, data.email)
    if user_db:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = security.hash_password(data.password)
    new_user = crud.create_user(db, data.email, hashed_password)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = security.create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Falta cabecera Authorization")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token inválido")
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user = crud.get_user_by_email(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

@app.post("/reviews", response_model=schemas.ReviewResponse)
async def post_review(
    payload: schemas.ReviewCreate, 
    current_user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    sentiment = await analyze_sentiment(payload.texto_resena)
    rv = crud.create_review(
        db, 
        user_id=current_user.id, 
        producto=payload.producto,
        texto_resena=payload.texto_resena,
        sentimiento=sentiment
    )
    return rv

@app.get("/reviews", response_model=list[schemas.ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(models.Review).order_by(models.Review.created_at.desc()).all()
    return reviews


@app.get("/reviews/{producto}", response_model=list[schemas.ReviewResponse])
def get_reviews(producto: str, db: Session = Depends(get_db)):
    rows = crud.get_reviews_by_producto(db, producto)
    return rows