"""
Get data from S3
"""

# %%
# imports

from functions import (
    download_object_from_s3_with_progress,
    OUTPUT_DIRECTORY,
    S3_CLIENT,
    DOWNLOAD_FILE,
    OUTPUT_FILE,
)

# %%
# download

download_object_from_s3_with_progress(
    S3_CLIENT,
    bucket="tellae-mobility-bots",
    key=DOWNLOAD_FILE,
    filename=f"{OUTPUT_DIRECTORY}/{OUTPUT_FILE}",
)

# %%
