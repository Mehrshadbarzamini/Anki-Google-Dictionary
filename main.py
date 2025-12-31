import requests
import json
import base64

# CONFIGURATION
DECK_NAME = "MyVocabulary"  # Change this to your specific deck name
MODEL_NAME = "Google Dictionary" # The note type we created

def get_google_audio(word):
    """
    Google stores audio in a predictable pattern.
    We will try to fetch the US pronunciation.
    """
    url = f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word}--_us_1.mp3"
    response = requests.get(url, proxies={"http": None, "https": None})
    if response.status_code == 200:
        # We need to base64 encode the binary data to send via AnkiConnect
        return base64.b64encode(response.content).decode('utf-8')
    return None

def get_definition_data(word):
    """
    Uses the Free Dictionary API (often uses Oxford/Wiktionary data).
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url, proxies={"http": None, "https": None})
    if response.status_code != 200:
        return None
    return response.json()[0]

def add_note_to_anki(word, phonetic, audio_b64, part_speech, definition_html, examples_html):
    url = "http://localhost:8765" # AnkiConnect port
    
    # Prepare audio object if it exists
    audio_obj = []
    if audio_b64:
        filename = f"google_us_{word}.mp3"
        audio_obj = [{
            "url": "https://ssl.gstatic.com/dictionary/static/sounds/oxford/" + word + "--_us_1.mp3",
            "filename": filename,
            "fields": [
                "Audio"
            ]
        }]
        # Note: AnkiConnect can download URL directly, so we use that method below
    
    note = {
        "deckName": DECK_NAME,
        "modelName": MODEL_NAME,
        "fields": {
            "Word": word,
            "Phonetic": phonetic,
            "PartSpeech": part_speech,
            "Definition": definition_html,
            "Examples": examples_html,
            "Audio": "" # Will be filled by the audio download action
        },
        "options": {
            "allowDuplicate": False
        },
        "tags": ["google-import"],
        "audio": audio_obj
    }
    
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": note
        }
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def main():
    while True:
        target_word = input("Enter word to add (or 'q' to quit): ").strip().lower()
        if target_word == 'q':
            break

        print(f"Fetching data for '{target_word}'...")
        data = get_definition_data(target_word)
        
        if not data:
            print("Word not found in dictionary.")
            continue

        # Extract Phonetic
        phonetic = data.get('phonetic', '')
        if not phonetic and 'phonetics' in data:
            for p in data['phonetics']:
                if 'text' in p:
                    phonetic = p['text']
                    break
        
        # Extract Meanings (Constructing the HTML definition list) & Examples
        meanings_html = ""
        part_speech_display = ""
        examples_list = []  # Initialize list
        
        for meaning in data.get('meanings', []):
            p_speech = meaning.get('partOfSpeech', '')
            part_speech_display += f"{p_speech}, "
            
            meanings_html += f"<h3>{p_speech}</h3><ol>"
            for definition in meaning.get('definitions', []):
                defi = definition.get('definition', '')
                example = definition.get('example', '')
                
                meanings_html += f"<li>{defi}"
                if example:
                    meanings_html += f"<br><span class='example'>\"{example}\"</span>"
                    examples_list.append(example) # Collect example
                meanings_html += "</li>"
            meanings_html += "</ol>"

        part_speech_display = part_speech_display.rstrip(", ")
        
        # Create the HTML for the Examples field
        if examples_list:
            examples_html = "<ul>" + "".join([f"<li>{ex}</li>" for ex in examples_list]) + "</ul>"
        else:
            examples_html = ""

        # Check for Audio URL
        # We prefer constructing the google URL manually as it's cleaner
        # but the API usually provides one too. Let's use the manual Google URL logic
        # inside the add_note function for the cleanest US audio.
        
        result = add_note_to_anki(data['word'], phonetic, True, part_speech_display, meanings_html, examples_html)
        
        if result.get('error') is None:
            print(f"Success! Added '{target_word}' to Anki.")
        else:
            print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()