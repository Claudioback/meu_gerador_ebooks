import streamlit as st
from utils import extract_text_from_pdf, generate_pdf_ebook, generate_epub_ebook
from reportlab.lib.pagesizes import A5, letter
from style import set_theme

# Tema
mode = st.radio("🌗 Escolha o tema:", ["Claro", "Escuro"])
set_theme(mode.lower())

st.title("📚 Gerador Avançado de E-Books")

uploaded_pdf = st.file_uploader("📄 Faça upload do seu PDF", type=["pdf"])
uploaded_cover = st.file_uploader("🖼️ Faça upload da imagem da capa (opcional)", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns(2)
with col1:
    page_size_option = st.selectbox("🗒️ Tamanho da página", ["A5 (livro)", "Carta (padrão)"])
    font_size = st.slider("🔤 Tamanho da fonte", 8, 24, 12)
with col2:
    line_spacing = st.slider("📏 Espaçamento entre linhas", 1.0, 2.0, 1.2)

st.subheader("Margens (em pontos)")
left_margin = st.slider("⬅️ Margem esquerda", 30, 100, 50)
right_margin = st.slider("➡️ Margem direita", 30, 100, 50)
top_margin = st.slider("⬆️ Margem superior", 30, 100, 50)
bottom_margin = st.slider("⬇️ Margem inferior", 30, 100, 50)

output_format = st.selectbox("📂 Formato de saída:", ["PDF", "EPUB"])

if uploaded_pdf is not None:
    pages_text = extract_text_from_pdf(uploaded_pdf)

    if st.button("🚀 Gerar E-Book"):
        page_size = A5 if page_size_option == "A5 (livro)" else letter
        margins = (left_margin, right_margin, top_margin, bottom_margin)

        if output_format == "PDF":
            ebook = generate_pdf_ebook(
                pages_text=pages_text,
                cover_image=uploaded_cover,
                page_size=page_size,
                font_size=font_size,
                margins=margins,
                line_spacing=line_spacing
            )
            file_name = "ebook_formatado.pdf"
            mime_type = "application/pdf"
        else:
            ebook = generate_epub_ebook(
                pages_text=pages_text,
                title="Meu Livro",
                author="Autor Desconhecido"
            )
            file_name = "ebook_formatado.epub"
            mime_type = "application/epub+zip"

        st.success(f"{output_format} gerado com sucesso!")
        st.download_button(
            label=f"📥 Baixar {output_format}",
            data=ebook,
            file_name=file_name,
            mime=mime_type
        )