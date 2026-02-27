import streamlit as st
from PIL import Image
import numpy as np
import io
import tempfile
import os
from pathlib import Path
import pypdfium2 as pdfium


def convert_red_to_white(image: Image.Image, red_threshold=100, green_offset=20, blue_offset=20):
    """Convert all red pixels in an image to white."""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    data = np.array(image)
    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    
    mask = (r > red_threshold) & (r > g + green_offset) & (r > b + blue_offset)
    data[mask] = [255, 255, 255]
    
    return Image.fromarray(data)


def convert_pdf_to_images(input_pdf):
    """Convert PDF to images using pypdfium2"""
    pdf = pdfium.PdfDocument(input_pdf)
    images = []
    
    for page_num in range(len(pdf)):
        page = pdf.get_page(page_num)
        bitmap = page.render(scale=2)
        img = bitmap.to_pil()
        images.append(img)
    
    pdf.close()
    return images



st.set_page_config(page_title="Red to White PDF Converter", layout="centered")
st.title("Left On Red: PDF Red Pixel Converter")

st.write("""
This app converts all red pixels in a PDF to white.
Upload your PDF file and download the processed version.
""")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Display file info
    st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.2f} MB)")
    
    # Red detection threshold settings
    st.subheader("⚙️ Red Detection Settings")
    col1, col2, col3 = st.columns(3)
    with col1:
        red_threshold = st.slider("Red threshold (0-255)", 0, 255, 100)
    with col2:
        green_threshold = st.slider("Green threshold offset", 0, 100, 20)
    with col3:
        blue_threshold = st.slider("Blue threshold offset", 0, 100, 20)
    
    # Process button
    if st.button("🔄 Process PDF", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name
            
            status_text.text("Converting PDF to images...")
            progress_bar.progress(10)
            
            # Convert PDF to images
            images = convert_pdf_to_images(tmp_path)
            num_pages = len(images)
            
            status_text.text(f"Processing {num_pages} page(s)...")
            progress_bar.progress(30)
            
            # Process each image
            processed_images = []
            for i, image in enumerate(images):
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Convert to numpy array for faster processing
                data = np.array(image)
                r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
                
                # Define red pixels with user-selected thresholds
                mask = (r > red_threshold) & (r > g + green_threshold) & (r > b + blue_threshold)
                
                # Apply the mask: turn red pixels white
                data[mask] = [255, 255, 255]
                
                # Convert back to image
                processed_images.append(Image.fromarray(data))
                
                # Update progress
                progress = 30 + int((i + 1) / num_pages * 50)
                progress_bar.progress(progress)
            
            status_text.text("Saving as PDF...")
            progress_bar.progress(85)
            
            # Save processed images as PDF
            output_buffer = io.BytesIO()
            rgb_images = [img.convert('RGB') for img in processed_images]
            rgb_images[0].save(
                output_buffer,
                format='PDF',
                save_all=True,
                append_images=rgb_images[1:] if len(rgb_images) > 1 else []
            )
            output_buffer.seek(0)
            
            progress_bar.progress(100)
            status_text.text("Processing complete!")
            
            # Download button
            st.download_button(
                label="📥 Download Processed PDF",
                data=output_buffer.getvalue(),
                file_name=f"{Path(uploaded_file.name).stem}_processed.pdf",
                mime="application/pdf",
                type="primary"
            )
            
            # Display statistics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Pages processed", num_pages)
            with col2:
                st.metric("Red pixels converted", "All detected")
            
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

# Footer
st.divider()
st.caption("💡 Tip: Adjust the thresholds if the detection isn't working perfectly for your PDF.")
