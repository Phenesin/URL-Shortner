from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
import validators
import models, schemas, database, crud
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from config import get_settings







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


def get_admin_info(db_url : models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for("administration info", secret_key = db_url.secret_key)
    db_url.url = str(base_url.replace(path = db_url.key))
    db_url.admin_url = str(base_url.replace(path = db_url.secret_key))
    return db_url

@app.get("/")
async def read_root():
    return "Welcome to URL Shortner"


@app.post("/url", response_model = schemas.URLInfo)
async def create_url(url : schemas.URLBase, db : Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid")
    db_url = crud.create_db_url(db = db, url = url)
    return get_admin_info(db_url)





@app.get('/return_all/')
async def all_entries(db : Session = Depends(get_db)):
    db_url = db.query(models.URL).all()
    return db_url





@app.get("/admin/{secret_key}", name = "administration info", response_model = schemas.URLInfo)
async def get_url_info(secret_key : str, request : Request, db : Session = Depends(get_db)):
    if db_url := crud.get_url_by_secret_key(db, secret_key = secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)



@app.delete("/admin/{secret_key}")
async def delete_url(secret_key : str, request : Request, db : Session = Depends(get_db)):
    if db_url := crud.deactivate_url_by_secret_key(db, secret_key = secret_key):
        message = f"Successfully deleted shortened URL for {db_url.target_url}"
        return {"detail" : message}
    else:
        raise_not_found(request)






@app.get("/{url_key}")
async def forward_to_target_url(url_key : str, request : Request, db : Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first()
    if db_url:= crud.check_unique_key(db = db, url_key = url_key):
        crud.update_db_clicks(db = db, db_url = db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

    return db_url