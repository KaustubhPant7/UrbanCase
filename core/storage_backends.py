import mimetypes
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Custom S3 storage that correctly sets Content-Type for all
    file formats including GIF, WebP, SVG, and video files.
    """

    def _save(self, name, content):
        # Detect MIME type from filename
        content_type, _ = mimetypes.guess_type(name)
        if content_type:
            # Set the correct Content-Type so browsers render inline
            if hasattr(content, "content_type"):
                content.content_type = content_type
            self.object_parameters.update({"ContentType": content_type})
        return super()._save(name, content)
