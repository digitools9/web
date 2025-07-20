from django.shortcuts import render, HttpResponse
from pypdf import PdfReader, PdfWriter
from io import BytesIO


def pdf_merge(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')

        # Ensure user selected at least two PDF files
        if len(pdf_files) < 2:
            return render(request, 'pdftools/pdf-merger.html', {
                'error': 'Please select at least 2 PDF files to merge'
            })

        # Validate that all uploaded files are PDFs
        for pdf_file in pdf_files:
            if not pdf_file.name.lower().endswith('.pdf'):
                return render(request, 'pdftools/pdf-merger.html', {
                    'error': 'All files must be PDFs'
                })

        # Create a writer object to store merged PDF pages
        merger = PdfWriter()

        try:
            # Iterate through each uploaded PDF file
            for pdf_file in pdf_files:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    merger.add_page(page)

            # Write the merged PDF to memory buffer
            output_buffer = BytesIO()
            merger.write(output_buffer)
            output_buffer.seek(0)

            # Return the merged PDF as downloadable response
            response = HttpResponse(
                output_buffer.getvalue(),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
            return response

        except Exception as e:
            # Handle any errors during merging
            return render(request, 'pdftools/pdf-merger.html', {
                'error': f'Error merging PDFs: {str(e)}'
            })

    # Render the merge tool UI on GET request
    return render(request, 'pdftools/pdf-merger.html')


def pdf_splitter(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('pdf'):
        try:
            # Get start and end page numbers from user input (1-based index)
            start = int(request.POST.get('start', 1)) - 1
            end = int(request.POST.get('end', 1))

            reader = PdfReader(request.FILES['pdf'])
            writer = PdfWriter()

            # Add specified range of pages to the new PDF
            for i in range(start, end):
                writer.add_page(reader.pages[i])

            # Write the split PDF to memory buffer
            buffer = BytesIO()
            writer.write(buffer)
            buffer.seek(0)

            # Return the split PDF as downloadable response
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="split.pdf"'
            return response

        except Exception as e:
            # Handle any errors during splitting
            context['error'] = f'Error splitting PDF: {str(e)}'

    # Render the split tool UI on GET request or error
    return render(request, 'pdftools/pdf-splitter.html', context)


def encrypt_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file') and request.POST.get('password'):
        try:
            pdf_file = request.FILES['pdf_file']
            password = request.POST['password']

            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            # Copy all pages to the writer object
            for page in reader.pages:
                writer.add_page(page)

            # Apply password protection
            writer.encrypt(password)

            # Write encrypted PDF to memory buffer
            output_stream = BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            # Return the encrypted PDF as downloadable response
            response = HttpResponse(output_stream, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="encrypted.pdf"'
            return response

        except Exception as e:
            # Handle any errors during encryption
            return render(request, 'pdftools/encrypt-pdf.html', {
                'error': f'Error encrypting PDF: {str(e)}'
            })

    # Render the encryption tool UI on GET request or error
    return render(request, 'pdftools/encrypt-pdf.html')


def decrypt_pdf(request):
    # Handle POST request with uploaded PDF and provided password
    if request.method == 'POST' and request.FILES.get('pdf_file') and request.POST.get('password'):
        try:
            pdf_file = request.FILES['pdf_file']
            password = request.POST['password']

            reader = PdfReader(pdf_file)

            # Check if the uploaded PDF is encrypted
            if not reader.is_encrypted:
                return render(request, 'pdftools/decrypt-pdf.html', {
                    'error': 'This PDF is not encrypted.'
                })

            # Try to decrypt using the provided password
            if not reader.decrypt(password):
                return render(request, 'pdftools/decrypt-pdf.html', {
                    'error': 'Incorrect password.'
                })

            # Create writer object and copy all pages after decryption
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            # Write decrypted PDF to memory buffer
            output_stream = BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            # Return the decrypted PDF as downloadable response
            response = HttpResponse(output_stream, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="decrypted.pdf"'
            return response

        except Exception as e:
            # Handle any errors during decryption
            return render(request, 'pdftools/decrypt-pdf.html', {
                'error': f'Error decrypting PDF: {str(e)}'
            })

    # Render the decryption tool UI on GET request or error
    return render(request, 'pdftools/decrypt-pdf.html')
