import streamlit as st

from agent import ask_tutor
from memory import build_context


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ================================
   IMPORT FONT
================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* ================================
   GLOBAL
================================ */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(236, 72, 153, 0.13),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(139, 92, 246, 0.14),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(6, 182, 212, 0.08),
            transparent 30%
        ),
        #08070d;
    color: #f8f7ff;
}


/* ================================
   MAIN CONTAINER
================================ */

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ================================
   HEADER
================================ */

.hero {
    padding: 25px 0 15px 0;
}

.logo {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #f472b6;
    text-transform: uppercase;
}

.hero-title {
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    margin-top: 10px;
    margin-bottom: 12px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #f9a8d4,
        #c084fc,
        #67e8f9
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #aaa7bb;
    font-size: 16px;
    max-width: 650px;
    line-height: 1.7;
}


/* ================================
   STATUS BADGE
================================ */

.status {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    padding: 7px 13px;
    margin-top: 10px;

    border-radius: 999px;

    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.25);

    color: #86efac;
    font-size: 12px;
    font-weight: 600;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #4ade80;

    box-shadow:
        0 0 8px #4ade80,
        0 0 16px rgba(74, 222, 128, 0.5);
}


/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #100b17 0%,
            #0b0910 100%
        );

    border-right: 1px solid rgba(244, 114, 182, 0.12);
}

section[data-testid="stSidebar"] h2 {
    color: #f9a8d4;
}

section[data-testid="stSidebar"] label {
    color: #c7c3d1 !important;
}


/* ================================
   SETTINGS CARD
================================ */

.settings-card {
    padding: 18px;

    border-radius: 18px;

    background: rgba(255, 255, 255, 0.025);

    border: 1px solid rgba(255, 255, 255, 0.07);

    margin-bottom: 20px;
}


/* ================================
   CHAT MESSAGES
================================ */

[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.025);

    border: 1px solid rgba(255, 255, 255, 0.06);

    border-radius: 18px;

    padding: 12px 16px;

    margin-bottom: 12px;
}


/* Assistant message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    border-left: 2px solid #f472b6;

    box-shadow:
        0 0 20px rgba(236, 72, 153, 0.05);
}


/* User message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    border-right: 2px solid #8b5cf6;
}


/* ================================
   CHAT INPUT
================================ */

[data-testid="stChatInput"] {
    border-radius: 18px !important;
}

[data-testid="stChatInput"] textarea {
    background: rgba(20, 15, 28, 0.95) !important;

    border: 1px solid rgba(244, 114, 182, 0.25) !important;

    border-radius: 18px !important;

    color: white !important;

    transition: all 0.25s ease;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #f472b6 !important;

    box-shadow:
        0 0 0 1px #f472b6,
        0 0 25px rgba(244, 114, 182, 0.12) !important;
}


/* ================================
   BUTTONS
================================ */

.stButton > button {
    width: 100%;

    border-radius: 12px;

    border: 1px solid rgba(244, 114, 182, 0.25);

    background:
        linear-gradient(
            135deg,
            rgba(236, 72, 153, 0.12),
            rgba(139, 92, 246, 0.12)
        );

    color: #f9a8d4;

    font-weight: 600;

    transition: all 0.25s ease;
}

.stButton > button:hover {
    border-color: #f472b6;

    color: white;

    box-shadow:
        0 0 18px rgba(244, 114, 182, 0.18);

    transform: translateY(-1px);
}


/* ================================
   SELECT BOX
================================ */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.035);

    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.08);
}


/* ================================
   FEATURE CARDS
================================ */

.feature-card {
    padding: 20px;

    min-height: 145px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.045),
            rgba(255,255,255,0.015)
        );

    border: 1px solid rgba(255,255,255,0.07);

    transition: all 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-3px);

    border-color: rgba(244,114,182,0.25);

    box-shadow:
        0 10px 35px rgba(0,0,0,0.25);
}

.feature-icon {
    font-size: 24px;
    margin-bottom: 10px;
}

.feature-title {
    font-weight: 700;
    color: #f8f7ff;
}

.feature-text {
    color: #9894a5;
    font-size: 13px;
    line-height: 1.6;
}


/* ================================
   DIVIDER
================================ */

.neon-line {
    height: 1px;

    margin: 25px 0;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(244,114,182,0.5),
            rgba(139,92,246,0.5),
            transparent
        );
}


/* ================================
   MOBILE
================================ */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }

    .hero-title {
        font-size: 2.3rem;
    }

    .hero-subtitle {
        font-size: 14px;
    }

    .feature-card {
        margin-bottom: 12px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:24px;
            font-weight:800;
            margin-bottom:5px;
        ">
            ✦ StudyMate
        </div>

        <div style="
            color:#8f8a9d;
            font-size:13px;
            margin-bottom:25px;
        ">
            AI Study Companion
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Study Settings")

    subject = st.selectbox(
        "Subject",
        [
            "Computer Science",
            "Mathematics",
            "Physics",
            "English",
            "General"
        ]
    )

    level = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            color:#aaa7bb;
            font-size:12px;
            line-height:1.7;
        ">
        <b style="color:#f9a8d4;">AI Tutor</b><br>
        Ask questions, learn concepts,
        practice problems and create
        study plans.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑 Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="logo">
            ✦ STUDYMATE AI
        </div>

        <div class="hero-title">
            Learn smarter.<br>
            Understand deeper.
        </div>

        <div class="hero-subtitle">
            Your personal AI study tutor for understanding concepts,
            practicing questions and building better study habits.
        </div>

        <div class="status">
            <span class="status-dot"></span>
            AI Tutor Online
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FEATURE CARDS
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown("<div class='neon-line'></div>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">
                    Learn Concepts
                </div>
                <div class="feature-text">
                    Get difficult topics explained
                    in simple language with examples.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">
                    Practice
                </div>
                <div class="feature-text">
                    Test your understanding with
                    questions and guided practice.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">✦</div>
                <div class="feature-title">
                    Study Smarter
                </div>
                <div class="feature-text">
                    Create simple study plans and
                    get personalized guidance.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="✦" if message["role"] == "assistant" else "👤"
    ):

        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask anything you want to learn..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -------------------------
    # User message
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(question)


    # -------------------------
    # Previous context
    # -------------------------

    previous_context = build_context(
        st.session_state.messages
    )


    # -------------------------
    # Full prompt
    # -------------------------

    full_question = f"""
    Previous conversation:

    {previous_context}

    Current student question:

    {question}
    """


    # -------------------------
    # AI response
    # -------------------------

    with st.chat_message(
        "assistant",
        avatar="✦"
    ):

        with st.spinner("✦ Thinking..."):

            try:

                answer = ask_tutor(
                    full_question,
                    subject,
                    level
                )

                st.markdown(answer)

            except Exception as e:

                answer = (
                    "I couldn't process that request. "
                    "Please check your API configuration."
                )

                st.error(str(e))


    # -------------------------
    # Save response
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
