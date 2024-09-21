from PIL import Image as PILImage
from io import BytesIO
import os


def convert_image_to_webp(sender, instance, **kwargs):
    if instance.image:
        try:
            image = PILImage.open(instance.image)
            webp_buffer = BytesIO()
            image.save(webp_buffer, "WEBP")
            webp_buffer.seek(0)
            filename, _ = os.path.splitext(os.path.basename(instance.image.name))
            new_filename = filename + ".webp"
            instance.image.save(new_filename, webp_buffer, save=False)
        except Exception as e:
            print(f"Error converting image to WebP: {e}")
