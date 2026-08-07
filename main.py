from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from database import Base, engine, get_db
import models
import schemas
from auth import hash_password, verify_password, create_access_token
from fastapi import UploadFile, File, Form
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_current_user
from typing import List,Optional

import cloudinary.uploader
from cloudinary_config import cloudinary

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Notes platform is running"}


@app.post("/signup")
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):    #schemas.usercreate will validate user data db will store databse session
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first() #check whether this user already signedup
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password) #password is stored after hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #databse se latest data vapas le aoo here will be auto genertsed user id needed

    return {"message": "User created successfully", "user_id": new_user.id}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
 
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
 
    access_token = create_access_token(data={"sub": user.email})
 
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@app.get("/me")
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


# folder jaha files save hongi
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # agar folder na ho toh khud bana lega

@app.post("/upload")
def upload_resource(
    title: str = Form(...),
    subject: str = Form(...),
    semester: int = Form(...),
    resource_type: str = Form(...),
    year: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # file ko seedha Cloudinary pe upload karo (local save nahi karna ab)
    upload_result = cloudinary.uploader.upload(
         file.file,
         resource_type="raw",
         folder="notes_platform",
         public_id=file.filename,
         use_filename=True,
       unique_filename=False
    )

    file_url = upload_result["secure_url"]  # yeh Cloudinary ka permanent link hai


    # database mein entry banao
    new_resource = models.Resource(
        title=title,
        subject=subject,
        semester=semester,
        resource_type=resource_type,
        year=year,
        file_url=file_url,
        uploader_id=current_user.id
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return {"message": "Resource uploaded successfully", "resource_id": new_resource.id}

@app.get("/resources", response_model=List[schemas.ResourceOut])
def get_resources(
    semester: Optional[int]  = None,
    subject:Optional[str]= None,
    resource_type: Optional[str]  = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Resource)

    if semester is not None:
        query = query.filter(models.Resource.semester == semester)

    if subject is not None:
        query = query.filter(models.Resource.subject.ilike(subject))

    if resource_type is not None:
        query = query.filter(models.Resource.resource_type.ilike(resource_type))

    resources = query.all()
    return resources


@app.get("/resources/{resource_id}/download")
def download_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()

    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    return RedirectResponse(url=resource.file_url)