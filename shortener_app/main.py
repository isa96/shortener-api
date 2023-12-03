import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .config import get_settings
from .database import SessionLocal, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    """ Get a database session """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """ Get the admin info for a URL """

    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration page", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))

    return db_url

def raise_bad_request(message: str):
    """ Raise a bad request exception """

    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    """ Raise a not found exception """

    message = f"URL '{request.url}' not found"

    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root():
    """ Root endpoint """

    return "Welcome to ammf.at URL shortener ^^/"

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """ Create a new URL """

    if not validators.url(url.target_url):
        raise_bad_request(message="The provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)

    return get_admin_info(db_url)

@app.get("/{url_key}")
def redirect_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    """ Redirect to the target URL """

    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db, db_url)

        return RedirectResponse(url=db_url.target_url)

    raise_not_found(request)

@app.get(
    "/admin/{secret_key}",
    name="administration page",
    response_model=schemas.URLInfo
)
def get_url_info(
        secret_key: str, request: Request, db: Session = Depends(get_db)    
    ):
    """ Get URL info """

    if db_url := crud.get_db_url_by_secret_key(db, secret_key):
        return get_admin_info(db_url)

    raise_not_found(request)

@app.delete("/admin/{secret_key}")
def delete_url(
        secret_key: str, request: Request, db: Session = Depends(get_db)
    ):
    """ Delete a URL """

    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key):
        message = (
            f"Successfully deleted '{get_admin_info(db_url).url}' "
            f"for '{db_url.target_url}'"
        )

        return {"detail": message}
    
    raise_not_found(request)
