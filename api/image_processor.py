import base64
from io import BytesIO
from PIL import Image

def process_image_from_base64(base64_image: str):
    try:
        # Decode the base64 string to bytes
        image_data = base64.b64decode(base64_image)

        # Open the image using PIL from the byte data
        image = Image.open(BytesIO(image_data))

        # Example image processing: Convert to grayscale
        processed_image = image.convert("L")

        # Save the processed image to a buffer and return it
        buffer = BytesIO()
        processed_image.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer
    except Exception as e:
        raise ValueError(f"Error processing the image: {str(e)}")
