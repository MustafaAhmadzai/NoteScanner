from google.cloud import vision
import os
from openai import OpenAI
import io
from fpdf import FPDF

OPENAI_API = os.getenv("OPENAI_API_KEY")
#GOOGLE_CREDS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_CREDS_PATH = "client_creds.json"
client = OpenAI(api_key=OPENAI_API)


def extract_text_from_image_google_vision(image_path):
    client = vision.ImageAnnotatorClient()
    # read img file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # image instance
    image = vision.Image(content=content)

    # text detection from cloud vision
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # error checking
    if response.error.message:
        raise Exception(f'Google Vision API error: {response.error.message}')

    if texts:
        full_text = texts[0].description.strip()
    else:
        full_text = ""

    return full_text


def post_API(note_text):

    instructions = (
        "You are an expert note summarizer and professional document formatter.\n\n"
        "Your task is to:\n"
        "- Refine raw notes extracted from handwritten documents\n"
        "- Correct OCR errors (e.g., misspelled words, jumbled or disordered phrases)\n"
        "- Add brief, relevant context to improve clarity\n"
        "- Organize the result into a clean, structured format that is suitable for PDF conversion\n\n"
        "Formatting Rules (Strict — Follow Exactly):\n"
        "1. The first line must be a concise, summarized title using '###'.\n"
        "2. You may only use the following formatting symbols:\n"
        "   - '###' for titles/headings (maximum of 3 per document)\n"
        "   - '!!!' for subheadings (maximum of 3 per document)\n"
        "   - '-' for bullet points (always followed by a space, e.g., '- Correct example')\n"
        "3. Do not use any other formatting symbols:\n"
        "   - No asterisks such as '*' or '**'\n"
        "   - No underscores\n"
        "   - No italics, bold, markdown, or any other styles\n"
        "4. Leave appropriate spacing between headings, subheadings, and bullet sections to maintain readability\n"
        "5. Avoid large blocks of text — break down content logically using subheadings and bullets\n\n"
        "Style:\n"
        "- Maintain a professional, educational tone\n"
        "- Be concise and clear\n"
        "- Use subheadings to reduce clutter and improve scanability\n\n"
        "Example Input:\n"
        "\"ph goes up means seizure risk patient needs suction availble bedside\"\n\n"
        "Example Output:\n"
        "### Acid-Base Imbalance Summary\n"
        "!!! Effects of High pH\n"
        "- Increased risk of seizures\n"
        "- Ensure suction equipment is available at bedside\n\n"
        "Repeat: Use only '###', '!!!', and '-'. Do not use any other symbols or styles."
    )

    if note_text:
        response = client.responses.create(
            model="gpt-4o",
            instructions=instructions,
            input=note_text
        )
    
    return response.output_text


class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font_path = os.path.join(os.getcwd(), "DejaVuSans.ttf")
        self.add_font('DejaVuSans', '', font_path, uni=True)


    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVuSans', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(note_text, output_file='output.pdf'):
    pdf = PDF()
    pdf.add_page()
    pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVuSans', '', 12)
    pdf.add_font('DejaVuSans_Bold', '', 'DejaVuSans-Bold.ttf', uni=True)

    for line in note_text.splitlines():
        line = line.strip()
        if line.startswith('###'):
            title_text = line[3:].strip()
            pdf.set_font('DejaVuSans_Bold', '', 16) # Bold title
            pdf.cell(0, 10, title_text, ln=True, align='C')
            pdf.ln(1)
        elif line.startswith('!!!'):
            pdf.set_font('DejaVuSans_Bold', '', 13)  # Bold subheading
            pdf.cell(0, 8, line[3:].strip(), ln=True)
        else:
            pdf.set_font('DejaVuSans', '', 12)   # Body text
            pdf.multi_cell(0, 8, line)

    output_file = title_text + ".pdf"
    pdf.output(output_file)
    return output_file

if __name__ == '__main__':
    image_path = input("Please input the file image path: ")
    extracted_text = extract_text_from_image_google_vision(image_path)
    summarized_notes = post_API(extracted_text)
    create_pdf(summarized_notes)