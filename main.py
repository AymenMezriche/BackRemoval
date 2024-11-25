from flask import Flask, request, jsonify, send_file
from api.image_processor import process_image_from_base64

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def handle_image():
    # Check if the JSON body contains the 'image' key
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    base64_image = data['image']

    try:
        # Process the image using the function from image_processor
        processed_image_buffer = process_image_from_base64(base64_image)

        # Send the processed image as a response
        return send_file(processed_image_buffer, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def hello():
    return 'Hello! API is running.'

if __name__ == '__main__':
    app.run(debug=True)
