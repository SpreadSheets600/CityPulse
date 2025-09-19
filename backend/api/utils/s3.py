import io
import boto3
from PIL import Image


def get_s3_client(config):
    return boto3.client(
        "s3",
        endpoint_url=config["endpoint_url"],
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config.get("region_name"),
    )


def compress_image(file, max_size_mb=1.5, quality=85):

    img = Image.open(file)
    output = io.BytesIO()

    img.save(output, format="WEBP", quality=quality)
    output.seek(0)

    while output.getbuffer().nbytes > max_size_mb * 1024 * 1024 and quality > 40:
        quality -= 10
        output = io.BytesIO()
        img.save(output, format="WEBP", quality=quality)
        output.seek(0)
    return output


def upload_file_to_s3(fileobj, filename, config, content_type="image/webp"):
    s3 = get_s3_client(config)
    bucket = config["bucket_name"]

    s3.upload_fileobj(
        fileobj,
        bucket,
        filename,
        ExtraArgs={"ACL": "public-read", "ContentType": content_type},
    )

    url = f'{config["endpoint_url"].replace("https://", "https://"+bucket+".")}/{filename}'
    return url
