import fitz
import json
import os

pdf_path = os.path.join("assets", "义务教育教科书·英语（一年级起点）一年级上册.pdf")
doc = fitz.open(pdf_path)

pages_data = []

for idx, page in enumerate(doc):
    page_num = idx + 1
    text = page.get_text("text")
    blocks = page.get_text("blocks")
    images = page.get_images()
    
    pages_data.append({
        "page": page_num,
        "text": text,
        "block_count": len(blocks),
        "image_count": len(images)
    })

with open("pdf_structure.json", "w", encoding="utf-8") as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print(f"Parsed {len(pages_data)} pages. Saved structure to pdf_structure.json.")
