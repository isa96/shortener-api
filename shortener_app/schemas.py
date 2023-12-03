from pydantic import BaseModel

class URLBase(BaseModel):
    """ Base model for URL """

    target_url: str

class URL(URLBase):
    """ Model for URL """

    is_active: bool
    clicks: int

    class Config:
        """ Config for the model """

        orm_mode = True

class URLInfo(URL):
    """ Model for URL info """

    url: str
    admin_url: str
