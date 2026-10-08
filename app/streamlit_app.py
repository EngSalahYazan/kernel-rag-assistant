from __future__ import annotations

import base64

import streamlit as st

from kernel_rag.bootstrap import build_pipeline
from kernel_rag.exceptions import ConfigurationError, KnowledgeBaseNotReadyError

# UI VERSION: ART_DECO_V2_NO_VERTICAL_LABEL

st.set_page_config(
    page_title="Kernel Knowledge Assistant",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource
def get_pipeline():
    return build_pipeline()


ART_DECO_AI_SVG = r"""
<svg width="620" height="560" viewBox="0 0 620 560" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="coat" x1="180" y1="120" x2="470" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F6EEDF"/>
      <stop offset="0.42" stop-color="#D8D3E7"/>
      <stop offset="1" stop-color="#91A8FF"/>
    </linearGradient>
    <linearGradient id="shadow" x1="300" y1="100" x2="420" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#16214E"/>
      <stop offset="1" stop-color="#070B16"/>
    </linearGradient>
    <linearGradient id="magenta" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF315D"/>
      <stop offset="1" stop-color="#C71FFF"/>
    </linearGradient>
    <linearGradient id="blue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#36B8FF"/>
      <stop offset="1" stop-color="#3C36FF"/>
    </linearGradient>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>
  </defs>

  <!-- architectural rays -->
  <path d="M16 446L212 178L230 196L60 498L16 446Z" fill="#2850FF" fill-opacity=".32"/>
  <path d="M604 86L398 246L382 226L558 62L604 86Z" fill="#FF2F79" fill-opacity=".24"/>
  <path d="M5 170L198 255L186 280L0 229L5 170Z" fill="#655DFF" fill-opacity=".18"/>
  <path d="M614 286L429 324L427 298L620 229L614 286Z" fill="#1F6CFF" fill-opacity=".16"/>

  <!-- concentric art-deco arches -->
  <path d="M112 512V174C112 103 171 46 244 46H380C453 46 512 103 512 174V512" stroke="#5D6CFF" stroke-opacity=".22" stroke-width="2"/>
  <path d="M148 512V190C148 130 198 82 259 82H365C426 82 476 130 476 190V512" stroke="#FF3A70" stroke-opacity=".19" stroke-width="2"/>
  <path d="M184 512V206C184 157 225 118 275 118H349C399 118 440 157 440 206V512" stroke="#F5E7C8" stroke-opacity=".13" stroke-width="2"/>

  <!-- ambient lights -->
  <circle cx="150" cy="184" r="54" fill="#1A57FF" fill-opacity=".22" filter="url(#softGlow)"/>
  <circle cx="470" cy="152" r="62" fill="#FF2E72" fill-opacity=".18" filter="url(#softGlow)"/>

  <!-- head / mask -->
  <path d="M273 113L323 91L370 122L363 207L321 239L276 207L273 113Z" fill="#E6E2F2"/>
  <path d="M323 91L370 122L363 207L321 239V91H323Z" fill="#A8B8F5"/>
  <path d="M294 133L318 124L318 164L291 168L294 133Z" fill="#101A3B"/>
  <path d="M328 123L351 132L354 167L328 164V123Z" fill="#101A3B"/>
  <path d="M299 143L315 138" stroke="#5FD5FF" stroke-width="4" stroke-linecap="round"/>
  <path d="M333 138L348 144" stroke="#FF577F" stroke-width="4" stroke-linecap="round"/>
  <path d="M307 190L321 199L337 190" stroke="#7C85C8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M282 106L316 78L356 94L374 122L325 105L282 106Z" fill="#11172F"/>
  <path d="M316 78L351 91L337 108L321 104L316 78Z" fill="#FF315D"/>

  <!-- neck -->
  <path d="M294 222H347L354 272H286L294 222Z" fill="#E8E4ED"/>
  <path d="M321 222H347L354 272H321V222Z" fill="#9FACDE"/>

  <!-- dramatic art-deco shoulders / coat -->
  <path d="M286 253L207 280L150 520H307L321 276L286 253Z" fill="url(#coat)"/>
  <path d="M354 253L434 281L491 520H335L321 276L354 253Z" fill="#CDD3FB"/>
  <path d="M354 253L434 281L491 520H411L321 276L354 253Z" fill="url(#shadow)"/>

  <!-- collar -->
  <path d="M286 253L321 276L289 327L245 277L286 253Z" fill="#10162E"/>
  <path d="M354 253L321 276L355 327L399 278L354 253Z" fill="#141B3A"/>
  <path d="M306 272L321 285L336 272L329 364H313L306 272Z" fill="url(#magenta)"/>

  <!-- central deco panel -->
  <path d="M307 364H335L366 520H276L307 364Z" fill="#0D1430"/>
  <path d="M321 382L342 458L321 490L300 458L321 382Z" fill="url(#blue)" fill-opacity=".9"/>

  <!-- coat facets -->
  <path d="M207 280L284 252L250 520H151L207 280Z" fill="#FFFFFF" fill-opacity=".12"/>
  <path d="M435 281L356 253L410 520H492L435 281Z" fill="#283671" fill-opacity=".66"/>

  <!-- deco pins -->
  <circle cx="244" cy="327" r="6" fill="#FF315D"/>
  <circle cx="398" cy="329" r="6" fill="#49BEFF"/>

  <!-- floor / city motif -->
  <path d="M45 520H575" stroke="#E9D9B6" stroke-opacity=".28" stroke-width="2"/>
  <path d="M83 520V471H113V520" stroke="#355BFF" stroke-opacity=".32" stroke-width="2"/>
  <path d="M521 520V454H551V520" stroke="#FF3A70" stroke-opacity=".28" stroke-width="2"/>
  <path d="M120 520V431H141V520" stroke="#9A85FF" stroke-opacity=".22" stroke-width="2"/>
  <path d="M490 520V409H510V520" stroke="#345FFF" stroke-opacity=".23" stroke-width="2"/>
</svg>
""".strip()

ART_DECO_AI_URI = "data:image/svg+xml;base64," + base64.b64encode(
    ART_DECO_AI_SVG.encode("utf-8")
).decode("ascii")


def inject_css() -> None:
    st.markdown(
        r"""
<style>
:root {
    --ink: #05070d;
    --night: #08111f;
    --navy: #0c1a36;
    --cobalt: #314dff;
    --electric: #65c8ff;
    --kernel-red: #ff3f55;
    --magenta: #d92dff;
    --ivory: #f5eedf;
    --cream: #e9dcc2;
    --muted: #9ba7c2;
    --hairline: rgba(245, 238, 223, 0.14);
}

/* ---------- page ---------- */
.stApp {
    color: var(--ivory);
    background:
        linear-gradient(118deg, rgba(49,77,255,.12) 0 1px, transparent 1px 14%),
        linear-gradient(62deg, rgba(255,63,85,.06) 0 1px, transparent 1px 18%),
        radial-gradient(circle at 91% 9%, rgba(217,45,255,.13), transparent 22%),
        radial-gradient(circle at 8% 20%, rgba(49,77,255,.17), transparent 26%),
        linear-gradient(180deg, #05070d 0%, #07101d 44%, #050810 100%);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: .22;
    background-image:
        linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.015) 1px, transparent 1px);
    background-size: 46px 46px;
    mask-image: linear-gradient(to bottom, black 0%, transparent 76%);
}

.main .block-container {
    position: relative;
    z-index: 1;
    max-width: 1380px;
    padding: 1.35rem 2rem 7rem;
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: rgba(5,7,13,.86); }

/* ---------- hero ---------- */
.deco-hero-copy {
    position: relative;
    min-height: 470px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 3.5rem 2.2rem 3rem 2.3rem;
    overflow: hidden;
}

.deco-hero-copy::before {
    content: "";
    position: absolute;
    left: 0;
    top: 12%;
    width: 2px;
    height: 76%;
    background: linear-gradient(transparent, var(--kernel-red), #6c61ff, transparent);
}

.deco-hero-copy::after {
    content: "";
    position: absolute;
    left: 0;
    top: 12%;
    width: 46%;
    height: 1px;
    background: linear-gradient(90deg, rgba(245,238,223,.65), transparent);
}

.kernel-mark {
    display: inline-flex;
    width: fit-content;
    align-items: flex-end;
    gap: .08rem;
    margin-bottom: 2.25rem;
    color: var(--ivory);
    font-size: 1.35rem;
    font-weight: 900;
    letter-spacing: -.055em;
}
.kernel-mark .dot {
    width: .32rem;
    height: .32rem;
    margin-bottom: .25rem;
    border-radius: 50%;
    background: var(--kernel-red);
    box-shadow: 0 0 18px rgba(255,63,85,.7);
}

.deco-eyebrow {
    display: flex;
    align-items: center;
    gap: .85rem;
    margin-bottom: 1rem;
    color: #b8c8ff;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .22em;
    text-transform: uppercase;
}
.deco-eyebrow::before,
.deco-eyebrow::after {
    content: "";
    display: block;
    width: 35px;
    height: 1px;
    background: linear-gradient(90deg, var(--kernel-red), var(--cobalt));
}

.deco-title {
    max-width: 760px;
    margin: 0;
    color: var(--ivory);
    font-size: clamp(3.4rem, 6.5vw, 6.8rem);
    line-height: .86;
    font-weight: 900;
    letter-spacing: -.073em;
    text-wrap: balance;
    text-shadow: 0 12px 50px rgba(0,0,0,.36);
}

.deco-title .accent {
    color: transparent;
    -webkit-text-stroke: 1px rgba(245,238,223,.78);
    text-shadow: none;
}

.deco-rule {
    display: flex;
    align-items: center;
    gap: 12px;
    width: min(420px, 86%);
    margin-top: 1.75rem;
}
.deco-rule .line-a { height: 2px; flex: 1; background: linear-gradient(90deg, var(--kernel-red), #ff6881); }
.deco-rule .diamond { width: 10px; height: 10px; transform: rotate(45deg); border: 1px solid var(--cream); background: #101a36; }
.deco-rule .line-b { height: 1px; width: 38%; background: linear-gradient(90deg, rgba(245,238,223,.64), transparent); }

/* ---------- art panel ---------- */
.deco-stage {
    position: sticky;
    top: 5rem;
    min-height: 470px;
    display: grid;
    place-items: center;
    overflow: hidden;
    isolation: isolate;
    clip-path: polygon(10% 0, 100% 0, 100% 90%, 90% 100%, 0 100%, 0 10%);
    border: 1px solid rgba(245,238,223,.11);
    background:
        linear-gradient(135deg, transparent 0 46%, rgba(49,77,255,.12) 46% 47%, transparent 47% 100%),
        linear-gradient(45deg, rgba(217,45,255,.08), transparent 35%),
        #07101c;
    box-shadow: 0 35px 90px rgba(0,0,0,.42);
}

.deco-stage::before {
    content: "";
    position: absolute;
    inset: 20px;
    border: 1px solid rgba(245,238,223,.09);
    clip-path: polygon(9% 0, 100% 0, 100% 91%, 91% 100%, 0 100%, 0 9%);
    pointer-events: none;
}

.deco-stage::after {
    content: "";
    position: absolute;
    width: 165%;
    height: 42%;
    left: -28%;
    top: 31%;
    transform: rotate(-18deg);
    background: linear-gradient(90deg, transparent 0%, rgba(101,200,255,.03) 34%, rgba(101,200,255,.22) 48%, rgba(255,63,85,.11) 56%, transparent 72%);
    animation: decoSweep 7.5s ease-in-out infinite;
    pointer-events: none;
}

.deco-art-wrap {
    position: relative;
    z-index: 3;
    width: min(94%, 590px);
    transform-origin: 50% 60%;
    animation: decoFloat 5.2s ease-in-out infinite;
    filter: drop-shadow(0 28px 38px rgba(0,0,0,.44));
}
.deco-art {
    display: block;
    width: 100%;
    height: auto;
    animation: decoTilt 9s ease-in-out infinite;
}


@keyframes decoFloat {
    0%,100% { transform: translate3d(0, 8px, 0) scale(1); }
    50% { transform: translate3d(0, -16px, 0) scale(1.012); }
}
@keyframes decoTilt {
    0%,100% { transform: rotate(-.45deg); }
    50% { transform: rotate(.55deg); }
}
@keyframes decoSweep {
    0%,100% { transform: translateX(-10%) rotate(-18deg); opacity: .45; }
    50% { transform: translateX(12%) rotate(-18deg); opacity: .9; }
}

/* ---------- chat ---------- */
div[data-testid="stChatMessage"] {
    position: relative;
    margin-bottom: .9rem;
    padding: .55rem .85rem;
    overflow: hidden;
    border: 1px solid rgba(245,238,223,.09);
    border-radius: 0;
    clip-path: polygon(14px 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%, 0 14px);
    background: linear-gradient(100deg, rgba(14,24,45,.92), rgba(7,13,26,.96));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.02), 0 12px 30px rgba(0,0,0,.12);
}

div[data-testid="stChatMessage"]::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 3px;
    height: 100%;
    background: linear-gradient(var(--kernel-red), var(--cobalt));
    opacity: .8;
}

div[data-testid="stChatMessage"] p {
    color: #eef2ff;
    line-height: 1.72;
}

.answer-meta {
    margin: .45rem 0 .75rem;
    color: rgba(233,220,194,.52);
    font-size: .72rem;
    letter-spacing: .1em;
    text-transform: uppercase;
}

.retrieval-heading {
    display: flex;
    align-items: center;
    gap: .7rem;
    margin: 1rem 0 .6rem;
    color: var(--ivory);
    font-size: .92rem;
    font-weight: 850;
    letter-spacing: .07em;
    text-transform: uppercase;
}
.retrieval-heading::after {
    content: "";
    height: 1px;
    flex: 1;
    background: linear-gradient(90deg, rgba(255,63,85,.65), rgba(49,77,255,.28), transparent);
}

div[data-testid="stExpander"] {
    margin-bottom: .55rem;
    overflow: hidden;
    border: 1px solid rgba(245,238,223,.10);
    border-radius: 0;
    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
    background: rgba(7,13,25,.78);
}

div[data-testid="stExpander"] summary {
    color: #dce5ff;
    font-weight: 650;
}

/* ---------- chat input ---------- */
div[data-testid="stChatInput"] {
    background: rgba(5,8,15,.96);
    border-top: 1px solid rgba(245,238,223,.09);
    box-shadow: 0 -18px 50px rgba(0,0,0,.32);
}

div[data-testid="stChatInput"] > div {
    border-radius: 0 !important;
}

div[data-testid="stChatInput"] textarea {
    color: var(--ivory) !important;
}

/* ---------- sidebar ---------- */
div[data-testid="stSidebar"] {
    background:
        linear-gradient(160deg, rgba(49,77,255,.08), transparent 36%),
        #070c16;
    border-right: 1px solid rgba(245,238,223,.09);
}

div[data-testid="stSidebar"] h3 {
    color: var(--ivory);
    letter-spacing: -.025em;
}

div[data-testid="stSidebar"] .stButton > button {
    border: 1px solid rgba(255,63,85,.32);
    border-radius: 0;
    background: linear-gradient(90deg, rgba(255,63,85,.12), rgba(49,77,255,.10));
    color: var(--ivory);
    clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
}

/* ---------- responsive ---------- */

.deco-v2-diamond {
    position: absolute;
    top: 24px;
    right: 26px;
    width: 11px;
    height: 11px;
    z-index: 4;
    background: var(--kernel-red);
    transform: rotate(45deg);
    box-shadow: 0 0 18px rgba(255,63,85,.55);
}

@media (max-width: 900px) {
    .main .block-container { padding-left: 1rem; padding-right: 1rem; }
    .deco-hero-copy { min-height: auto; padding: 1rem .3rem 2rem 1rem; }
    .deco-title { font-size: 3.4rem; }
    .deco-stage { position: relative; top: auto; min-height: 330px; margin-bottom: 1.4rem; }
}

@media (prefers-reduced-motion: reduce) {
    .deco-art-wrap, .deco-art, .deco-stage::after { animation: none !important; }
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    left, right = st.columns([1.02, 0.98], gap="large", vertical_alignment="center")

    with left:
        st.markdown(
            """
<div class="deco-hero-copy">
    <div class="kernel-mark">Kernel<span class="dot"></span></div>
    <div class="deco-eyebrow">RAG IN ACTION</div>
    <h1 class="deco-title">Knowledge<br><span class="accent">Assistant</span></h1>
    <div class="deco-rule">
        <div class="line-a"></div>
        <div class="diamond"></div>
        <div class="line-b"></div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
<div class="deco-stage">
    <div class="deco-v2-diamond" aria-hidden="true"></div>
    <div class="deco-art-wrap">
        <img class="deco-art" src="{ART_DECO_AI_URI}" alt="Art Deco AI figure" />
    </div>
</div>
""",
            unsafe_allow_html=True,
        )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### Kernel Knowledge Assistant")
        st.caption("RAG Workshop Demo")
        st.divider()
        st.success("Knowledge base ready")
        st.caption("Kernel Knowledge Base PDF")
        st.divider()
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def render_message(message: dict) -> None:
    role = message["role"]
    avatar = "🧑‍💻" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])


def main() -> None:
    inject_css()
    render_sidebar()
    render_hero()

    try:
        pipeline = get_pipeline()
    except (ConfigurationError, KnowledgeBaseNotReadyError, ImportError) as exc:
        st.error(str(exc))
        st.info("Setup: fill OPENAI_API_KEY in .env, then run `python scripts/ingest.py --rebuild`.")
        st.stop()
    except Exception as exc:
        st.error(f"Startup failed: {exc}")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        render_message(message)

    question = st.chat_input(
        "Ask about SalahAldeen, Kernel, MABIEN, services, projects, or training..."
    )
    if not question:
        return

    user_message = {"role": "user", "content": question}
    st.session_state.messages.append(user_message)
    render_message(user_message)

    with st.chat_message("assistant", avatar="🤖"):
        try:
            with st.spinner("Retrieving the most relevant context..."):
                response = pipeline.ask(question)

            st.markdown(response.answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response.answer,
                    "sources": response.sources,
                }
            )
        except Exception as exc:
            st.error(f"Request failed: {exc}")


if __name__ == "__main__":
    main()