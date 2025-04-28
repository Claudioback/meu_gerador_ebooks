import streamlit as st
import io
from fpdf import FPDF
import ebooklib
from ebooklib import epub

# Funções para gerar PDF
def gerar_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, texto)
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return output

# Funções para gerar EPUB
def gerar_epub(texto):
    book = epub.EpubBook()
    book.set_title('Meu E-Book')
    book.set_language('pt')

    c1 = epub.EpubHtml(title='Introdução', file_name='intro.xhtml', lang='pt')
    c1.content = f'<h1>{texto}</h1>'

    book.add_item(c1)
    book.spine = ['nav', c1]

    output = io.BytesIO()
    epub.write_epub(output, book)
    output.seek(0)
    return output

# Interface do Streamlit
st.title("Gerador de E-book 📚")

texto = st.text_area("Escreva o conteúdo do seu e-book:", height=200)

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Baixar como PDF"):
        if texto:
            pdf_bytes = gerar_pdf(texto)
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="meu_ebook.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF gerado com sucesso!")
        else:
            st.error("⚠️ Escreva algum conteúdo primeiro.")

with col2:
    if st.button("📚 Baixar como EPUB"):
        if texto:
            epub_bytes = gerar_epub(texto)
            st.download_button(
                label="📥 Download EPUB",
                data=epub_bytes,
                file_name="meu_ebook.epub",
                mime="application/epub+zip"
            )
            st.success("✅ EPUB gerado com sucesso!")
        else:
            st.error("⚠️ Escreva algum conteúdo primeiro.")

              
