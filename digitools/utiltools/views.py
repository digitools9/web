# Import necessary Django modules and libraries
from django.shortcuts import render
from django.contrib import messages
from io import BytesIO
import base64
import qrcode
import pyshorteners

# QR Code Generator View
def qr_generator(request):
    qr_img_base64 = None  # Holds the base64-encoded QR image string
    qr_text = ''  # Holds the input text for QR code generation

    if request.method == 'POST':
        qr_text = request.POST.get('qr_text', '')  # Get the input text from form
        if qr_text:
            try:
                # Configure the QR code parameters
                qr = qrcode.QRCode(
                    version=1,  # Controls the size of the QR code
                    error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction
                    box_size=10,  # Size of each box in pixels
                    border=4,  # Border thickness
                )
                qr.add_data(qr_text)  # Add data to QR code
                qr.make(fit=True)  # Fit the QR code size to the input

                # Generate the QR image
                img = qr.make_image(fill_color="black", back_color="white")

                # Save image to memory buffer
                buffer = BytesIO()
                img.save(buffer, format="PNG")

                # Encode image in base64 to embed in HTML
                img_str = base64.b64encode(buffer.getvalue()).decode()
                qr_img_base64 = f"data:image/png;base64,{img_str}"
            except Exception as e:
                messages.error(request, f'Error generating QR code: {str(e)}')

    # Render the template with QR image and input text
    return render(request, 'utiltools/qr-generator.html', {
        'qr_img_base64': qr_img_base64,
        'qr_text': qr_text
    })


# URL Shortener View
def url_shortener(request):
    short_url = None  # Holds the shortened URL
    original_url = None  # Holds the original input URL

    if request.method == 'POST':
        original_url = request.POST.get('original_url', '')  # Get the input URL
        if original_url:
            try:
                # Initialize URL shortener (default is TinyURL)
                shortener = pyshorteners.Shortener()

                # Generate shortened URL
                short_url = shortener.tinyurl.short(original_url)

                # Show success message
                messages.success(request, 'URL shortened successfully!')

            except Exception as e:
                # Handle errors during URL shortening
                messages.error(request, f'Error shortening URL: {str(e)}')

    # Render the template with original and shortened URLs
    return render(request, 'utiltools/url-shortener.html', {
        'short_url': short_url,
        'original_url': original_url
    })

