import fitz
import os
import json

pdf_path = os.path.join("assets", "义务教育教科书·英语（一年级起点）一年级上册.pdf")
doc = fitz.open(pdf_path)

print(f"Inspecting PDF: {pdf_path} (Pages: {len(doc)})")

# 1. Check embedded files in PDF catalog / name tree
embedded_count = doc.embfile_count()
print(f"Embedded files count in PDF: {embedded_count}")
for i in range(embedded_count):
    name = doc.embfile_names()[i]
    info = doc.embfile_info(i)
    print(f"  Embedded File {i}: {name}, info: {info}")

# 2. Inspect page annotations (Sound annotations, Screen annotations, RichMedia)
sound_annots = []
media_annots = []

for idx, page in enumerate(doc):
    page_num = idx + 1
    annots = page.annots()
    if annots:
        for a in annots:
            a_type = a.type[1]  # string type representation
            a_sub = a.type[0]
            info = a.info
            # Print annotation info if relevant
            if a_type in ["Sound", "Screen", "RichMedia", "Movie", "FileAttachment"] or "sound" in str(a.type).lower():
                print(f"Page {page_num}: Annotation type {a_type} (sub {a_sub}), info: {info}")
                sound_annots.append({"page": page_num, "type": a_type, "info": info, "xref": a.xref})

# 3. Low-level object inspection for audio streams (/Sound, /MediaClip, /Audio, /WAV, /MP3)
audio_objects = []
for xref in range(1, doc.xref_length()):
    try:
        obj_str = doc.xref_object(xref)
        if "/Sound" in obj_str or "/Audio" in obj_str or "/MediaClip" in obj_str or "/Type /Sound" in obj_str or "audio/" in obj_str:
            print(f"Xref {xref} contains audio signature:\n{obj_str[:300]}")
            audio_objects.append(xref)
    except Exception as e:
        pass

print(f"\nSummary:")
print(f"Sound/Media annotations found: {len(sound_annots)}")
print(f"Audio stream Xref objects found: {len(audio_objects)}")
