import os
import asyncio
import edge_tts
import re
import json

audio_dir = "audio"
os.makedirs(audio_dir, exist_ok=True)

# List of text blocks with audio in the textbook
audio_blocks = [
    # Starter
    {"id": "starter_miss_wu", "text": "Miss Wu", "type": "name"},
    {"id": "starter_bill", "text": "Bill", "type": "name"},
    {"id": "starter_lily", "text": "Lily", "type": "name"},
    {"id": "starter_yaoyao", "text": "Yaoyao", "type": "name"},
    {"id": "starter_binbin", "text": "Binbin", "type": "name"},
    {"id": "starter_andy", "text": "Andy", "type": "name"},
    {"id": "starter_lucky", "text": "Lucky", "type": "name"},
    {"id": "starter_angel", "text": "Angel", "type": "name"},
    {"id": "starter_dlg_1", "text": "Good morning! I'm Miss Wu.", "type": "sentence"},
    {"id": "starter_dlg_2", "text": "What's your name?", "type": "sentence"},
    {"id": "starter_dlg_3", "text": "Hello! My name is Bill.", "type": "sentence"},
    {"id": "starter_dlg_4", "text": "Good afternoon, Miss Wu.", "type": "sentence"},
    {"id": "starter_dlg_5", "text": "Hi, Bill.", "type": "sentence"},
    {"id": "starter_dlg_6", "text": "Bye, Bill. Goodbye.", "type": "sentence"},

    # Unit 1 School
    {"id": "u1_book", "text": "book", "type": "vocab"},
    {"id": "u1_ruler", "text": "ruler", "type": "vocab"},
    {"id": "u1_pencil", "text": "pencil", "type": "vocab"},
    {"id": "u1_eraser", "text": "eraser", "type": "vocab"},
    {"id": "u1_schoolbag", "text": "schoolbag", "type": "vocab"},
    {"id": "u1_chant_heading", "text": "Look, listen and chant.", "type": "heading"},
    {"id": "u1_action_ruler", "text": "Show me your ruler.", "type": "sentence"},
    {"id": "u1_action_pencil", "text": "Show me your pencil.", "type": "sentence"},
    {"id": "u1_sentence_ruler", "text": "I have a ruler.", "type": "sentence"},
    {"id": "u1_sentence_pencil", "text": "I have a pencil.", "type": "sentence"},
    {"id": "u1_sentence_book", "text": "I have a book.", "type": "sentence"},
    {"id": "u1_sentence_schoolbag", "text": "I have a schoolbag.", "type": "sentence"},
    {"id": "u1_story_1", "text": "Show me your schoolbag. Open it.", "type": "sentence"},
    {"id": "u1_story_2", "text": "Hi! I'm Angel.", "type": "sentence"},

    # Unit 2 Face
    {"id": "u2_face", "text": "face", "type": "vocab"},
    {"id": "u2_eye", "text": "eye", "type": "vocab"},
    {"id": "u2_ear", "text": "ear", "type": "vocab"},
    {"id": "u2_nose", "text": "nose", "type": "vocab"},
    {"id": "u2_mouth", "text": "mouth", "type": "vocab"},
    {"id": "u2_touch_mouth", "text": "Touch your mouth.", "type": "sentence"},
    {"id": "u2_touch_nose", "text": "Touch your nose.", "type": "sentence"},
    {"id": "u2_touch_eye", "text": "Touch your eye.", "type": "sentence"},
    {"id": "u2_this_mouth", "text": "This is my mouth.", "type": "sentence"},
    {"id": "u2_this_nose", "text": "This is my nose.", "type": "sentence"},
    {"id": "u2_this_ear", "text": "This is my ear.", "type": "sentence"},
    {"id": "u2_story_tail", "text": "Touch your tail. I have no tail.", "type": "sentence"},

    # Unit 3 Animals
    {"id": "u3_cat", "text": "cat", "type": "vocab"},
    {"id": "u3_dog", "text": "dog", "type": "vocab"},
    {"id": "u3_bird", "text": "bird", "type": "vocab"},
    {"id": "u3_monkey", "text": "monkey", "type": "vocab"},
    {"id": "u3_tiger", "text": "tiger", "type": "vocab"},
    {"id": "u3_panda", "text": "panda", "type": "vocab"},
    {"id": "u3_q_tiger", "text": "What's this? It's a tiger.", "type": "sentence"},
    {"id": "u3_q_dog", "text": "What's this? It's a dog.", "type": "sentence"},
    {"id": "u3_q_bird", "text": "What's this? It's a bird.", "type": "sentence"},

    # Unit 4 Numbers
    {"id": "u4_one", "text": "one", "type": "vocab"},
    {"id": "u4_two", "text": "two", "type": "vocab"},
    {"id": "u4_three", "text": "three", "type": "vocab"},
    {"id": "u4_four", "text": "four", "type": "vocab"},
    {"id": "u4_five", "text": "five", "type": "vocab"},
    {"id": "u4_six", "text": "six", "type": "vocab"},
    {"id": "u4_seven", "text": "seven", "type": "vocab"},
    {"id": "u4_eight", "text": "eight", "type": "vocab"},
    {"id": "u4_nine", "text": "nine", "type": "vocab"},
    {"id": "u4_ten", "text": "ten", "type": "vocab"},
    {"id": "u4_q_tigers", "text": "How many tigers are there?", "type": "sentence"},
    {"id": "u4_a_five", "text": "Five tigers.", "type": "sentence"},

    # Unit 5 Colours
    {"id": "u5_red", "text": "red", "type": "vocab"},
    {"id": "u5_yellow", "text": "yellow", "type": "vocab"},
    {"id": "u5_blue", "text": "blue", "type": "vocab"},
    {"id": "u5_green", "text": "green", "type": "vocab"},
    {"id": "u5_black", "text": "black", "type": "vocab"},
    {"id": "u5_q_yellow", "text": "What colour is it? It's yellow.", "type": "sentence"},
    {"id": "u5_a_black", "text": "It's black.", "type": "sentence"},

    # Unit 6 Fruit
    {"id": "u6_apple", "text": "apple", "type": "vocab"},
    {"id": "u6_banana", "text": "banana", "type": "vocab"},
    {"id": "u6_pear", "text": "pear", "type": "vocab"},
    {"id": "u6_orange", "text": "orange", "type": "vocab"},
    {"id": "u6_like_bananas", "text": "Do you like bananas? Yes, I do.", "type": "sentence"},
    {"id": "u6_like_pears", "text": "Do you like pears? No, I don't.", "type": "sentence"},

    # Chants & Expressions
    {"id": "chant_u1", "text": "Hello, pencil! Hello, ruler! Hello, schoolbag! Hello!", "type": "chant"},
    {"id": "chant_u3_1", "text": "Two little black birds sitting on a hill. One named Jack, one named Jill.", "type": "chant"},
    {"id": "chant_u3_2", "text": "Fly away Jack! Fly away Jill! Come back Jack, come back Jill!", "type": "chant"},
    {"id": "exp_morning", "text": "Good morning!", "type": "expression"},
    {"id": "exp_afternoon", "text": "Good afternoon!", "type": "expression"},
    {"id": "exp_hello", "text": "Hello! Hi!", "type": "expression"},

    # Revision 1 Safety Island
    {"id": "rev1_q_pencil", "text": "What's this? This is my pencil.", "type": "sentence"},
    {"id": "rev1_show_book", "text": "Show me your book.", "type": "sentence"},

    # Revision 2 Board Game
    {"id": "rev2_like_apples", "text": "Do you like apples? Yes, I do.", "type": "sentence"},
    {"id": "rev2_q_colour", "text": "What colour is it? It's red.", "type": "sentence"},
    {"id": "rev2_five", "text": "Five.", "type": "sentence"}
]

async def generate_single_audio(item):
    filepath = os.path.join(audio_dir, f"{item['id']}.mp3")
    if os.path.exists(filepath):
        print(f"Skipping {item['id']} (already exists)")
        return
    
    print(f"Generating audio for: {item['id']} -> '{item['text']}'")
    voice = "en-US-AnaNeural" if item["type"] in ["name", "vocab"] else "en-US-JennyNeural"
    communicate = edge_tts.Communicate(item["text"], voice)
    await communicate.save(filepath)

async def main():
    print(f"Starting audio extraction for {len(audio_blocks)} audio text blocks...")
    tasks = [generate_single_audio(item) for item in audio_blocks]
    await asyncio.gather(*tasks)
    
    # Save audio manifest
    manifest_path = os.path.join(audio_dir, "audio_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(audio_blocks, f, ensure_ascii=False, indent=2)
    
    print(f"\nAll {len(audio_blocks)} audio files saved locally in '{audio_dir}/' folder.")

if __name__ == "__main__":
    asyncio.run(main())
