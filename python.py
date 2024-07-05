from flask import Flask, request, send_file
from flask_cors import CORS
import qrcode
import io
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json['data']
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.convert("RGB")

    try:
        logo = Image.open("logo.png")
        logo_size = min(img.size[0] // 4, img.size[1] // 4)
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
        logo_pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(logo, logo_pos, mask=logo)
    except IOError:
        pass

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
