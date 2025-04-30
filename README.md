This is a Python tool that extracts handwritten text from an image, summarizes it using GPT-4o and generations a PDF.

**Features**
- OCR text extraction using Google Vision API
- GPT-4o summarization and formatting
- Clean, structured PDF output
- Font support for special characters

**Input**
- An image path shall be inserted containing handwritten or printed notes.

**Output**
- A PDF file with summarized and organized content is added to the working directory.

**How to run**
1. Clone this repository:
   - git clone https://github.com/MustafaAhmadzai/NoteScanner.git
   - cd NoteScanner

3. Set up a virtual environment:
   - python -m venv venv
   - venv\Scripts\activate  # Windows
     #or
   - source venv/bin/activate  # macOS/Linux

4. Install dependencies:
   - pip install -r requirements.txt

5. Set environment variables:
   - OPENAI_API_KEY — your OpenAI API key
   - GOOGLE_APPLICATION_CREDENTIALS — absolute path to your client_creds.json file

6. Run the program:
   - python scanner_version2.py


