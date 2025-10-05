"""
Utilities for dropbox API, for storing in the webhook based service, that was aborted.
"""

import dropbox
import dropbox.base
import pandas as pd
from io import BytesIO

from constants import (
    DROPBOX_ACCESS_TOKEN,
    DROPBOX_APP_KEY,
    DROPBOX_APP_SECRET,
)

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN, app_key=DROPBOX_APP_KEY, app_secret=DROPBOX_APP_SECRET)


def dropbox_to_pandas(dbx: dropbox.Dropbox, path: str) -> pd.DataFrame:
    assert path is not None
    metadata, res = dbx.files_download(path)  # type: ignore
    assert metadata is not None and res is not None
    data: bytes = res.content
    return pd.read_csv(BytesIO(data))


def pandas_to_dropbox(dbx: dropbox.Dropbox, dataframe: pd.DataFrame, path: str) -> bool:
    output = BytesIO()
    dataframe.to_csv(output, index=False)
    output.seek(0)
    dbx.files_upload(output.read(), path, mode=dropbox.base.files.WriteMode.overwrite)
    return True
