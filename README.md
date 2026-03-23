# DeepSeek Translator

**DeepSeek Translator** to narzędzie do szybkiego tłumaczenia tekstu przy użyciu API DeepSeek. Projekt posiada wygodne GUI w Pythonie i funkcję automatycznego wklejania przetłumaczonego tekstu.

## Funkcje

- Tłumaczenie tekstu na wybrany język (angielski, polski, niemiecki, ukraiński, rosyjski, hiszpański, francuski)
- Obsługa skrótu klawiszowego `Ctrl + Space` do natychmiastowego przetłumaczenia zaznaczonego tekstu
- Automatyczne kopiowanie wyniku do schowka i wklejanie w miejsce oryginalnego tekstu
- Graficzny interfejs użytkownika (Tkinter) z możliwością zmiany języka docelowego i zapisywania klucza API
- Opcja automatycznego wyświetlania okna translatora na wierzchu po tłumaczeniu
- Konfiguracja przechowywana w pliku `config.json`

## Instalacja

1. Zainstaluj wymagane biblioteki:
```bash
pip install keyboard pyperclip requests
