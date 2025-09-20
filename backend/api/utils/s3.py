import io
import boto3
from PIL import Image
from botocore.config import Config


def get_s3_client(config):
    s3_config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        request_checksum_calculation="when_required",
        response_checksum_validation="when_required",
        s3={"addressing_style": "path"},
        signature_version="s3v4",
    )
    return boto3.client(
        "s3",
        endpoint_url=config["endpoint_url"],
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config.get("region_name"),
        config=s3_config,
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


def upload_file_to_s3(
    fileobj, filename, config, content_type="image/webp", signed_url_expires=3600
):
    s3 = get_s3_client(config)
    bucket = config["bucket_name"]

    file_content = fileobj.read()
    fileobj.seek(0)

    s3.put_object(
        Bucket=bucket, Key=filename, Body=file_content, ContentType=content_type
    )

    signed_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": filename},
        ExpiresIn=signed_url_expires,
    )

    return signed_url
