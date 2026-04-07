# DeepSeek Translator

**DeepSeek Translator** This is a tool for fast text translation using the DeepSeek API. The project features a convenient Python GUI and an automatic paste function for translated text.

## Funkcje

- Translation of the text into the selected language (English, Polish, German, Ukrainian, Russian, Spanish, French)
- Handling the keyboard shortcut `Ctrl + Space` for instant translation of selected text
- Automatic copying of the result to the clipboard and pasting in place of the original text
- Graphical User Interface (Tkinter) with the ability to change the target language and save the API key.
- The option to automatically display the translator window on top after translation
- Configuration stored in the "config.json" file

## Instalacja

1. Install the required libraries:
```bash
pip install keyboard pyperclip requests
