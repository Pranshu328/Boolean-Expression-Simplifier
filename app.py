import streamlit as st
from simplifier import simplify
from pathlib import Path
from html import escape
import base64

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "manit_logo.jpg"
BUILDING_PATH = BASE_DIR / "manit_building.jpg"
building_background = (base64.b64encode(BUILDING_PATH.read_bytes()).decode("ascii")
                      if BUILDING_PATH.exists() else "")

st.set_page_config(
    page_title="Boolean Expression Simplifier | MANIT Bhopal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def html_table(rows, headers):
    """Render a simple HTML table without pandas/Arrow conversion."""
    head = "".join(f"<th>{escape(str(h))}</th>" for h in headers)
    body = []
    for row in rows:
        cells = "".join(f"<td>{escape(str(v))}</td>" for v in row)
        body.append(f"<tr>{cells}</tr>")
    return (
        '<div class="table-wrap"><table class="result-table">'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
    )

css = """
<style>
:root { color-scheme: light; }
.stApp {
    background:
      radial-gradient(circle at 92% 4%, rgba(39,110,170,.10), transparent 26rem),
      linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%);
}
.block-container { max-width: 1180px; padding-top: 1.4rem; padding-bottom: 3rem; }
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background: transparent;}
.hero {
    position: relative; overflow: hidden; border-radius: 24px;
    padding: 30px 34px; color: white; margin-bottom: 22px;
    background: linear-gradient(110deg, rgba(10,25,49,.97), rgba(18,54,88,.92)),
                #10243f;
    box-shadow: 0 16px 40px rgba(14,36,64,.16);
}
.hero:after {
    content:""; position:absolute; right:0; top:0; width:42%; height:100%;
    background: linear-gradient(90deg, #10243f 0%, rgba(16,36,63,.28) 100%),
                url("data:image/jpeg;base64,__BUILDING_BG__") center 43%/cover;
    opacity:.26; pointer-events:none;
}
.hero-content {position:relative; z-index:1;}
.eyebrow {color:#f0c56b; font-size:.76rem; font-weight:800; letter-spacing:.16em;}
.hero h1 {font-size:clamp(2rem,4vw,3.25rem); line-height:1.08; margin:.55rem 0 .65rem; color:#fff;}
.hero p {color:#d6e2ef; margin:0; font-size:1rem;}
.identity {
    margin-top:22px; padding:15px 18px; max-width:650px;
    border:1px solid rgba(255,255,255,.2); border-radius:15px;
    background:rgba(255,255,255,.09); backdrop-filter:blur(4px);
}
.identity .name {font-size:1.12rem; font-weight:800; color:#fff; letter-spacing:.04em;}
.identity .meta {color:#d7e2ef; font-size:.84rem; line-height:1.65;}
.section-card {
    background:#fff; border:1px solid #e2e9f1; border-radius:18px;
    padding:20px 22px; margin:12px 0;
    box-shadow:0 7px 22px rgba(27,53,82,.045);
}
.section-kicker {font-size:.72rem; letter-spacing:.12em; font-weight:800; color:#b17a20;}
.section-title {font-size:1.35rem; font-weight:800; color:#172c49; margin:.2rem 0 .75rem;}
.result-banner {
    padding:20px 22px; border-radius:17px; color:white;
    background:linear-gradient(110deg,#132b4a,#1d4b72);
    box-shadow:0 10px 26px rgba(19,43,74,.14); margin:16px 0 22px;
}
.result-label {font-size:.72rem; letter-spacing:.13em; color:#f2cb78; font-weight:800;}
.result-expression {font-size:clamp(1.45rem,3vw,2.15rem); font-weight:800; margin-top:7px; overflow-wrap:anywhere;}
.table-wrap {overflow-x:auto; border:1px solid #e5ebf2; border-radius:12px; margin:.5rem 0 1rem;}
.result-table {border-collapse:collapse; width:100%; background:white; font-size:.9rem;}
.result-table th {background:#edf3f9; color:#183451; font-weight:800; text-align:left;}
.result-table th,.result-table td {padding:9px 12px; border-bottom:1px solid #e8edf3; white-space:nowrap;}
.result-table tr:last-child td {border-bottom:0;}
div[data-testid="stTextInput"] input {border-radius:11px;}
div.stButton > button {
    border-radius:11px; padding:.65rem 1.25rem; font-weight:750;
    border:0; background:#173b60; color:white;
}
div.stButton > button:hover {background:#245783; color:white; border:0;}
div[data-testid="stExpander"] {border:1px solid #e1e8f0; border-radius:12px; background:#fff;}
.small-note {color:#62748a; font-size:.86rem;}
.footer-note {text-align:center; color:#718096; font-size:.8rem; padding:18px 0 4px;}
/* ===== FULL-PAGE MANIT TECH THEME ===== */
:root { color-scheme: dark; }
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: #071426 !important;
    color: #eaf2ff !important;
}
[data-testid="stAppViewContainer"] {
    background-image:
      radial-gradient(ellipse at 12% 0%, rgba(27,111,174,.30), transparent 38%),
      radial-gradient(ellipse at 88% 26%, rgba(18,72,125,.24), transparent 34%),
      linear-gradient(145deg, #071426 0%, #0a1c33 48%, #071426 100%) !important;
}
[data-testid="stHeader"] { background: rgba(7,20,38,.72) !important; }
[data-testid="stToolbar"] { right: 1rem; }
.block-container { max-width: 1220px; padding-top: 1.5rem; padding-bottom: 4rem; }
.stMarkdown, .stText, label, [data-testid="stCaptionContainer"] { color: #d7e5f7 !important; }
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] { color: #dce9fa; }
/* Institute masthead */
[data-testid="stImage"] img { filter: drop-shadow(0 5px 12px rgba(0,0,0,.28)); }
/* Hero */
.hero {
    border: 1px solid rgba(130,184,232,.25);
    background: linear-gradient(115deg, rgba(5,18,36,.98), rgba(11,54,91,.94) 58%, rgba(12,77,116,.86));
    box-shadow: 0 24px 65px rgba(0,0,0,.36), inset 0 1px 0 rgba(255,255,255,.08);
    padding: 42px 46px; margin: 22px 0 30px;
}
.hero:after { opacity: .34; width: 48%; }
.hero h1 { font-size: clamp(2.5rem,5vw,4rem); letter-spacing: -.035em; }
.hero p { font-size: 1.08rem; }
.identity { background: rgba(16,67,105,.55); border-color: rgba(164,207,245,.32); }
/* Streamlit's actual form becomes the prominent input panel */
div[data-testid="stForm"] {
    background: linear-gradient(145deg, rgba(16,42,69,.98), rgba(10,29,51,.98)) !important;
    border: 1px solid rgba(112,169,220,.30) !important;
    border-radius: 22px !important;
    padding: 26px 28px 24px !important;
    box-shadow: 0 18px 45px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.05) !important;
}
div[data-testid="stTextInput"] label { color: #f0c76e !important; font-weight: 750 !important; font-size: 1rem !important; }
div[data-testid="stTextInput"] input {
    min-height: 58px !important; border-radius: 13px !important;
    background: #f4f8ff !important; color: #10243c !important;
    border: 2px solid #6f9fc8 !important; font-size: 1.08rem !important;
    padding: 12px 16px !important;
}
div[data-testid="stTextInput"] input:focus { border-color: #efc66d !important; box-shadow: 0 0 0 3px rgba(239,198,109,.2) !important; }
div[data-testid="stTextInput"] input::placeholder { color: #667b91 !important; }
/* Large, unmistakable action button */
div[data-testid="stFormSubmitButton"] { width: 100% !important; margin-top: 12px !important; }
div[data-testid="stFormSubmitButton"] button {
    width: 100% !important; min-height: 64px !important;
    border-radius: 14px !important; border: 1px solid #f4d58f !important;
    background: linear-gradient(100deg, #d99a32 0%, #f0c66c 52%, #d99a32 100%) !important;
    color: #10243c !important; font-size: 1.12rem !important;
    font-weight: 900 !important; letter-spacing: .025em !important;
    box-shadow: 0 9px 24px rgba(217,154,50,.24) !important;
    transition: transform .18s ease, box-shadow .18s ease !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px); box-shadow: 0 14px 30px rgba(217,154,50,.34) !important;
    color: #071426 !important; border-color: #ffe4a8 !important;
}
/* Section and result panels */
.section-card {
    background: linear-gradient(145deg, rgba(17,43,70,.96), rgba(10,28,49,.96)) !important;
    border: 1px solid rgba(117,170,218,.24) !important;
    box-shadow: 0 14px 34px rgba(0,0,0,.20) !important;
}
.section-title { color: #f2f6ff !important; }
.section-kicker, .result-label { color: #f0c66d !important; }
.small-note, .footer-note { color: #a9bdd4 !important; }
.result-banner {
    border: 1px solid rgba(240,198,109,.38) !important;
    background: linear-gradient(110deg,#102b49,#164b72 65%,#12617a) !important;
    box-shadow: 0 16px 36px rgba(0,0,0,.28) !important;
}
/* Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #123454, #0d2742) !important;
    border: 1px solid rgba(125,178,225,.25) !important;
    border-radius: 16px !important; padding: 16px 18px !important;
}
div[data-testid="stMetricLabel"] { color: #b8cce2 !important; }
div[data-testid="stMetricValue"] { color: #f5cc73 !important; }
/* Tables, code, expanders */
.table-wrap { border-color: rgba(125,178,225,.25) !important; }
.result-table { background: #102943 !important; color: #eaf2ff !important; }
.result-table th { background: #1b4568 !important; color: #f4d58f !important; }
.result-table td { color: #e1ecf8 !important; border-color: rgba(140,180,215,.15) !important; }
.result-table tr:nth-child(even) td { background: rgba(255,255,255,.035) !important; }
div[data-testid="stExpander"] {
    background: rgba(15,39,64,.92) !important;
    border: 1px solid rgba(125,178,225,.25) !important; border-radius: 14px !important;
}
div[data-testid="stExpander"] summary, div[data-testid="stExpander"] summary p { color: #f0f5ff !important; font-weight: 700 !important; }
div[data-testid="stCode"] pre { background: #071a2d !important; color: #f3d58e !important; border: 1px solid rgba(125,178,225,.2) !important; }
[data-testid="stAlert"] { border-radius: 13px !important; }
.footer-note { border-top: 1px solid rgba(125,178,225,.18); margin-top: 28px; }
@media(max-width:700px) {
 .hero {padding:25px 20px;}
 .hero h1 {font-size:2.25rem;}
 .identity {padding:12px;}
 .section-card {padding:16px;}
 div[data-testid="stForm"] {padding:18px 16px !important;}
}
</style>
"""
st.markdown(css.replace("__BUILDING_BG__", building_background), unsafe_allow_html=True)

# Institute masthead
c1, c2 = st.columns([1, 8], vertical_alignment="center")
with c1:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=92)
with c2:
    st.markdown(
        '<div style="color:#eaf2ff;font-weight:850;font-size:1.02rem;">'
        'MAULANA AZAD NATIONAL INSTITUTE OF TECHNOLOGY, BHOPAL</div>'
        '<div style="color:#a9bdd4;font-size:.83rem;">Department of Electronics and Communication Engineering</div>',
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="hero"><div class="hero-content">
  <div class="eyebrow">DIGITAL CIRCUIT DESIGN • PROJECT</div>
  <h1>Boolean Expression<br> Simplifier</h1>
  <p>An interactive implementation of the Quine–McCluskey Tabulation Method</p>
  <div class="identity">
    <div class="eyebrow">PROJECT DEVELOPED BY</div>
    <div class="name">PRANSHU SACHDEV</div>
    <div class="meta">Scholar No.: 25114011328 &nbsp; | &nbsp; Roll No.: 328<br>
    Guided by: Suryakant Gautam Sir</div>
  </div>
</div></div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">01 / INPUT</div><div class="section-title">Simplify a Boolean expression</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="small-note">Enter an expression to generate its truth table, minterms, '
    'tabulation stages, prime implicants and minimum SOP expression.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    "**Notation:** NOT: `A'` or `~A` &nbsp; • &nbsp; OR: `+` &nbsp; • &nbsp; "
    "AND: `AB`, `A.B` or `A*B` &nbsp; • &nbsp; Parentheses supported<br>"
    "**Limit:** Up to 6 single-letter variables (A–Z).",
    unsafe_allow_html=True,
)
with st.form("simplify_form"):
    expr = st.text_input("Boolean expression", placeholder="Example: A'B + AB + AC")
    submitted = st.form_submit_button("⚡  Simplify Expression", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    try:
        data = simplify(expr)
        result = data["result"]
        st.success("Expression simplified successfully.")
        st.markdown(
            f'<div class="result-banner"><div class="result-label">MINIMUM SOP RESULT</div>'
            f'<div class="result-expression">F = {escape(result)}</div></div>',
            unsafe_allow_html=True,
        )

        # Quick summary
        a, b, c = st.columns(3)
        a.metric("Variables", len(data["variables"]))
        b.metric("Minterms", len(data["minterms"]))
        c.metric("Prime implicants", len(data["prime_patterns"]))

        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-kicker">02 / VARIABLE ANALYSIS</div><div class="section-title">Variables identified</div>', unsafe_allow_html=True)
            st.write("  •  ".join(data["variables"]))
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">03 / COMPLETE ANALYSIS</div><div class="section-title">Truth table</div>', unsafe_allow_html=True)
        vars_ = data["variables"]
        headers = vars_ + ["Output F"]
        truth_rows = [[row[v] for v in vars_] + [row["Output F"]] for row in data["truth_table"]]
        st.markdown(html_table(truth_rows, headers), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">04 / CANONICAL FORM</div><div class="section-title">Minterms</div>', unsafe_allow_html=True)
        st.code("Σm(" + ", ".join(map(str, data["minterms"])) + ")", language="text")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">05 / QUINE–McCLUSKEY</div><div class="section-title">Tabulation stages</div>', unsafe_allow_html=True)
        for i, stage in enumerate(data["stages"], 1):
            with st.expander(f"Stage {i} — {len(stage['terms'])} terms", expanded=(i == 1)):
                st.markdown("**Terms considered**")
                st.write(stage["terms"])
                st.markdown("**Combinations**")
                if stage["combinations"]:
                    comb_rows = [[a, b, combined, ", ".join(map(str, covered))]
                                 for a, b, combined, covered in stage["combinations"]]
                    st.markdown(
                        html_table(comb_rows, ["Term 1", "Term 2", "Combined pattern", "Minterms covered"]),
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("No further combinations are possible at this stage.")
                st.markdown("**Prime implicants identified**")
                st.write(stage["primes"] or "None")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">06 / COVER SELECTION</div><div class="section-title">Prime implicants</div>', unsafe_allow_html=True)
        st.write(data["prime_patterns"] or "None")
        st.caption("A dash (–) in a binary pattern indicates a variable eliminated during combination.")
        st.write("Implicant expressions: " + (", ".join(data["prime_implicants"]) or "None"))
        st.markdown("**Selected minimum cover**")
        st.write(", ".join(data["selected_patterns"]) or "None")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="result-banner"><div class="result-label">FINAL SIMPLIFIED EXPRESSION</div>'
            f'<div class="result-expression">F = {escape(result)}</div></div>',
            unsafe_allow_html=True,
        )
    except Exception as error:
        st.error(f"Could not simplify this expression: {error}")
        st.info("Check the notation and parentheses, then try again.")

st.markdown(
    '<div class="footer-note">MANIT Bhopal • Department of Electronics and Communication Engineering<br>'
    'Quine–McCluskey tabulation method · Academic project</div>',
    unsafe_allow_html=True,
)
