import fitz  # PyMuPDF

def reduce_pdf_size(input_pdf_path, output_pdf_path):
    # Open the input PDF
    pdf_document = fitz.open(input_pdf_path)
    
    # Create a new PDF document to save the reduced size PDF
    new_pdf_document = fitz.open()
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        # Create a pixmap with reduced resolution
        pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))  # Adjust the scaling factor as needed
        
        # Create a new page in the new PDF document with the same size as the original page
        new_page = new_pdf_document.new_page(width=page.rect.width, height=page.rect.height)
        
        # Insert the image into the new page
        new_page.insert_image(page.rect, pixmap=pix)
    
    # Save the compressed PDF
    new_pdf_document.save(output_pdf_path, garbage=4, deflate=True)
    new_pdf_document.close()
    pdf_document.close()

# Specify the input and output PDF file paths
input_pdf_path = r'C:\Users\adams\Downloads\meow.pdf'
output_pdf_path = r'C:\Users\adams\Downloads\reduced_file.pdf'

# Reduce the PDF size
reduce_pdf_size(input_pdf_path, output_pdf_path)

print(f"Reduced PDF size and saved to {output_pdf_path}")
