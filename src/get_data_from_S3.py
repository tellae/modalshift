"""
Get data from S3
"""

# %%
# imports

from functions import (
    download_object_from_s3,
    S3_SERVER,
    S3_ID_ENV_NAME,
    S3_SECRET_ENV_NAME,
    OUTPUT_DIRECTORY,
    S3_CLIENT,
    DOWNLOAD_FILE,
    OUTPUT_FILE,
    os,
    boto3,
)

# %%
# download

download_object_from_s3(
    S3_CLIENT,
    bucket="tellae-mobility-bots",
    key=DOWNLOAD_FILE,
    filename=f"{OUTPUT_DIRECTORY}/{OUTPUT_FILE}",
)

# %%
