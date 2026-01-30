from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
import validators
import models, schemas, database, crud
from sqlalchemy.orm import Session





app = FastAPI()
models.Base.metadata.create_all(bind = database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    raise HTTPException(status_code = 400, detail = message)


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code = 404, detail = message)






@app.post("/url", response_model = schemas.URLInfo)
async def create_url(url : schemas.URLBase, db : Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid")
    db_url = crud.create_db_url(db = db, url = url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    return db_url






@app.get("/{url_key}")
async def forward_to_target_url(url_key : str, request : Request, db : Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first()
    if db_url:= crud.check_unique_key(db = db, url_key = url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)











@app.get("/")
async def read_root():
    return "Welcome to URL Shortner"