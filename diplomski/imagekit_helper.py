import requests
from django.conf import settings
from imagekitio import ImageKit


def upload_to_imagekit(file):
    # Set the ImageKit configuration
    imagekit = ImageKit(
        private_key=settings.IMAGEKIT_PRIVATE_KEY,
        public_key=settings.IMAGEKIT_PUBLIC_KEY,
        url_endpoint=settings.IMAGEKIT_ENDPOINT
    )

    # Upload the file to ImageKit
    response = imagekit.upload(file)

    # Return the URL of the uploaded image
    return response.get('url')
