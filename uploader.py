import urllib.request
import minio
import pathlib
import os
import time
import urllib
import zipfile


def main():
    print("Connecting to minio...")
    client = minio.Minio("minio:9000", os.getenv("MY_ACCESS_KEY"), os.getenv("MY_SECRET_KEY"), secure=False)
    BUCKET = "mybucket"

    if not client.bucket_exists(BUCKET):
        print(f"Bucket '{BUCKET}' doesn't exist!")
        exit(1)

    print("Downloading images...")
    print("")
    path, _ = urllib.request.urlretrieve(
        "https://huggingface.co/datasets/XieMo/Furina_Genshin/resolve/main/Furina.zip?download=true",
        reporthook=lambda blocks, bytes, total: print(f"\033[F\033[KDownloaded {int(blocks * bytes / total * 100)}%")
    )

    print("Extracting images...")
    images_dir = pathlib.Path("images")
    images_dir.mkdir(511, True, True)
    with zipfile.ZipFile(path) as zip:
        zip.extractall("images")

    print("Uploading images to minio...")
    for dir in (images_dir / "Furina").iterdir():
        for file in dir.iterdir():
            print(f"Putting object '{file}'...")
            try:
                client.fput_object(
                    BUCKET,
                    file.name,
                    str(file),
                )
            except minio.error.S3Error as err:
                print(f"{err.message} on {file.name}")
            time.sleep(0.5)


if __name__ == "__main__":
    main()
