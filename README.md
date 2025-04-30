# Note Scanner
This is a Python tool that extracts handwritten text from an image, summarizes it using GPT-4o and generations a PDF.

## Features
- OCR text extraction using Google Vision API
- GPT-4o summarization and formatting
- Clean, structured PDF output
- Font support for special characters


## Run Locally

Clone the project

```bash
  git clone https://github.com/MustafaAhmadzai/NoteScanner.git
```

Go to the project directory

```bash
  cd NoteScanner
```

Create virtual environment

```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  # or
  source venv/bin/activate # macOS/Linux
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run the program

```bash
  python scanner_version2.py
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_KEY`

`GOOGLE_APPLICATION_CREDENTIALS`








