import os
import streamlit as st
import streamlit.components.v1 as components
import json

HISTORY_FILE = "chat_history.json"
MESSAGES_FILE = "chat_messages.json"

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_messages(messages):
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# =========================================================
# VALIDATION CONFIG
# =========================================================
ALLOWED_KEYWORDS = [
    "jasa", "produk", "bisnis", "usaha", "brand",
    "toko", "layanan", "service", "agency",
    "marketing", "seo", "digital", "online",
    "website", "aplikasi", "skincare", "makanan",
    "travel", "tour", "konstruksi", "renovasi"
]

INVALID_CONTEXT_RESPONSE = """
Input Anda belum sesuai dengan konteks **Search Engine Assistant**,
Silakan masukkan topik **Produk, Jasa, atau Bisnis**.

Contoh Inputan: Jasa renovasi rumah, Produk skincare anti aging, Jasa pembuatan website UMKM, Travel umroh terpercaya

Gunakan kata benda atau frasa singkat (bukan pertanyaan).
"""


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Digital Marketing AI",
    page_icon=None,
    layout="wide",
)

# =========================================================
# API KEY INPUT – SCOPED STYLING (DIBIARKAN)
# =========================================================
st.markdown("""
<style>
.api-key-wrapper {
    max-width: 420px;
    margin: 140px auto 0 auto;
    text-align: left;
}

.api-key-wrapper input {
    max-width: 420px !important;
    width: 420px !important;
}

.api-key-wrapper label {
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# GROQ API KEY CHECK
# =========================================================
if "GROQ_API_KEY" not in os.environ:
    st.markdown('<div class="api-key-wrapper">', unsafe_allow_html=True)

    st.markdown("### 🔐 Masukkan Groq API Key")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_************************"
    )

    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        st.success("API key saved. Reloading app...")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

from llm import generate_marketing_content

def is_marketing_context(prompt: str) -> bool:
    prompt = prompt.lower().strip()

    if len(prompt) > 80:
        return False

    forbidden_patterns = [
        "import ", "def ", "{", "}", "<", ">", 
        "http", "www", "pip install", "SELECT "
    ]
    if any(p in prompt for p in forbidden_patterns):
        return False

    return any(keyword in prompt for keyword in ALLOWED_KEYWORDS)


def format_marketing_response(text: str) -> str:
    text = text.replace("**", "").strip()

    sections = [
        "SEO_TITLE",
        "META_DESCRIPTION",
        "FOCUS_KEYWORD",
        "SECONDARY_KEYWORDS",
        "HASHTAGS",
        "CTA",
        "CONTENT_SNIPPET",
    ]

    blocks = ""

    for idx, section in enumerate(sections):
        if f"{section}:" in text:
            part = text.split(f"{section}:")[1]
            for s in sections:
                if s != section and f"{s}:" in part:
                    part = part.split(f"{s}:")[0]

            content = part.strip()
            title = section.replace("_", " ").title()
            element_id = f"copy-{idx}"

            blocks += f"""
            <div style="margin-bottom:20px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <div style="
                        font-size:12px;
                        font-weight:600;
                        letter-spacing:0.4px;
                        text-transform:uppercase;
                        color:#facc15;
                    ">
                        {title}
                    </div>

                 <button
                    onclick="
                        navigator.clipboard.writeText(
                            document.getElementById('{element_id}').innerText
                        ).then(() => {{
                            const originalText = this.innerHTML;
                            const originalBg = this.style.background;
                            const originalBorder = this.style.borderColor;

                            this.innerHTML = '✓ Copied';
                            this.style.background = 'rgba(34,197,94,0.25)';
                            this.style.borderColor = 'rgba(34,197,94,0.6)';

                            setTimeout(() => {{
                                this.innerHTML = originalText;
                                this.style.background = originalBg;
                                this.style.borderColor = originalBorder;
                            }}, 1500);
                        }});
                                "
                                style="
                                    display:flex;
                                    align-items:center;
                                    gap:6px;
                                    padding:4px 10px;
                                    font-size:12px;
                                    font-weight:500;
                                    color:#e6e7eb;
                                    background:rgba(255,255,255,0.04);
                                    border:1px solid rgba(255,255,255,0.08);
                                    border-radius:999px;
                                    cursor:pointer;

                                    transition:
                                        background 0.2s ease,
                                        border-color 0.2s ease,
                                        transform 0.1s ease,
                                        box-shadow 0.1s ease;
                                "
                                onmouseover="this.style.background='rgba(255,255,255,0.12)';
                                            this.style.borderColor='rgba(255,255,255,0.25)'"
                                onmouseout="this.style.background='rgba(255,255,255,0.04)';
                                            this.style.borderColor='rgba(255,255,255,0.08)';
                                            this.style.transform='scale(1)';
                                            this.style.boxShadow='none'"
                                onmousedown="this.style.transform='scale(0.96)';
                                            this.style.boxShadow='0 2px 8px rgba(0,0,0,0.25)'"
                                onmouseup="this.style.transform='scale(1)'"
                            >
                                ⧉ Copy
                            </button>
                        </div>
                        <div id="{element_id}" style="
                            font-size:14px;
                            line-height:1.65;
                            color:#e6e7eb;
                        ">
                            {content}
                    </div>
            </div>
            """

    return f"""
    <div style="
        background:linear-gradient(180deg,#1b1f33,#171a2b);
        border-radius:16px;
        padding:20px 22px;
        border:1px solid rgba(255,255,255,0.04);
        box-shadow:0 4px 18px rgba(0,0,0,0.28);
        font-family:Manrope,system-ui;
    ">
        {blocks}
    </div>
    """

# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = load_history()

if "messages" not in st.session_state:
    st.session_state.messages = load_messages()

has_interaction = len(st.session_state.messages) > 0

# =========================================================
# INPUT POSITION
# =========================================================
input_position_css = """
div[data-testid="stChatInput"] {
    position: relative;
    max-width: 640px;
    margin: 36px auto 0 auto;
}
""" if not has_interaction else """
div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 28px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 760px;
    width: 100%;
    z-index: 100;
}
"""

# =========================================================
# GLOBAL STYLES
# =========================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap');

            
/* ===== HIDE STREAMLIT SIDEBAR ===== */
# section[data-testid="stSidebar"] {{
#     display: none;
# }}

# div[data-testid="stSidebarNav"] {{
#     display: none;
# }}

# button[data-testid="baseButton-header"] {{
#     display: none;
# }}
/* ================================= */
            

/* ===== SIDEBAR SCROLLABLE & RESPONSIVE ===== */
section[data-testid="stSidebar"] {{
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 280px;

    overflow-y: auto;
    overflow-x: hidden;

    background: linear-gradient(180deg,#1b1f33,#171a2b);
    border-right: 1px solid rgba(255,255,255,0.06);
    z-index: 100;
}}

section[data-testid="stSidebar"] > div {{
    padding: 20px 16px 40px 16px;
}}

/* scrollbar */
section[data-testid="stSidebar"]::-webkit-scrollbar {{
    width: 6px;
}}

section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {{
    background: rgba(255,255,255,0.25);
    border-radius: 8px;
}}

section[data-testid="stSidebar"] {{
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.25) transparent;
}}

/* mobile */
@media (max-width: 768px) {{
    section[data-testid="stSidebar"] {{
        width: 78vw;
        min-width: 240px;
        max-width: 300px;
    }}
}}

/* ===== APP BASE ===== */
.stApp {{
    color: #e8e8e8;
    font-family: Manrope, system-ui;
}}

header, footer {{ display:none; }}

.block-container {{
    max-width:760px;
    margin:0 auto;
    padding-top:{ "150px" if not has_interaction else "72px" };
    padding-bottom:200px;
}}

/* ===== CHAT CLEANUP ===== */
div[data-testid="stChatMessageAvatar"] {{
    display: none !important;
}}

div[data-testid="stChatMessageContent"] {{
    margin-left: 0 !important;
}}
/* ================================= */

/* ===== BATASI LEBAR INPUT API KEY ===== */
div[data-testid="stTextInput"] {{
    max-width: 420px;
    margin-left: auto;
    margin-right: auto;
}}

div[data-testid="stTextInput"] input {{
    width: 100% !important;
}}

/* ===== HILANGKAN ICON MATA PASSWORD ===== */
div[data-testid="stTextInput"] button {{
    display: none !important;
}}

/* ===== HILANGKAN ICON / AVATAR CHAT ===== */
div[data-testid="stChatMessageAvatar"] {{
    display: none !important;
}}

div[data-testid="stChatMessageContent"] {{
    margin-left: 0 !important;
}}
/* ================================= */

.stApp {{
    color: #e8e8e8;
    font-family: Manrope, system-ui;
}}

header, footer {{ display:none; }}

.block-container {{
    max-width:760px;
    margin:0 auto;
    padding-top:{ "150px" if not has_interaction else "72px" };
    padding-bottom:200px;
    text-align:{ "center" if not has_interaction else "left" };
}}

.hero-title {{
    font-size:42px;
    font-weight:700;
    letter-spacing:-0.6px;
    line-height:1.15;
    margin-bottom:14px;
}}

.hero-highlight {{
    background:linear-gradient(transparent 62%, rgba(250,204,21,.45) 62%);
    padding:0 6px;
}}

.hero-muted {{ color:#c7c9d3; }}

.hero-subtitle {{
    font-size:16px;
    line-height:1.7;
    color:#a1a1aa;
    max-width:580px;
    margin:0 auto;
}}

.hero-link {{
    color:#a1a1aa;
    text-decoration:none;
    font-weight:500;
}}

.chat-user {{
    max-width:68%;
    margin-left:auto;
    padding:8px 12px;
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:10px;
}}

div[data-testid="stChatMessage"] {{
    background:transparent!important;
    padding:6px 0!important;
}}

div[data-testid="stChatInput"] textarea {{
    border-radius:14px;
    padding:14px 16px;
    font-size:14px;
    color:#fff;
}}

{input_position_css}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================
if not has_interaction:
    st.markdown("""
    <div class="hero-title">
        <span class="hero-highlight">🕵🏼‍♂️ Search Engine</span>
        <span class="hero-muted">Assistant</span>
    </div>

    <div class="hero-subtitle">
        Asisten AI untuk memberikan referensi <b>SEO Title</b>, <b>Meta Description</b>,
        <b>Hashtag</b>, dan <b>CTA</b> secara instan dalam satu input.
        <br><br>
        👾 <a href="https://www.jendelakode.com/" target="_blank" class="hero-link">
       Jendela Kode</a>
        <br><br>
                Contoh Input : <br>
        • Jasa renovasi rumah<br>
        • Produk skincare<br>
        • Jasa pembuatan website
    </div>
    """, unsafe_allow_html=True)


with st.sidebar:
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown("## 🕘 History")

    with col2:
        if st.button("🗑️", key="delete-history", help="Hapus semua history"):
            # Hapus history dan messages
            st.session_state.history = []
            st.session_state.messages = []

            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            if os.path.exists(MESSAGES_FILE):
                os.remove(MESSAGES_FILE)

            st.success("History berhasil dihapus!")
            st.rerun()  # <-- gunakan ini di Streamlit terbaru

        # Styling tombol minimalis
        st.markdown("""
        <style>
        div[data-testid="stSidebar"] button[kind="primary"] {
            padding:4px !important;
            font-size:14px !important;
            width:32px !important;
            height:32px !important;
            border-radius:20% !important;
            background-color:rgba(255,75,75,0.12) !important;
            color:#ff4b4b !important;
            border:none !important;
            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
            transition: all 0.2s !important;
        }
        div[data-testid="stSidebar"] button[kind="primary"]:hover {
            background-color: rgba(255,75,75,0.25) !important;
            transform: scale(1.1) !important;
        }
        @media (max-width: 768px) {
            div[data-testid="stSidebar"] button[kind="primary"] {
                width:32px !important;
                height:32px !important;
                font-size:14px !important;
                padding:4px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        # Python side: cek klik tombol
        if st.session_state.get("delete_history_click"):
            st.session_state.history = []
            st.session_state.messages = []

            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            if os.path.exists(MESSAGES_FILE):
                os.remove(MESSAGES_FILE)

            st.success("History berhasil dihapus!")
            st.session_state._rerun()



    # Tampilkan history
    if not st.session_state.history:
        st.caption("Belum ada history")

    else:
         for idx, item in enumerate(st.session_state.history):
            if st.button(item, key=f"history-{idx}", use_container_width=True):
                # LOAD MESSAGES YANG SESUAI DENGAN HISTORY ITEM
                all_messages = load_messages()  # semua pesan
                # filter messages sampai terakhir kali user input sama dengan history
                messages_for_item = []
                for msg in all_messages:
                    messages_for_item.append(msg)
                    if msg["role"] == "user" and msg["content"] == item:
                        break

                st.session_state.messages = messages_for_item
                st.rerun()




# =========================================================
# CHAT HISTORY
# =========================================================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):

            # JIKA PESAN VALIDASI → TAMPILKAN TEKS BIASA
            if msg.get("type") == "validation":
                st.markdown(msg["content"])

            # JIKA OUTPUT AI → TAMPILKAN CARD SEO
            else:
                components.html(
                    format_marketing_response(msg["content"]),
                    height=520,
                    scrolling=True
                )

# =========================================================
# INPUT
# =========================================================
prompt = st.chat_input(
    "Contoh: jasa renovasi rumah, produk skincare, jasa pembuatan website…"
)

if prompt:
    # simpan user message
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    save_messages(st.session_state.messages)  # simpan ke file

    # simpan ke sidebar history (hindari duplikat)
    if prompt not in st.session_state.history:
        st.session_state.history.insert(0, prompt)
        save_history(st.session_state.history)

    # validasi konteks
    if not is_marketing_context(prompt):
        validation_msg = {
            "role": "assistant",
            "type": "validation",
            "content": INVALID_CONTEXT_RESPONSE
        }
        st.session_state.messages.append(validation_msg)
        save_messages(st.session_state.messages)  # simpan validation
        st.rerun()

    # generate konten marketing
    with st.spinner("Generating marketing content..."):
        response = generate_marketing_content(prompt)

    ai_msg = {"role": "assistant", "content": response}
    st.session_state.messages.append(ai_msg)
    save_messages(st.session_state.messages)  # simpan AI message
    st.rerun()


