"""
Potential base for a webhook receiver. Unused to prefer a query-based approach local
"""

from contextlib import asynccontextmanager
from typing import Optional

import dropbox
import fastapi

from constants import DROPBOX_ACCESS_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET

dbx: Optional[dropbox.Dropbox] = None


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    dbx = dropbox.Dropbox(
        DROPBOX_ACCESS_TOKEN, app_key=DROPBOX_APP_KEY, app_secret=DROPBOX_APP_SECRET
    )
    yield
    dbx.close()


app = fastapi.FastAPI(lifespan=lifespan)


@app.post("monzo")
def monzo():
    pass
