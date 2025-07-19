from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Image resizing view - resize to fit under a given size in KB
def img_resize(request):
    if request.method == 'POST':
        try:
            # Get uploaded image and target size in KB from form
            image_file = request.FILES['image']
            target_kb = int(request.POST['target_kb'])
            target_bytes = target_kb * 1024

            # Open image and determine format
            img = Image.open(image_file)
            img_format = img.format if img.format else 'JPEG'

            # Resize image if its dimensions exceed max allowed (e.g., 1600px)
            max_dim = 1600
            if max(img.size) > max_dim:
                img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

            # Convert transparent images to RGB
            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')

            # Binary search compression quality to stay under target size
            low, high = 20, 95
            best_buffer = None
            while low <= high:
                mid = (low + high) // 2
                buffer = BytesIO()
                img.save(buffer, format=img_format, quality=mid)
                size = buffer.tell()
                if size <= target_bytes:
                    best_buffer = buffer
                    low = mid + 1
                else:
                    high = mid - 1

            # If size is still too big, reduce dimensions and retry compression
            while (best_buffer is None or best_buffer.tell() > target_bytes) and min(img.size) > 200:
                new_size = (int(img.size[0] * 0.9), int(img.size[1] * 0.9))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                low, high = 20, 95
                while low <= high:
                    mid = (low + high) // 2
                    buffer = BytesIO()
                    img.save(buffer, format=img_format, quality=mid)
                    size = buffer.tell()
                    if size <= target_bytes:
                        best_buffer = buffer
                        low = mid + 1
                    else:
                        high = mid - 1

            # If all methods fail, return lowest quality image
            if best_buffer is None:
                best_buffer = BytesIO()
                img.save(best_buffer, format=img_format, quality=20)

            # Send resized image as download
            best_buffer.seek(0)
            response = HttpResponse(best_buffer, content_type=f'image/{img_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename="resized_image.{img_format.lower()}"'
            return response

        except (UnidentifiedImageError, KeyError, ValueError):
            return HttpResponse("Invalid input", status=400)
        except Exception:
            return HttpResponse("Image processing failed", status=500)

    return render(request, 'imgtools/img-resize.html')


# Image format converter view (e.g., JPG to PNG)
def img_to_img(request):
    if request.method == 'POST':
        try:
            # Get uploaded image and target format from form
            image_file = request.FILES['image']
            output_format = request.POST.get('target_format', 'PNG')

            # Open image and convert to new format
            image = Image.open(image_file)
            buffer = BytesIO()
            image.save(buffer, format=output_format)
            buffer.seek(0)

            # Return converted image as download
            response = HttpResponse(buffer, content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename="converted.{output_format.lower()}"'
            return response

        except (UnidentifiedImageError, KeyError):
            return HttpResponse("Invalid image file", status=400)
        except Exception:
            return HttpResponse("Conversion failed", status=500)

    return render(request, 'imgtools/img-to-img.html')


# Image to PDF converter view
def img_to_pdf(request):
    if request.method == 'POST':
        try:
            # Get uploaded image
            image_file = request.FILES['image']
            image = Image.open(image_file)

            # Convert to RGB and save as PDF
            buffer = BytesIO()
            image.convert('RGB').save(buffer, format='PDF')
            buffer.seek(0)

            # Return PDF as downloadable response
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="image.pdf"'
            return response

        except (UnidentifiedImageError, KeyError):
            return HttpResponse("Invalid image file", status=400)
        except Exception:
            return HttpResponse("PDF conversion failed", status=500)

    return render(request, 'imgtools/img-to-pdf.html')
