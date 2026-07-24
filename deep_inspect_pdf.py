import fitz
import os
import json

pdf_path = os.path.join("assets", "义务教育教科书·英语（一年级起点）一年级上册.pdf")
doc = fitz.open(pdf_path)

print(f"Deep inspecting {len(doc)} pages for Links, Actions, Streams, and Audio references...")

link_details = []

for idx, page in enumerate(doc):
    page_num = idx + 1
    # Check links on page
    links = page.get_links()
    if links:
        for l in links:
            link_details.append({
                "page": page_num,
                "kind": l.get("kind"),
                "uri": l.get("uri"),
                "file": l.get("file"),
                "from": [round(x, 1) for x in l.get("from", [])],
                "xref": l.get("xref")
            })
    
    # Check all annotations regardless of type
    annot = page.first_annot
    while annot:
        print(f"Page {page_num}: Found annot type={annot.type}, rect={annot.rect}, info={annot.info}")
        annot = annot.next

print(f"\nTotal links found across pages: {len(link_details)}")
for l in link_details[:20]:
    print(f"  Page {l['page']}: kind={l['kind']}, uri={l['uri']}, file={l['file']}, from={l['from']}")

# Deep search all Xref objects for stream data with sound/audio or media keywords
print("\nSearching Xref objects for streams and media references...")
stream_audio_xrefs = []

for xref in range(1, doc.xref_length()):
    try:
        keys = doc.xref_get_keys(xref)
        obj_str = doc.xref_object(xref)
        
        # Check if object is a stream
        if doc.is_stream(xref):
            # Try reading stream bytes header
            try:
                stream_bytes = doc.xref_stream(xref)
                # Check magic bytes for MP3 (ID3 or 0xFF 0xFB/0xF3/0xF2), WAV (RIFF...WAVE), AAC, OGG
                if stream_bytes.startswith(b'ID3') or b'WAVE' in stream_bytes[:20] or b'OggS' in stream_bytes[:20]:
                    print(f"Xref {xref} has audio magic bytes! Size: {len(stream_bytes)} bytes")
                    stream_audio_xrefs.append((xref, len(stream_bytes)))
            except Exception:
                pass

        if any(k in obj_str for k in ["/Audio", "/Sound", "/Media", "/Movie", "/Rendition", ".mp3", ".wav", ".m4a"]):
            print(f"Xref {xref} mentions media:\n  {obj_str[:250]}")
    except Exception as e:
        pass

print(f"Found {len(stream_audio_xrefs)} raw audio streams in PDF.")
