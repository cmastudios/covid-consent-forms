from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):

    bucket_name = 'consentformmedia.innovationdx.com'

    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass


class StaticStorage(S3Boto3Storage):

    bucket_name = 'consentformstatic.innovationdx.com'

    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass
