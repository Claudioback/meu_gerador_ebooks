import streamlit as st
import time
import io
from fpdf import FPDF
from ebooklib import epub
from PIL import Image

# --- Estilo CSS customizado ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        border: None;
        font-weight: bold;
        margin: 5px;
    }
    .stSlider>div>div>div {
        background: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# --- Título principal ---
st.title("\U0001F4DA Gerador Avançado de E-Books")
st.write("Transforme seus PDFs em e-books formatados!")

# --- Upload de Arquivo ---
uploaded_file = st.file_uploader("Faça upload do seu PDF", type=["pdf"])

# --- Upload de Capa Opcional ---
uploaded_cover = st.file_uploader("Upload da imagem da capa (opcional)", type=["png", "jpg", "jpeg"])

# --- Parâmetros do E-Book ---
st.subheader("Configurações do E-Book")
page_size = st.selectbox("Tamanho da página", ["A4", "A5", "Carta"])
font_size = st.slider("Tamanho da fonte", 8, 24, 12)
line_spacing = st.slider("Espaçamento entre linhas", 1.0, 2.0, 1.2)

# --- Botão para Gerar ---
if uploaded_file is not None:
    if st.button("\U0001F680 Gerar E-Book"):
        st.info("Gerando seu e-book, aguarde...")
        progress_bar = st.progress(0)

        for perc in range(100):
            time.sleep(0.01)
            progress_bar.progress(perc + 1)

        # --- Simulando geração do e-book ---
        pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=font_size)
pdf.cell(200, 10, txt="Seu e-book gerado!", ln=True, align='C')

# Corrigido: gerar PDF como bytes
pdf_bytes = pdf.output(dest='S').encode('latin1')

# Criar botão para download
st.download_button(
    label="📄 Baixar E-book em PDF",
    data=pdf_bytes,
    file_name="meu_ebook.pdf",
    mime="application/pdf"
)



        epub_book = epub.EpubBook()
        epub_book.set_title('Meu E-Book')
        epub_book.set_language('pt')
        c1 = epub.EpubHtml(title='Introdução', file_name='intro.xhtml', lang='pt')
        c1.content = '<h1>Seu e-book gerado!</h1>'
        epub_book.add_item(c1)
        epub_book.spine = ['nav', c1]
        epub_output = io.BytesIO()
        epub.write_epub(epub_output, epub_book)

        st.success("\U0001F389 E-book gerado com sucesso! Obrigado por usar nosso app!")

        # --- Botões lado a lado ---
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="\U0001F4C4 Baixar PDF",
                data=pdf_output.getvalue(),
                file_name="meu_ebook.pdf",
                mime="application/pdf"
            )
        with col2:
            st.download_button(
                label="\U0001F4DA Baixar EPUB",
                data=epub_output.getvalue(),
                file_name="meu_ebook.epub",
                mime="application/epub+zip"
            )
else:
    st.warning("\u26a0\ufe0f Por favor, envie um arquivo PDF para começar.")


              
