import io
from urllib.parse import urlparse
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


def extract_s3_key(url_or_key, bucket_name=None):
    """Extract the S3 object key from a presigned URL or return the key directly.

    Handles both:
    - Plain object keys (e.g. 'issues/images/user_uuid_file.webp')
    - Presigned URLs (e.g. 'https://endpoint/bucket/key?X-Amz-...')
    """
    if not url_or_key:
        return url_or_key
    if url_or_key.startswith("http://") or url_or_key.startswith("https://"):
        parsed = urlparse(url_or_key)
        path = parsed.path.lstrip("/")
        if bucket_name and path.startswith(bucket_name + "/"):
            path = path[len(bucket_name) + 1 :]
        return path
    return url_or_key


def generate_presigned_url(key, config, expires_in=3600):
    """Generate a fresh presigned URL for an S3 object key."""
    s3 = get_s3_client(config)
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": config["bucket_name"], "Key": key},
        ExpiresIn=expires_in,
    )


def resolve_media_urls(keys_or_urls, config):
    """Convert a list of stored S3 keys (or legacy presigned URLs) to fresh presigned URLs."""
    if not keys_or_urls:
        return keys_or_urls
    bucket_name = config.get("bucket_name")
    return [
        generate_presigned_url(extract_s3_key(u, bucket_name), config)
        for u in keys_or_urls
    ]


def resolve_media_url(url_or_key, config):
    """Convert a single stored S3 key (or legacy presigned URL) to a fresh presigned URL."""
    if not url_or_key:
        return url_or_key
    bucket_name = config.get("bucket_name")
    return generate_presigned_url(extract_s3_key(url_or_key, bucket_name), config)


def upload_file_to_s3(
    fileobj, filename, config, content_type="image/webp"
):
    s3 = get_s3_client(config)
    bucket = config["bucket_name"]

    file_content = fileobj.read()
    fileobj.seek(0)

    s3.put_object(
        Bucket=bucket, Key=filename, Body=file_content, ContentType=content_type
    )

    return filename
