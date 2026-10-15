from pdf2image import convert_from_path
import os

# Input PDF and output directory
pdf_path = "C:\\Users\\lsz\\Desktop\\KeyShield\\Video_Assets\\KeyShield_Slide_Deck.pdf"
output_dir = "C:\\Users\\lsz\\Desktop\\KeyShield\\Video_Assets\\slides"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Convert PDF to images
pages = convert_from_path(pdf_path, dpi=300, output_folder=output_dir,poppler_path=r"D:\poppler\Library\bin")

# Save each page as an image
for i, page in enumerate(pages):
    image_path = os.path.join(output_dir, f"slide_{i+1}.png")
    page.save(image_path, "PNG")
    print(f"Saved: {image_path}")

print(f"Converted {len(pages)} slides to images in {output_dir}")