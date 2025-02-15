Voice Assistant - Transcription and Command Execution

Overview

This Python-based voice assistant allows users to record audio, transcribe it into text using OpenAI's Whisper model, and process the text with GPT-4o to execute various commands, including opening websites, launching applications, and managing notes. The assistant supports Polish language transcription and responses.

## Przegląd

Ten asystent głosowy oparty na Pythonie pozwala użytkownikom nagrywać dźwięk, transkrybować go na tekst za pomocą modelu Whisper OpenAI i przetwarzać tekst przy użyciu GPT-4o w celu wykonywania różnych poleceń, w tym otwierania stron internetowych, uruchamiania aplikacji i zarządzania notatkami. Asystent obsługuje transkrypcję i odpowiedzi w języku polskim.

## Features

- **Audio Recording**: Start and stop voice recording with a keyboard shortcut.
- **Speech-to-Text Transcription**: Uses Whisper to transcribe Polish speech.
- **AI Text Processing**: Processes transcribed text with GPT-4o-mini.
- **Text-to-Speech**: Uses gTTS to read AI responses aloud.
- **Web and Application Commands**: Opens URLs or launches macOS applications.
- **Note Management**: Create, read, update, delete, and list notes.

## Funkcje

- **Nagrywanie audio**: Rozpoczynanie i zatrzymywanie nagrywania głosu za pomocą skrótu klawiszowego.
- **Transkrypcja mowy na tekst**: Wykorzystuje Whisper do transkrypcji polskiej mowy.
- **Przetwarzanie tekstu przez AI**: Przetwarza transkrybowany tekst za pomocą GPT-4o-mini.
- **Tekst na mowę**: Używa gTTS do odczytywania odpowiedzi AI na głos.
- **Polecenia internetowe i aplikacyjne**: Otwiera adresy URL lub uruchamia aplikacje macOS.
- **Zarządzanie notatkami**: Tworzenie, odczyt, aktualizacja, usuwanie i lista notatek.

## Installation

### Prerequisites

Ensure you have Python installed, then install dependencies:

```sh
pip install openai whisper gtts pyaudio sounddevice scipy pynput pyperclip python-dotenv
```

### Instalacja

### Wymagania wstępne

Upewnij się, że masz zainstalowany Python, a następnie zainstaluj zależności:

```sh
pip install openai whisper gtts pyaudio sounddevice scipy pynput pyperclip python-dotenv
```

### API Key Setup

Create a `.env` file in the project directory with the following content:

```
OPENAI_API_KEY=your_openai_api_key
```

### Konfiguracja klucza API

dodaj do plik `.env` w katalogu projektu z następującą zawartością:

```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Start the Assistant

Run the script:

```sh
python assistant.py
```

Press `Ctrl + Shift + R` to start/stop recording.

### Użycie

### Uruchomienie Asystenta

Uruchom skrypt:

```sh
python assistant.py
```

Naciśnij `Ctrl + Shift + R`, aby rozpocząć/zatrzymać nagrywanie.

### Functionality

- **Voice Commands**: Speak commands to be processed by GPT-4o.
- **Web Commands**: If a URL is detected, it opens in the default browser.
- **App Commands**: If an application name is detected, it launches on macOS.
- **Note Management**:
  - `create`: Creates a note with specified content.
  - `read`: Reads out an existing note.
  - `update`: Updates a note's content.
  - `delete`: Deletes a specified note.
  - `list`: Lists all saved notes.

### Funkcjonalność

- **Polecenia głosowe**: Wypowiedz polecenia do przetworzenia przez GPT-4o.
- **Polecenia internetowe**: Jeśli wykryty zostanie adres URL, zostanie on otwarty w domyślnej przeglądarce.
- **Polecenia aplikacji**: Jeśli zostanie wykryta nazwa aplikacji, zostanie ona uruchomiona na macOS.
- **Zarządzanie notatkami**:
  - `create`: Tworzy notatkę z określoną treścią.
  - `read`: Odczytuje istniejącą notatkę.
  - `update`: Aktualizuje treść notatki.
  - `delete`: Usuwa określoną notatkę.
  - `list`: Wyświetla listę zapisanych notatek.

