import streamlit as st
from fpdf import FPDF
from ebooklib import epub
from docx import Document
import fitz  # PyMuPDF
import io
from PIL import Image

# Configurações iniciais
st.set_page_config(page_title="Gerador de E-book", page_icon="📚", layout="centered")

st.title("📚 Magic Ebook Creator")
st.write("Transforme seus documentos em e-books profissionais!")

# Upload do documento
st.header("📄 Envie seu documento")
arquivo = st.file_uploader("Escolha um arquivo (.docx ou .pdf)", type=["pdf", "docx"])

# Upload da capa
st.header("🎨 Envie uma imagem para a capa (opcional)")
capa_imagem = st.file_uploader("Imagem da capa (.jpg ou .png)", type=["jpg", "png"])

# Inputs de dados
st.header("✍️ Informações do E-book")
titulo = st.text_input("Título do E-book", value="Meu E-book Incrível")
autor = st.text_input("Autor", value="Autor Desconhecido")
tamanho_fonte = st.slider("Tamanho da Fonte", 10, 24, 14)
espacamento = st.slider("Espaçamento entre linhas", 1.0, 2.5, 1.5)

# Funções auxiliares
def extrair_texto_docx(file):
    doc = docx.Document(file)
    texto = "\n".join([par.text for par in doc.paragraphs])
    return texto

def extrair_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

def gerar_epub(titulo, autor, conteudo, imagem_capa=None):
    livro = epub.EpubBook()
    livro.set_title(titulo)
    livro.set_language('pt')
    livro.add_author(autor)

    if imagem_capa:
        imagem_bytes = imagem_capa.read()
        livro.set_cover("cover.jpg", imagem_bytes)

    c1 = epub.EpubHtml(title='Conteúdo', file_name='conteudo.xhtml', lang='pt')
    c1.content = f'<h1>{titulo}</h1><p>{conteudo.replace("\n", "<br>")}</p>'
    livro.add_item(c1)

    livro.add_item(epub.EpubNcx())
    livro.add_item(epub.EpubNav())
    livro.spine = ['cover', 'nav', c1]

    epub_output = io.BytesIO()
    epub.write_epub(epub_output, livro)
    epub_output.seek(0)

    return epub_output

# Botão de gerar E-book
if st.button("🚀 Gerar E-book"):
    if not arquivo:
        st.error("❗ Por favor, envie um documento.")
    else:
        with st.spinner('⏳ Gerando seu E-book, aguarde...'):

            # Extrair texto
            if arquivo.name.endswith(".docx"):
                conteudo = extrair_texto_docx(arquivo)
            elif arquivo.name.endswith(".pdf"):
                conteudo = extrair_texto_pdf(arquivo)
            else:
                st.error("❗ Formato de arquivo não suportado.")
                st.stop()

            if not conteudo.strip():
                st.error("❗ Não foi possível extrair texto do documento.")
                st.stop()

            # Gerar EPUB
            epub_file = gerar_epub(titulo, autor, conteudo, imagem_capa=capa_imagem)

            st.success("✅ E-book gerado com sucesso!")

            # Botão de download
            st.download_button(
                label="⬇️ Baixar EPUB",
                data=epub_file,
                file_name=f"{titulo}.epub",
                mime="application/epub+zip"
            )

# Rodapé
st.markdown("""
<hr style="margin-top: 2em; margin-bottom: 1em;">
<center><sub>Desenvolvido com ❤️ por Claudio - 2025</sub></center>
""", unsafe_allow_html=True)
