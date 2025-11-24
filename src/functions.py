"""
Functions
"""

import os
import boto3
import tqdm
import yaml

# get configuration
with open("../config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

S3_SERVER = config["S3_server"]
S3_ID_ENV_NAME = config["S3_id_env_name"]
S3_SECRET_ENV_NAME = config["S3_secret_env_name"]
OUTPUT_DIRECTORY = config["output_directory"]
DOWNLOAD_FILE = config["download_file"]
OUTPUT_FILE = config["output_file"]

# make output directory
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

# init S3 session
session = boto3.Session()

S3_CLIENT = session.client(
    service_name="s3",
    aws_access_key_id=os.environ[S3_ID_ENV_NAME],
    aws_secret_access_key=os.environ[S3_SECRET_ENV_NAME],
    endpoint_url=S3_SERVER,
)


def download_object_from_s3(client, *, bucket, key, version_id=None, filename):
    """
    Download an object from S3 with a progress bar.

    From https://alexwlchan.net/2021/04/s3-progress-bars/
    """
    s3 = client

    # First get the size, so we know what tqdm is counting up to.
    # Theoretically the size could change between this HeadObject and starting
    # to download the file, but this would only affect the progress bar.
    kwargs = {"Bucket": bucket, "Key": key}

    if version_id is not None:
        kwargs["VersionId"] = version_id

    object_size = s3.head_object(**kwargs)["ContentLength"]

    # Now actually download the object, with a progress bar to match.
    # How this works:
    #
    #   -   We take manual control of tqdm() using a ``with`` statement,
    #       see https://pypi.org/project/tqdm/#manual
    #
    #   -   We set ``unit_scale=True`` so tqdm uses SI unit prefixes, and
    #       ``unit="B"`` means it adds a "B" as a suffix.  This means we get
    #       progress info like "14.5kB/s".
    #
    #       (Note: the "B" is just a string; tqdm doesn't know these are
    #       bytes and doesn't care.)
    #
    #   -   The Callback method on a boto3 S3 function is called
    #       periodically during the download with the number of bytes
    #       transferred.  We can use it to update the progress bar.
    #
    if version_id is not None:
        ExtraArgs = {"VersionId": version_id}
    else:
        ExtraArgs = None

    with tqdm.tqdm(total=object_size, unit="B", unit_scale=True, desc=filename) as pbar:
        s3.download_file(
            Bucket=bucket,
            Key=key,
            ExtraArgs=ExtraArgs,
            Filename=filename,
            Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
        )
