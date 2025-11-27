"""
Get data from S3
"""

# %%
# imports

from functions import (
    OUTPUT_DIRECTORY,
    S3_CLIENT,
    botocore,
    download_object_from_s3_with_progress,
)


# %%
#

# %%
# test listing folders and counting files


def list_folder_objects(client, bucket, prefix):
    file_list = []
    for key in client.list_objects(Bucket=bucket, Prefix=prefix)["Contents"]:
        file_list.append(key["Key"])

    return file_list


bucket = "tellae-mobility-bots"
prefix_list = [
    "GTFS-RT/renfe/",
    "gtfs/renfe-cercanias/",
    "gtfs/",
    "gbfs/",
    "GTFS-RT/bibus/",
]  # Make sure you provide / in the end

for prefix in prefix_list:
    print("******", prefix, "******")
    try:
        result = S3_CLIENT.list_objects(Bucket=bucket, Prefix=prefix, Delimiter="/")

        common_prefixes = result.get("CommonPrefixes")
        if not common_prefixes is None:
            for o in result.get("CommonPrefixes"):
                print("sub folder : ", o.get("Prefix"))
                print("# files: ", len(list_folder_objects(S3_CLIENT, bucket, prefix)))
        else:
            print("no sub folder")
            print("# files: ", len(list_folder_objects(S3_CLIENT, bucket, prefix)))

    except botocore.exceptions.ClientError as e:
        print(e)

# %%
# test downloading files

files = [
    "gtfs/madrid-metro-ligero/gtfs_madrid-metro-ligero_2025-11-11.zip",
    "GTFS-RT/renfe/bus_position_20250907_renfe.csv.bz2",
    "gbfs/auray/2025-02-02_auray.csv.bz2",
    "GTFS-RT/bibus/bus_position_20240102_bibus.csv.bz2",
]

for file in files:
    print("*******", file, "******")
    try:
        download_object_from_s3_with_progress(
            client=S3_CLIENT,
            bucket=bucket,
            key=file,
            filename=f"{OUTPUT_DIRECTORY}/{file.replace('/', '_')}",
        )
    except botocore.exceptions.ClientError as e:
        print(e)

# %%
#
