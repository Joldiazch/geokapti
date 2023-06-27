from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.infrastructure.database import create_db
from app.api.routers import location_router, auth_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event("startup")
async def startup_event():
    create_db()

@app.get("/", include_in_schema=False)
def read_root():
    """
    redirect to Autodocumentation.
    """
    return RedirectResponse('/docs')


# include routers
app.include_router(location_router)
app.include_router(auth_router)


""" # Endpoint protegido que requiere autenticación
@app.get("/secure_endpoint")
def secure_endpoint(user: User = Depends(get_current_user)):
    return {"message": f"Hello, {user.username}! This is a secure endpoint."}


# Endpoint para obtener un token de acceso
@app.post("/token")
def login_for_access_token(data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_session)):
    username = data.username
    password = data.password

    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
def register_user(data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_session)):
    username = data.username
    password = data.password

    if get_user(db, username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"} """


if __name__ == '__main__':
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)