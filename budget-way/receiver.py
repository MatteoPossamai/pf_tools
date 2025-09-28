from contextlib import asynccontextmanager
from typing import Optional

import dropbox
import fastapi

from constants import ACCESS_TOKEN, TRANSACTIONS_FILE_PATH, APP_KEY, APP_SECRET

dbx: Optional[dropbox.Dropbox] = None


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    dbx = dropbox.Dropbox(ACCESS_TOKEN, app_key=APP_KEY, app_secret=APP_SECRET)
    yield
    dbx.close()


app = fastapi.FastAPI(lifespan=lifespan)


@app.post("monzo")
def monzo():
    pass
