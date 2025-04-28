import streamlit as st
from fpdf import FPDF
from ebooklib import epub  # Agora está certo!
import io

# Configurações iniciais do app
st.set_page_config(page_title="Gerador de E-books", layout="centered", page_icon="📚")

st.title("📚 Magic Ebook")
st.write("Crie seu próprio e-book em poucos minutos!")

# Inputs do usuário
titulo = st.text_input("Título do E-book", value="Meu E-book")
autor = st.text_input("Autor", value="Autor Desconhecido")
conteudo = st.text_area("Conteúdo", height=300, placeholder="Digite ou cole aqui o texto do seu e-book...")

# Configurações adicionais
st.sidebar.header("⚙️ Configurações do Documento")
tamanho_fonte = st.sidebar.slider("Tamanho da Fonte", 8, 20, 12)
espacamento = st.sidebar.slider("Espaçamento entre Linhas", 1.0, 2.5, 1.5)

# Funções para gerar arquivos
def gerar_pdf(titulo, autor, conteudo, tamanho_fonte, espacamento):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=tamanho_fonte)

    pdf.multi_cell(0, 10 * espacamento, f"{titulo}\n\n{conteudo}")

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output

def gerar_epub(titulo, autor, conteudo):
    livro = epub.EpubBook()
    livro.set_title(titulo)
    livro.set_language('pt')
    livro.add_author(autor)

    c1 = epub.EpubHtml(title='Introdução', file_name='intro.xhtml', lang='pt')
    c1.content = f'<h1>{titulo}</h1><p>{conteudo}</p>'

    livro.add_item(c1)

    livro.toc = (epub.Link('intro.xhtml', 'Introdução', 'intro'),)

    livro.add_item(epub.EpubNcx())
    livro.add_item(epub.EpubNav())
    livro.spine = ['nav', c1]

    epub_output = io.BytesIO()
    epub.write_epub(epub_output, livro)
    epub_output.seek(0)

    return epub_output

# Botão de gerar e-book
if st.button("📖 Gerar E-book"):
    if titulo and conteudo:
        pdf_file = gerar_pdf(titulo, autor, conteudo, tamanho_fonte, espacamento)
        epub_file = gerar_epub(titulo, autor, conteudo)

        st.success("✅ E-book gerado com sucesso!")

        # Botões de download lado a lado
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="⬇️ Baixar PDF",
                data=pdf_file,
                file_name=f"{titulo}.pdf",
                mime="application/pdf"
            )

        with col2:
            st.download_button(
                label="⬇️ Baixar EPUB",
                data=epub_file,
                file_name=f"{titulo}.epub",
                mime="application/epub+zip"
            )
    else:
        st.error("❗Por favor, preencha o título e o conteúdo do e-book.")

# Rodapé bonito
st.markdown(
    """
    <hr style="margin-top:2em;margin-bottom:1em;">
    <center><sub>Desenvolvido com ❤️ por Claudio - 2025</sub></center>
    """,
    unsafe_allow_html=True
)
