import streamlit as st
import pandas as pd
import re

# Injeta CSS customizado para estilo elegante, sóbrio e neutro
st.markdown(
    """
    <style>
    /* Fonte principal, cores e espaçamentos */
    .title {
        color: #222222; /* cinza escuro quase preto */
        font-family: 'Georgia', serif;
        font-size: 38px;
        font-weight: 600;
        margin-bottom: 0.3em;
    }
    .subtitle {
        color: #555555; /* cinza médio */
        font-family: 'Georgia', serif;
        font-size: 20px;
        margin-bottom: 1em;
    }
    label {
        font-weight: 500;
        font-family: 'Georgia', serif;
        color: #222222;
    }
    .stApp {
        background-color: #FAFAFA; /* quase branco */
        color: #222222;
        padding: 1.5rem 2rem;
        max-width: 900px;
        margin: auto;
    }
    div.row-widget.stTextInput > label {
        font-weight: 500;
        margin-bottom: 0.1rem;
        display: block;
    }
    /* Ajustes para mensagens de sucesso e erro */
    .stSuccess {
        color: #1A3E5D !important; /* azul escuro */
        font-weight: 600;
    }
    .stError {
        color: #8B0000 !important; /* vermelho escuro */
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título e descrição
st.markdown('<h1 class="title">Artwork Inventory Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Please fill out the form below to register a new artwork.</p>', unsafe_allow_html=True)

# Validação simplificada
def validate_year(value):
    return bool(re.match(r"^\d{4}(-\d{4})?$", value.strip()))

def validate_dimensions(value):
    return bool(re.match(r"^\d+(\.\d+)?x\d+(\.\d+)?\s?cm$", value.strip().lower()))

def validate_location(value):
    return value.replace(" ", "").isalpha() and value.istitle()

# Formulário organizado em colunas
with st.form("artwork_form"):
    col1, col2 = st.columns(2)
    with col1:
        registry = st.text_input("Inventory/Registry Number")
        artist = st.text_input("Artist/Author")
        technique = st.text_input("Technique/Materials")
        location = st.text_input("Place of Production")
    with col2:
        title = st.text_input("Title of the Artwork")
        year = st.text_input("Year or Period of Creation (e.g. 1990 or 1980-1990)")
        dimensions = st.text_input("Dimensions (e.g. 30x40 cm)")
        provenance = st.text_input("Provenance/History")

    submit = st.form_submit_button("Submit")

# Inicializar lista na sessão
if "entries" not in st.session_state:
    st.session_state["entries"] = []

# Processar submissão com mensagens elegantes
if submit:
    errors = []
    if not validate_year(year):
        errors.append("⚠️ 'Year or Period of Creation' must be in the format '1990' or '1980-1990'.")
    if not validate_dimensions(dimensions):
        errors.append("⚠️ 'Dimensions' must be in the format '30x40 cm'.")
    if not validate_location(location):
        errors.append("⚠️ 'Place of Production' must contain only letters and start with a capital letter.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        artwork = {
            "Inventory Number": registry,
            "Title": title,
            "Artist": artist,
            "Year/Period": year,
            "Technique": technique,
            "Dimensions": dimensions,
            "Place of Production": location,
            "Provenance/History": provenance
        }
        st.session_state["entries"].append(artwork)
        st.success("✅ Artwork successfully registered!")

# Exibir inventário com título
if st.session_state["entries"]:
    st.markdown('<h2 style="color:#222222; font-family:Georgia, serif; margin-top: 2rem;">Registered Artworks</h2>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state["entries"])
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv, file_name="a
