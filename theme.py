import streamlit as st
from datetime import datetime, timezone, timedelta
import data as D

CSS_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0a0a0f;color:#e8e8f0}
.stApp{background:#0a0a0f}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1rem 1.5rem 2rem 1.5rem;max-width:100%}

.topbar{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #1e1e2e;padding-bottom:.75rem;margin-bottom:1.25rem}
.logo{font-family:'JetBrains Mono',monospace;font-size:1.25rem;font-weight:700;letter-spacing:.12em;color:#00e5a0}
.logo span{color:#5a5a7a}
.logo .subtitle{font-size:.6rem;color:#5a5a7a;margin-left:.6rem;letter-spacing:.15em;text-transform:uppercase}
.ts{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#5a5a7a}
.section-label{font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:500;letter-spacing:.2em;color:#5a5a7a;text-transform:uppercase;margin-bottom:.75rem;border-left:2px solid #00e5a0;padding-left:.5rem}

/* ── Price card ── */
.pc{background:#12121a;border:1px solid #1e1e2e;border-radius:6px;padding:.85rem 1rem;margin-bottom:.5rem;position:relative;overflow:hidden}
.pc:hover{border-color:#2e2e4e}
.pc-accent{position:absolute;top:0;left:0;height:100%;background:linear-gradient(90deg,rgba(0,229,160,.07),transparent);border-left:3px solid #00e5a0;pointer-events:none}
.pc-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.4rem}
.pc-match{font-size:.82rem;font-weight:600;color:#e8e8f0}
.pc-meta{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#5a5a7a;margin-top:.1rem}
.pc-edge{font-family:'JetBrains Mono',monospace;font-size:.9rem;font-weight:700;color:#00e5a0;text-align:right}
.pc-edge-sub{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#5a5a7a;text-align:right}
.pc-bottom{display:flex;align-items:center;gap:.6rem;margin-top:.5rem;flex-wrap:wrap}
.outcome-tag{font-size:.78rem;color:#c8c8e0;flex:1;min-width:8rem}
.bookie-tag{font-family:'JetBrains Mono',monospace;font-size:.63rem;background:#1e1e2e;color:#9a9ab0;padding:.15rem .4rem;border-radius:3px;white-space:nowrap}
.odds-tag{font-family:'JetBrains Mono',monospace;font-size:.88rem;font-weight:700;color:#00e5a0}
.avg-tag{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#5a5a7a}
.mkt-tag{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#5a5a7a;background:#0a0a0f;border:1px solid #1e1e2e;padding:.1rem .35rem;border-radius:3px}
.ev-bar-wrap{height:3px;background:#1e1e2e;border-radius:2px;margin-top:.55rem;overflow:hidden}
.ev-bar-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,#00e5a0,#00ffb3)}

/* ── Expanded ── */
.xp-card{background:#0f0f1a;border:1px solid #00e5a0;border-radius:6px;padding:.85rem 1rem;margin-bottom:.5rem}
.xp-title{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a7a;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.6rem}
.bm-row{display:flex;align-items:center;justify-content:space-between;padding:.3rem 0;border-bottom:1px solid #1e1e2e;gap:1rem}
.bm-row:last-child{border-bottom:none}
.bm-name{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#9a9ab0;flex:1}
.bm-odds-best{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:700;color:#00e5a0}
.bm-odds{font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#e8e8f0}
.bm-above{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#00e5a0;min-width:3.5rem;text-align:right}
.bm-below{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#ff4d6d;min-width:3.5rem;text-align:right}
.bm-avg{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a7a;min-width:3.5rem;text-align:right}

/* ── Arb card ── */
.arb-card{background:#0f0f1a;border:1px solid #ffb020;border-radius:6px;padding:.85rem 1rem;margin-bottom:.75rem}
.arb-margin{font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700;color:#ffb020}

/* ── Misc ── */
.no-data{padding:2rem;text-align:center;color:#5a5a7a;font-family:'JetBrains Mono',monospace;font-size:.75rem;border:1px dashed #1e1e2e;border-radius:6px}
div[data-testid="stSelectbox"]>div>div{background:#12121a!important;border:1px solid #1e1e2e!important;color:#e8e8f0!important;font-family:'JetBrains Mono',monospace!important}
div[data-testid="stMultiSelect"]>div>div{background:#12121a!important;border:1px solid #1e1e2e!important}
.stButton>button{background:#12121a!important;border:1px solid #1e1e2e!important;color:#9a9ab0!important;font-family:'JetBrains Mono',monospace!important;font-size:.7rem!important;border-radius:4px!important}
.stButton>button:hover{border-color:#00e5a0!important;color:#00e5a0!important}
div[data-testid="stMetric"]{background:#12121a;border:1px solid #1e1e2e;border-radius:6px;padding:.75rem 1rem}
div[data-testid="stMetric"] label{font-family:'JetBrains Mono',monospace!important;font-size:.65rem!important;color:#5a5a7a!important;text-transform:uppercase!important;letter-spacing:.1em!important}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{font-family:'JetBrains Mono',monospace!important;font-size:1.3rem!important;color:#e8e8f0!important}
</style>
"""

STICKMAN_HTML = """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
     padding:2rem;font-family:'JetBrains Mono',monospace;">
<style>
@keyframes ku-ball{0%{transform:translate(0,0) rotate(0deg)}50%{transform:translate(2px,-52px) rotate(180deg)}100%{transform:translate(0,0) rotate(360deg)}}
@keyframes ku-thigh{0%,100%{transform:rotate(-38deg)}12%{transform:rotate(-52deg)}45%{transform:rotate(-15deg)}80%{transform:rotate(-30deg)}}
@keyframes ku-shin{0%,100%{transform:rotate(50deg)}12%{transform:rotate(75deg)}45%{transform:rotate(30deg)}80%{transform:rotate(40deg)}}
@keyframes ku-body{0%,100%{transform:translateY(0) rotate(-2deg)}12%{transform:translateY(-3px) rotate(-4deg)}55%{transform:translateY(1px) rotate(0)}}
@keyframes ku-arml{0%,100%{transform:rotate(-8deg)}12%{transform:rotate(-22deg)}55%{transform:rotate(5deg)}}
@keyframes ku-armr{0%,100%{transform:rotate(8deg)}12%{transform:rotate(25deg)}55%{transform:rotate(-5deg)}}
@keyframes ku-stand{0%,100%{transform:rotate(2deg)}12%{transform:rotate(4deg)}55%{transform:rotate(0)}}
.ku-ball{animation:ku-ball .85s cubic-bezier(.35,0,.65,1) infinite;transform-origin:66px 128px}
.ku-body{animation:ku-body .85s ease-in-out infinite;transform-origin:44px 148px}
.ku-thigh{animation:ku-thigh .85s ease-in-out infinite;transform-origin:44px 100px}
.ku-shin{animation:ku-shin .85s ease-in-out infinite;transform-origin:62px 112px}
.ku-arml{animation:ku-arml .85s ease-in-out infinite;transform-origin:44px 72px}
.ku-armr{animation:ku-armr .85s ease-in-out infinite;transform-origin:44px 72px}
.ku-stand{animation:ku-stand .85s ease-in-out infinite;transform-origin:44px 100px}
</style>
<svg width="120" height="165" viewBox="0 0 120 165">
<ellipse cx="50" cy="160" rx="26" ry="3" fill="rgba(0,229,160,.08)"/>
<g class="ku-ball"><circle cx="66" cy="128" r="8" stroke="#00e5a0" stroke-width="2" fill="rgba(0,229,160,.06)"/><path d="M60 124L66 128L72 124M66 128L66 136" stroke="#00e5a0" stroke-width="1" fill="none" opacity=".55"/></g>
<g class="ku-body">
<circle cx="44" cy="52" r="9" stroke="#00e5a0" stroke-width="2" fill="none"/>
<circle cx="47" cy="50" r="1.1" fill="#00e5a0"/>
<path d="M44 56 Q47 57.5 49 55.5" stroke="#00e5a0" stroke-width="1" fill="none"/>
<path d="M44 61 Q42 80 44 100" stroke="#00e5a0" stroke-width="2" fill="none"/>
<g class="ku-arml"><path d="M44 72 Q28 76 20 88" stroke="#00e5a0" stroke-width="2" fill="none"/></g>
<g class="ku-armr"><path d="M44 72 Q60 74 70 66" stroke="#00e5a0" stroke-width="2" fill="none"/></g>
</g>
<g class="ku-stand"><path d="M44 100 Q40 122 38 142" stroke="#00e5a0" stroke-width="2" fill="none"/><line x1="38" y1="142" x2="30" y2="158" stroke="#00e5a0" stroke-width="2"/><line x1="30" y1="158" x2="40" y2="159" stroke="#00e5a0" stroke-width="2"/></g>
<g class="ku-thigh"><line x1="44" y1="100" x2="62" y2="112" stroke="#00e5a0" stroke-width="2"/><g class="ku-shin"><line x1="62" y1="112" x2="66" y2="128" stroke="#00e5a0" stroke-width="2"/><line x1="66" y1="128" x2="76" y2="126" stroke="#00e5a0" stroke-width="2"/></g></g>
</svg>
<div style="margin-top:.4rem;font-size:.7rem;letter-spacing:.15em;color:#5a5a7a">LOADING MARKETS...</div>
</div>
"""


def setup_page(page_title="InsideEdge"):
    st.set_page_config(page_title=page_title, page_icon="⚡", layout="wide",
                        initial_sidebar_state="collapsed")
    D.API_KEY = st.secrets.get("ODDSPAPI_KEY", "")
    st.markdown(CSS_STYLE, unsafe_allow_html=True)


def require_api_key():
    if not D.API_KEY:
        st.error("Add ODDSPAPI_KEY to Streamlit secrets.")
        st.stop()


def render_topbar(subtitle=""):
    bst = timezone(timedelta(hours=1))
    now = datetime.now(bst).strftime("%d %b %Y  %H:%M BST")
    sub = f'<span class="subtitle">{subtitle}</span>' if subtitle else ""
    st.markdown(
        f'<div class="topbar"><div class="logo">INSIDE<span>EDGE</span>{sub}</div>'
        f'<div class="ts">{now}</div></div>',
        unsafe_allow_html=True,
    )
