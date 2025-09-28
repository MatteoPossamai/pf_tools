import dropbox
import dropbox.base
import pandas as pd
from io import BytesIO

from constants import ACCESS_TOKEN, TRANSACTIONS_FILE_PATH, APP_KEY, APP_SECRET

dbx = dropbox.Dropbox(ACCESS_TOKEN, app_key=APP_KEY, app_secret=APP_SECRET)


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


if __name__ == "__main__":
    print(dropbox_to_pandas(dbx, TRANSACTIONS_FILE_PATH))
