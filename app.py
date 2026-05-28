import streamlit as st
import requests
import base64

import base64

def get_logo_b64():
    with open("logo.png", "rb") as f:
        return base64.b64encode(f.read()).decode()

st.set_page_config(
    page_title="PulseIQ AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "https://kkgashx1cl.execute-api.us-east-1.amazonaws.com"

# ================= SESSION =================
defaults = {
    "selected_doc_name": None,
    "selected_doc_id": None,
    "selected_agent": "supervisor",
    "uploader_key": 0,
    "ai_answer": ""
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= CSS =================
st.markdown("""
<style>
header[data-testid="stHeader"]{background:transparent;}
#MainMenu, footer{visibility:hidden;}

html, body, [data-testid="stAppViewContainer"]{
    background:#f7f5fb;
    font-family:Inter, sans-serif;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background:#23003d !important;
    min-width:340px !important;
    max-width:340px !important;
    border-right:1px solid #3c165d;
}

/* titles */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:white !important;
}

/* FIXED TEXT COLORS */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span{
    color:#23003d!important;
}

/* logo */
.logo-title{
    font-size:34px;
    font-weight:800;
    color:white;
}

.logo-sub{
    font-size:13px;
    color:#dcc8f7;
    margin-top:6px;
}

/* SEARCH */
section[data-testid="stSidebar"] input{
    background:white !important;
    color:#23003d !important;
    border-radius:12px !important;
}

/* UPLOADER */
section[data-testid="stSidebar"] [data-testid="stFileUploader"]{
    background:white !important;
    border-radius:16px !important;
    padding:14px !important;
}

/* uploader text fix */
section[data-testid="stSidebar"] .stFileUploader label,
section[data-testid="stSidebar"] .stFileUploader span{
    color:#23003d !important;
}

/* BUTTONS */
section[data-testid="stSidebar"] .stButton > button{
    background:white !important;
    color:#23003d !important;
    border:none !important;
    border-radius:14px !important;
    font-weight:700 !important;
    height:46px !important;
}

section[data-testid="stSidebar"] .stButton > button:hover{
    background:#f2e8ff !important;
    color:#6b21a8 !important;
}

/* MAIN */
.block-container{
    padding-top:1rem;
    max-width:1500px;
}

.main-title{
    font-size:38px;
    font-weight:800;
    color:#23003d;
}

.main-sub{
    color:#6f6480;
    margin-bottom:24px;
    font-size:18px;
}

/* cards */
.agent-card{
    background:white;
    border:1px solid #eadcf8;
    border-radius:20px;
    padding:24px;
    height:260px;
}

.agent-title{
    font-size:18px;
    font-weight:800;
    color:#23003d;
}

.agent-desc{
    color:#655675;
}

/* selected button */
.stButton > button[kind="primary"]{
    background:linear-gradient(90deg,#6b21a8,#8b5cf6) !important;
    color:white !important;
}

/* answer */
.answer{
    background:white;
    border:1px solid #eadcf8;
    border-radius:18px;
    padding:24px;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# ================= DOCS =================
docs = []
try:
    r = requests.get(f"{API_BASE}/documents")
    if r.status_code == 200:
        docs = r.json()
except:
    docs = []

# ================= SIDEBAR =================

with st.sidebar:

    st.markdown("""
    <div style="display:flex; align-items:center; gap:14px; padding:10px 0 20px 0;">
        <img src="data:image/png;base64,{logo_b64}" width="64" style="border-radius:14px; flex-shrink:0;"/>
        <div>
            <div class="logo-title">PulseIQ AI</div>
            <div class="logo-sub">Turning Medical Records Into Clear Clinical Insight</div>
        </div>
    </div>
    """.format(logo_b64=get_logo_b64()), unsafe_allow_html=True)

    st.markdown("## Upload Record")

    uploaded = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key=f"up_{st.session_state.uploader_key}"
    )

    if uploaded:
        if st.button("Upload PDF", use_container_width=True):

            payload = {
                "file_name": uploaded.name,
                "file_data": base64.b64encode(uploaded.read()).decode()
            }

            rr = requests.post(f"{API_BASE}/upload", json=payload)

            if rr.status_code == 200:
                st.success("Uploaded")
                st.session_state.uploader_key += 1
                st.rerun()

    st.markdown("---")
    st.markdown("## Patient Library")

    search = st.text_input("Search Records")

    filtered = docs
    if search:
        filtered = [
            d for d in docs
            if search.lower() in d.get("file_name","").lower()
        ]

    for i, d in enumerate(filtered):
        fname = d.get("file_name","Document")
        docid = d.get("document_id","")

        if st.button(fname, key=f"doc_{i}", use_container_width=True):
            st.session_state.selected_doc_name = fname
            st.session_state.selected_doc_id = docid
            st.session_state.ai_answer = ""

# ================= MAIN =================
st.markdown('<div class="main-title">Clinical Intelligence Workspace</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Use specialized AI agents on one selected patient record at a time.</div>', unsafe_allow_html=True)

if st.session_state.selected_doc_name:
    st.success(f"Currently analyzing: {st.session_state.selected_doc_name}")
else:
    st.info("Select a patient document from the left sidebar.")

# ================= AGENTS =================
def choose(label, code, key):
    t = "primary" if st.session_state.selected_agent == code else "secondary"
    if st.button(label, key=key, type=t):
        st.session_state.selected_agent = code

c1,c2,c3,c4 = st.columns(4)

with c1: choose("Smart Consultant","supervisor","a1")
with c2: choose("Diagnosis Expert","qa","a2")
with c3: choose("Record Summarizer","summary","a3")
with c4: choose("Entity Extractor","coding","a4")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown('<div class="agent-card"><div class="agent-title">Smart Consultant</div><div class="agent-desc">Combines specialist reasoning for complete clinical insights.</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="agent-card"><div class="agent-title">Diagnosis Expert</div><div class="agent-desc">Answers disease, symptoms, findings and treatment questions.</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="agent-card"><div class="agent-title">Record Summarizer</div><div class="agent-desc">Creates concise summaries from lengthy medical records.</div></div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="agent-card"><div class="agent-title">Entity Extractor</div><div class="agent-desc">Extracts diagnoses, medications, symptoms and entities.</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================= QUESTION =================
question = st.text_area(
    "Question",
    placeholder="Ask a question about the selected patient record...",
    height=180,
    label_visibility="collapsed"
)

# ================= ASK =================
if st.button("Ask PulseIQ AI", use_container_width=True, type="primary"):

    if not st.session_state.selected_doc_id:
        st.warning("Select document first.")

    elif not question.strip():
        st.warning("Enter question first.")

    else:
        payload = {
            "question": question,
            "agent": st.session_state.selected_agent,
            "document_id": st.session_state.selected_doc_id
        }

        rr = requests.post(f"{API_BASE}/ask", json=payload)

        if rr.status_code == 200:
            st.session_state.ai_answer = rr.json()["answer"]

# ================= RESPONSE =================
def format_response(text):
    replacements = {
        "Diagnosis:": "### Diagnosis",
        "Supporting Evidence:": "### Supporting Evidence",
        "Confidence Level:": "### Confidence Level",
        "Patient Overview:": "### Patient Overview",
        "Key Findings:": "### Key Findings",
        "Recommended Actions:": "### Recommended Actions",
        "Diseases:": "### Diseases",
        "Symptoms:": "### Symptoms",
        "Medications:": "### Medications",
        "Tests:": "### Tests",
        "Clinical Insight:": "### Clinical Insight",
        "Possible Diagnoses:": "### Possible Diagnoses",
        "Recommended Next Steps:": "### Recommended Next Steps"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


if st.session_state.ai_answer:
    formatted = format_response(st.session_state.ai_answer)

    st.markdown(f"""
    <div class="answer">
        {formatted}
    </div>
    """, unsafe_allow_html=True)