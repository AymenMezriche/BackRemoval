import base64
from http.server import BaseHTTPRequestHandler
from io import BytesIO
from PIL import Image
from carvekit.api.high import HiInterface  # Assuming CarveKit is installed

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.headers.get('Content-Type') != 'application/json':
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Invalid content type. Expected application/json.'.encode('utf-8'))
            return

        try:
            # Read and decode the incoming JSON payload
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Parse Base64 data (assume `image` key in JSON payload)
            import json
            request_data = json.loads(post_data)
            if 'image' not in request_data:
                raise ValueError("Missing 'image' key in the request data.")

            # Decode the Base64 image
            image_data = base64.b64decode(request_data['image'])
            input_image = Image.open(BytesIO(image_data))

            # Save the decoded image temporarily
            input_image_path = 'temp_input_image.png'
            input_image.save(input_image_path)

            # Process the image
            processed_image_path = self.process_image(input_image_path)

            # Read the processed image and encode it back to Base64
            with open(processed_image_path, 'rb') as f:
                processed_image_base64 = base64.b64encode(f.read()).decode('utf-8')

            # Respond with the processed image in Base64 format
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_data = json.dumps({'processed_image': processed_image_base64})
            self.wfile.write(response_data.encode('utf-8'))

        except Exception as e:
            # Handle errors
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error processing image: {str(e)}'.encode('utf-8'))

    def process_image(self, input_image_path):
        # Simplified image processing logic using CarveKit
        interface = HiInterface(
            object_type="hairs-like",
            batch_size_seg=5,
            batch_size_matting=1,
            device='cpu',
            seg_mask_size=320,
            matting_mask_size=2048,
            trimap_prob_threshold=231,
            trimap_dilation=30,
            trimap_erosion_iters=5,
            fp16=False
        )

        # Process the input image
        output_image_path = 'output_image.png'
        images_without_background = interface([input_image_path])
        images_without_background[0].save(output_image_path)
        return output_image_path
