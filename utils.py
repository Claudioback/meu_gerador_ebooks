import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, letter
from reportlab.lib.utils import ImageReader
from PIL import Image
from io import BytesIO
from ebooklib import epub

def extract_text_from_pdf(file_stream):
    doc = fitz.open(stream=file_stream, filetype="pdf")
    pages_text = [page.get_text() for page in doc]
    return pages_text

def generate_pdf_ebook(pages_text, cover_image=None, page_size=A5, font_size=12, margins=(50, 50, 50, 50), line_spacing=1.2):
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=page_size)
    width, height = page_size
    left_margin, right_margin, top_margin, bottom_margin = margins
    textobject = c.beginText(left_margin, height - top_margin)
    textobject.setFont("Helvetica", font_size)

    if cover_image:
        img = Image.open(cover_image)
        img_width, img_height = img.size
        aspect = img_height / img_width
        new_width = width - left_margin - right_margin
        new_height = new_width * aspect
        img = img.resize((int(new_width), int(new_height)))
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        c.drawImage(ImageReader(img_buffer), left_margin, height - new_height - top_margin, width=new_width, height=new_height)
        c.showPage()
        textobject = c.beginText(left_margin, height - top_margin)
        textobject.setFont("Helvetica", font_size)

    chapters = []
    page_number = 1

    for page_text in pages_text:
        for line in page_text.split('\n'):
            if "CAPÍTULO" in line.upper():
                chapters.append((line.strip(), page_number))
                textobject.setFont("Helvetica-Bold", font_size + 2)
                textobject.textLine(line.strip())
                textobject.setFont("Helvetica", font_size)
            else:
                if textobject.getY() < bottom_margin:
                    c.drawText(textobject)
                    c.showPage()
                    textobject = c.beginText(left_margin, height - top_margin)
                    textobject.setFont("Helvetica", font_size)
                    page_number += 1
                textobject.textLine(line)
                textobject.moveCursor(0, -(font_size * line_spacing - font_size))

        c.drawText(textobject)
        c.showPage()
        textobject = c.beginText(left_margin, height - top_margin)
        textobject.setFont("Helvetica", font_size)
        page_number += 1

    c.setFont("Helvetica-Bold", font_size + 4)
    c.drawCentredString(width/2, height - top_margin, "Índice")
    c.setFont("Helvetica", font_size)
    y = height - top_margin*2

    for chapter_title, page_num in chapters:
        if y < bottom_margin:
            c.showPage()
            y = height - top_margin
        c.drawString(left_margin, y, f"{chapter_title} .......... {page_num}")
        y -= font_size + 6

    c.save()
    output.seek(0)
    return output

def generate_epub_ebook(pages_text, title="E-Book", author="Autor"):
    book = epub.EpubBook()
    book.set_title(title)
    book.set_language('pt')
    book.add_author(author)

    chapters = []
    for idx, page_text in enumerate(pages_text):
        chapter = epub.EpubHtml(title=f'Capítulo {idx+1}', file_name=f'chap_{idx+1}.xhtml', lang='pt')
        chapter.content = '<h1>Capítulo {}</h1><p>{}</p>'.format(idx+1, page_text.replace('\n', '<br>'))
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ['nav'] + chapters

    output = BytesIO()
    epub.write_epub(output, book)
    output.seek(0)
    return output