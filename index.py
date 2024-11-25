from flask import Flask, request, jsonify, send_file
import base64
from io import BytesIO
from PIL import Image
import torch
from carvekit.api.high import HiInterface
from time import time

app = Flask(__name__)

# Initialize carvekit interface
interface = HiInterface(object_type="hairs-like",  # "hairs-like" for hair, "object" for general
                        batch_size_seg=5,
                        batch_size_matting=1,
                        device='cuda' if torch.cuda.is_available() else 'cpu',
                        seg_mask_size=320,  # 320 for U2Net, good for hairs
                        matting_mask_size=2048,
                        trimap_prob_threshold=231,
                        trimap_dilation=30,
                        trimap_erosion_iters=5,
                        fp16=True)  # Enable FP16 for faster GPU processing if possible

# Track request time
@app.before_request
def start_timer():
    request.start_time = time()

@app.after_request
def log_request(response):
    duration = time() - request.start_time
    if duration > 120:  # Log if processing takes over 20 seconds
        app.logger.warning(f"Request timeout warning: {duration}s")
    return response

# Route for background removal
@app.route('/process-image', methods=['POST'])
def handle_image():
    try:
        # Check if the JSON body contains the 'image' key
        data = request.get_json()
        if 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode the base64 image
        base64_image = data['image']
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))

        # Save the input image temporarily (this is to simulate real-world scenario)
        temp_input_image_path = "input_image.jpg"
        image.save(temp_input_image_path)

        # Process the image using carvekit (remove background)
        images_without_background = interface([temp_input_image_path])
        output_image = images_without_background[0]

        # Save the processed image to a buffer
        buffer = BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Send the processed image as a response
        return send_file(buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test route
@app.route('/')
def hello():
    return 'Hello! API is running.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
