# Anki-Google-Dictionary

A Python tool that automates creating "Google Dictionary" style flashcards in Anki. It fetches definitions, IPA phonetics, and **Google's official US pronunciation audio** directly from the web and pushes them to Anki via AnkiConnect.

## Features

- **Google Audio:** Downloads the specific US pronunciation MP3s used by Google Search.
- **Rich Data:** Fetches meanings, parts of speech, and example sentences.
- **Beautiful Styling:** Includes a CSS template that mimics Google's Dark Mode dictionary.
- **Smart Fields:** Separates Definitions and Example sentences into different fields for cleaner card layouts.

## Prerequisites

1.  **Anki Desktop** installed.
2.  **AnkiConnect** Add-on installed:
    *   Open Anki -> Tools -> Add-ons -> Get Add-ons.
    *   Code: `2055492159`.
    *   Restart Anki.
3.  **Python 3.x** installed.

## Setup (One-Time)

Before running the script, you must set up the specific Note Type in Anki so the script knows where to put the data.

### 1. Create the Note Type
1.  In Anki, go to **Tools** -> **Manage Note Types**.
2.  Click **Add** -> **Add: Basic** -> Name it: `Google Dictionary`.
3.  Select it and click **Fields**. Ensure you have exactly these fields (case-sensitive):
    *   `Word`
    *   `Phonetic`
    *   `Audio`
    *   `PartSpeech`
    *   `Definition`
    *   `Examples`

### 2. Configure Card Templates
Select the **Google Dictionary** note type and click **Cards**.

**Front Template:**
```html
<div class="google-card">
  <div class="word">{{Word}}</div>
  <div class="phonetic">{{Phonetic}}</div>
</div>
```

**Back Template:**
```html
<div class="google-card">
  <div class="word">{{Word}}</div>
  <div class="phonetic">{{Phonetic}} {{Audio}}</div>
  
  <div class="part-speech">{{PartSpeech}}</div>
  
  <div class="definition-block">
    {{Definition}}
  </div>

  <div class="examples-section">
    <hr>
    <div class="part-speech" style="font-size: 0.8em;">All Examples</div>
    {{Examples}}
  </div>
</div>
```

**Styling (CSS):**
```css
.card {
  font-family: 'Roboto', 'Arial', sans-serif;
  background-color: #202124;
  color: #bdc1c6;
  font-size: 16px;
  text-align: left;
  line-height: 1.5;
}

.google-card {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.word {
  font-size: 32px;
  color: #e8eaed;
  margin-bottom: 5px;
}

.phonetic {
  color: #9aa0a6;
  margin-bottom: 20px;
}

.part-speech {
  font-style: italic;
  font-weight: bold;
  color: #8ab4f8;
  margin-top: 15px;
  margin-bottom: 5px;
}

.definition-block ol {
  padding-left: 20px;
}

.definition-block li {
  margin-bottom: 10px;
}

.example {
  color: #9aa0a6;
  font-style: italic;
  display: block;
  margin-top: 4px;
}

/* Example Section at bottom */
.examples-section {
  margin-top: 20px;
  font-size: 14px;
  color: #9aa0a6;
}
.examples-section ul {
  padding-left: 20px;
  margin: 0;
}
.examples-section li {
  margin-bottom: 5px;
}
hr {
  border: 0;
  border-top: 1px solid #3c4043;
  margin: 20px 0;
}
```

## Installation & Usage

1.  Clone this repository.
2.  Create a virtual environment:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration:** Open `main.py` and edit the configuration at the top to match your Anki Deck name:
    ```python
    DECK_NAME = "MyVocabulary"  # Change this to your deck
    ```
5.  **Run:** Ensure Anki is open, then run:
    ```bash
    python main.py
    ```
6.  Type a word and hit enter. The card will appear in your deck immediately.

## Troubleshooting

- **ProxyError / SSL Error:** The script includes `proxies={"http": None, "https": None}` to bypass system proxies that often cause issues with Python `requests` on Windows.
- **Connection Refused:** Ensure Anki is open and AnkiConnect is installed.