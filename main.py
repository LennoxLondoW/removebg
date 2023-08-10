from flask import Flask, request, Response
from rembg import remove
from io import BytesIO
from PIL import Image
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

@app.route('/removebg', methods=['GET'])
def remove_background():
    try:
        image_url = request.args.get('image_url')
        if not image_url:
            return "Please provide an 'image_url' parameter in the query string.", 400
        
        response = requests.get(image_url)
        if response.status_code != 200:
            return "Failed to fetch the image.", 500

        input_image = Image.open(BytesIO(response.content))
        output_image = remove(input_image)

        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return Response(output_buffer.read(), content_type='image/png')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
