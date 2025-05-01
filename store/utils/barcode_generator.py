import base64
from io import BytesIO

import barcode
from barcode.writer import ImageWriter
from PIL import Image


def generate_base64_barcode(value):
    CODE128 = barcode.get_barcode_class("code128")
    barcode_obj = CODE128(value, writer=ImageWriter())

    buffer = BytesIO()

    # Generate barcode with the desired width and height
    barcode_obj.write(
        buffer,
        options={
            "write_text": False,
            "module_height": 10.0,  # Adjust this for the desired barcode height
            "module_width": 0.2,  # Narrower bars for better fitting
            "quiet_zone": 1.0,  # Padding around barcode
        },
    )

    # Adjust image size to exactly fit the container dimensions (243px x 79px)
    img = Image.open(buffer)
    img = img.resize((243, 79))  # Resize to fit the required size (in pixels)

    # Rotate the image 90 degrees
    img = img.rotate(90, expand=True)

    # Save the rotated image to buffer again
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{encoded}"
