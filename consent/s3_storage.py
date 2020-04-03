from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'consentformmedia.innovationdx.com'
    region_name = 'us-west-2'
    querystring_auth = True
    querystring_expire = 600  # expire after 10 minutes for security
    object_parameters = {'ServerSideEncryption': 'AES256'}
    default_acl = None


class StaticStorage(S3Boto3Storage):
    bucket_name = 'consentformstatic.innovationdx.com'
    region_name = 'us-west-2'
    querystring_auth = False
    default_acl = 'public-read'
