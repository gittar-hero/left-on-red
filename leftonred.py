#!/usr/bin/env python3
"""
Red-to-White PDF Converter - Command Line Version
No external dependencies needed!
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np
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


def process_pdf(input_pdf: str, output_pdf: str = None):
    """Process PDF and convert red pixels to white."""
    
    if not Path(input_pdf).exists():
        raise FileNotFoundError(f"PDF not found: {input_pdf}")
    
    if output_pdf is None:
        output_pdf = str(Path(input_pdf).parent / f"{Path(input_pdf).stem}_processed.pdf")
    
    print(f"Processing: {input_pdf}")
    print("=" * 60)
    
    print("Converting PDF to images...")
    pdf = pdfium.PdfDocument(input_pdf)
    num_pages = len(pdf)
    
    processed_images = []
    for i in range(num_pages):
        print(f"  Page {i+1}/{num_pages}...", end=" ", flush=True)
        page = pdf.get_page(i)
        bitmap = page.render(scale=2)
        img = bitmap.to_pil()
        
        # Convert red to white
        processed = convert_red_to_white(img, red_threshold=100, green_offset=20, blue_offset=20)
        processed_images.append(processed)
        print("✓")
    
    pdf.close()
    
    # Save as PDF
    print(f"\nSaving to: {output_pdf}")
    if processed_images:
        processed_images[0].save(
            output_pdf,
            save_all=True,
            append_images=processed_images[1:] if len(processed_images) > 1 else []
        )
    print("✓ Done!")
    
    return output_pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python testersred.py <input.pdf> [output.pdf]")
        print("\nExample:")
        print("  python testersred.py document.pdf")
        print("  python testersred.py document.pdf result.pdf")
        sys.exit(1)
    
    try:
        process_pdf(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
