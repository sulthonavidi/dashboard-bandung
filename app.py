# ╔══════════════════════════════════════════════════════════════════════╗
# ║     PROFIL KEPENDUDUKAN KOTA BANDUNG  ·  Enterprise Dark Edition     ║
# ║     Data: BPS Kota Bandung 2025  |  Streamlit + Plotly               ║
# ╚══════════════════════════════════════════════════════════════════════╝

import os
import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ─────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Profil Kependudukan Bandung",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════
#  DESIGN TOKENS  —  World-Class Enterprise Dark
#  Reference: Bloomberg · Palantir · McKinsey · Linear
# ══════════════════════════════════════════════════════════
C = {
    "bg"       : "#07090E",   # terminal black — absolute base
    "surface"  : "#0D1117",   # card layer (GitHub dark level)
    "surface2" : "#141B27",   # elevated state
    "border"   : "#1C2333",   # default border (very low contrast)
    "text"     : "#E6EDF5",   # near-white — crisp readability
    "muted"    : "#5B6F8A",   # secondary labels
    "amber"    : "#C87D2A",   # gold — insight / warm accent
    "sky"      : "#1F73E8",   # corporate blue — primary data
    "teal"     : "#0D9E72",   # emerald green — positive
    "rose"     : "#D63B56",   # alert red — female / warning
    "violet"   : "#6B58E0",   # indigo — neutral accent
}

# ── CSS PREMIUM ───────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600&family=Space+Grotesk:wght@500;600;700;800&display=swap');

/* ═══════════════════════════════
   RESET
═══════════════════════════════ */
#MainMenu,footer,header,.stDeployButton{{visibility:hidden}}
[data-testid="stToolbar"],[data-testid="stDecoration"]{{display:none}}

html,body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"]>.main,
[data-testid="block-container"]{{
    background:{C["bg"]} !important;
    font-family:'Inter',sans-serif;
    color:{C["text"]};
    -webkit-font-smoothing:antialiased;
    -moz-osx-font-smoothing:grayscale;
}}
[data-testid="block-container"]{{
    padding-top:1.75rem !important;
    padding-bottom:3rem !important;
}}
*{{box-sizing:border-box}}

/* ═══════════════════════════════
   TYPOGRAPHY
═══════════════════════════════ */
h1,h2,h3,h4{{
    font-family:'Space Grotesk',sans-serif;
    color:{C["text"]};
    letter-spacing:-.4px;
}}

/* ═══════════════════════════════
   HERO
═══════════════════════════════ */
.hero{{
    background:{C["surface"]};
    border:1px solid {C["border"]};
    border-left:3px solid {C["sky"]};
    border-radius:0 10px 10px 0;
    padding:1.9rem 2.4rem 1.75rem;
    margin-bottom:1.75rem;
    position:relative;
    overflow:hidden;
}}
.hero::before{{
    content:'';
    position:absolute;
    inset:0;
    background:linear-gradient(105deg,transparent 60%,rgba(31,115,232,.04) 100%);
    pointer-events:none;
}}
.hero::after{{
    content:'KOTA BANDUNG 2025';
    position:absolute;
    right:2rem; bottom:-1rem;
    font-family:'Space Grotesk',sans-serif;
    font-size:4rem; font-weight:800;
    color:rgba(255,255,255,0.022);
    letter-spacing:-2px;
    pointer-events:none; user-select:none;
    line-height:2; white-space:nowrap;
}}
.hero-kicker{{
    font-size:.63rem; font-weight:600;
    letter-spacing:2.8px; text-transform:uppercase;
    color:{C["muted"]};
    margin-bottom:.6rem;
    display:flex; align-items:center; gap:.55rem;
}}
.hero-kicker::before{{
    content:'';
    display:inline-block;
    width:22px; height:1.5px;
    background:{C["sky"]};
    border-radius:2px;
    flex-shrink:0;
}}
.hero-title{{
    font-family:'Space Grotesk',sans-serif;
    font-size:2.05rem; font-weight:800;
    color:{C["text"]};
    margin:0 0 .5rem;
    line-height:1.15;
    letter-spacing:-.6px;
}}
.hero-title span{{color:{C["sky"]}}}
.hero-desc{{
    font-size:.9rem;
    color:{C["muted"]};
    max-width:800px;
    line-height:1.65;
    margin:0; font-weight:400;
}}

/* ═══════════════════════════════
   KPI CARDS
═══════════════════════════════ */
.kpi-wrap{{
    background:{C["surface"]};
    border:1px solid {C["border"]};
    border-radius:8px;
    padding:1.4rem 1.5rem 1.25rem;
    display:flex; flex-direction:column; gap:.15rem;
    position:relative; overflow:hidden;
    transition:border-color .18s, background .18s;
    cursor:default;
}}
.kpi-wrap:hover{{
    border-color:#263248;
    background:{C["surface2"]};
}}
.kpi-bar{{
    position:absolute;
    top:0; left:0; right:0;
    height:2px; border-radius:8px 8px 0 0;
}}
.kpi-label{{
    font-size:.6rem; font-weight:600;
    letter-spacing:2.2px; text-transform:uppercase;
    color:{C["muted"]}; margin-bottom:.45rem;
    font-family:'Inter',sans-serif;
}}
.kpi-val{{
    font-family:'Space Grotesk',sans-serif;
    font-size:2rem; font-weight:700;
    color:{C["text"]};
    line-height:1.05; letter-spacing:-.5px;
    margin-bottom:.2rem;
}}
.kpi-sub{{
    font-size:.73rem; color:{C["muted"]};
    font-weight:400; line-height:1.4;
    font-family:'Inter',sans-serif;
}}

/* ═══════════════════════════════
   TABS
═══════════════════════════════ */
[data-testid="stTabs"] [role="tablist"]{{
    border-bottom:1px solid {C["border"]} !important;
    padding-bottom:0 !important;
    gap:0 !important;
    background:transparent !important;
    border-radius:0 !important;
    margin-bottom:1.5rem;
}}
[data-testid="stTabs"] [role="tab"]{{
    font-family:'Inter',sans-serif !important;
    font-size:.875rem !important;
    font-weight:500 !important;
    color:{C["muted"]} !important;
    background:transparent !important;
    border:none !important;
    border-bottom:2px solid transparent !important;
    border-radius:0 !important;
    padding:.7rem 1.6rem !important;
    margin-bottom:-1px !important;
    letter-spacing:.05px;
    transition:color .15s, border-color .15s !important;
    white-space:nowrap !important;
}}
[data-testid="stTabs"] [role="tab"]:hover{{
    color:#7B9ABF !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{{
    color:{C["text"]} !important;
    font-weight:600 !important;
    border-bottom:2px solid {C["sky"]} !important;
}}

/* ═══════════════════════════════
   SECTION TITLE
═══════════════════════════════ */
.sec-title{{
    font-family:'Space Grotesk',sans-serif;
    font-size:1.05rem; font-weight:700;
    color:{C["text"]};
    margin:1.5rem 0 1rem;
    padding-bottom:.6rem;
    border-bottom:1px solid {C["border"]};
    letter-spacing:-.25px;
    display:flex; align-items:center; gap:.55rem;
}}
.sec-title::before{{
    content:'';
    display:inline-block;
    width:3px; height:1rem;
    background:{C["sky"]};
    border-radius:2px;
    flex-shrink:0;
}}

/* ═══════════════════════════════
   INSIGHT CARD
═══════════════════════════════ */
.insight{{
    background:{C["surface"]};
    border:1px solid {C["border"]};
    border-left:3px solid {C["amber"]};
    border-radius:0 6px 6px 0;
    padding:1.05rem 1.35rem;
    margin-top:.9rem;
}}
.insight-body{{
    font-size:.875rem;
    color:#8BA8C7;
    line-height:1.72;
    font-weight:400;
    font-family:'Inter',sans-serif;
}}
.insight-body strong{{
    color:{C["text"]};
    font-weight:600;
}}
.insight-body i{{
    font-style:italic;
    color:#7A9AB8;
}}

/* ═══════════════════════════════
   RADIO OVERRIDE
═══════════════════════════════ */
[data-testid="stRadio"] label span p{{
    font-size:.82rem !important;
    color:{C["muted"]} !important;
    font-family:'Inter',sans-serif !important;
}}

/* Hide st.info fallback */
[data-testid="stInfo"]{{display:none}}
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════
#  BULLETPROOF DATA UTILITIES
# ═════════════════════════════════════════════════════════════════════
def extract_number(val):
    if val is None: return None
    if isinstance(val, float) and np.isnan(val): return None
    if isinstance(val, (int, float)): return float(val)
    s = str(val).strip()
    s = re.sub(r'(?i)rp\.?\s*', '', s)
    s = re.sub(r'(?i)ribu\s*jiwa', '', s)
    s = re.sub(r'(?i)jiwa', '', s)
    s = re.sub(r'(?i)per\s*kapita.*', '', s)
    s = re.sub(r'(?i)miliar.*', '', s)
    s = re.sub(r'(?i)tahun\s*', '', s)
    s = s.replace(',', '.')
    nums = re.findall(r'\d+\.?\d*', s)
    return float(nums[0]) if nums else None

def find_header_row(df, keyword, col=0):
    for i, val in enumerate(df.iloc[:, col].astype(str)):
        if keyword.lower() in val.lower(): return i
    return None

def is_aggregate_row(val):
    s = str(val).strip().lower()
    return s in {'jumlah', 'total', 'kota bandung', 'kota bandung (total)', 'semua status', 'nan'}

def find_keyword_value(df, keyword, val_col=1, key_col=0):
    for i, cell in enumerate(df.iloc[:, key_col].astype(str)):
        if keyword.lower() in cell.lower():
            v = df.iloc[i, val_col]
            if not (isinstance(v, float) and np.isnan(v)): return v
    return None

def safe_block(raw, col_indices, col_names, header_keyword, header_col=0, numeric_check_name=None):
    hdr = find_header_row(raw, header_keyword, col=header_col)
    hdr = hdr if hdr is not None else 0
    block = raw.iloc[hdr + 1:, col_indices].copy()
    block.columns = col_names
    block = block[~block[col_names[0]].astype(str).apply(is_aggregate_row)]
    check = numeric_check_name or col_names[1]
    block = block[block[check].apply(lambda x: extract_number(x) is not None)]
    return block.reset_index(drop=True)

# ═════════════════════════════════════════════════════════════════════
#  LOAD DATA
# ═════════════════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "Data_Kota_Bandung.xlsx")

@st.cache_data(show_spinner="⏳ Menginisialisasi data BPS...")
def load_data():
    raw_umur = pd.read_excel(FILE, sheet_name='Penduduk menurut umur & jk', header=None)
    df_umur = safe_block(raw_umur, [0, 1, 2, 3], ['Kelompok_Umur', 'Laki_Laki', 'Perempuan', 'Jumlah'], 'Kelompok', numeric_check_name='Laki_Laki')
    for c in ['Laki_Laki', 'Perempuan', 'Jumlah']: df_umur[c] = df_umur[c].apply(extract_number)

    raw_kem = pd.read_excel(FILE, sheet_name='kemiskinan', header=None)
    pct_raw = find_keyword_value(raw_kem, 'Persentase')
    jml_raw = find_keyword_value(raw_kem, 'Jumlah Penduduk Miskin')
    pct_num = extract_number(pct_raw)
    pct_miskin = round(pct_num * 100, 2) if pct_num else 0.0
    jml_miskin_str = str(jml_raw) if jml_raw is not None else "N/A"

    raw_pend = pd.read_excel(FILE, sheet_name='pendidikan', header=None)
    df_ijazah = safe_block(raw_pend, [4, 5, 6], ['Ijazah', 'Laki_Laki', 'Perempuan'], 'Ijazah', header_col=4, numeric_check_name='Laki_Laki')
    for c in ['Laki_Laki', 'Perempuan']: df_ijazah[c] = df_ijazah[c].apply(extract_number)

    raw_pek = pd.read_excel(FILE, sheet_name='pekerjaan', header=None)
    df_status = safe_block(raw_pek, [0, 1, 2, 3], ['Status', 'Laki_Laki', 'Perempuan', 'Jumlah'], 'Status Pekerjaan', header_col=0, numeric_check_name='Laki_Laki')
    for c in ['Laki_Laki', 'Perempuan', 'Jumlah']: df_status[c] = df_status[c].apply(extract_number)

    df_lap = safe_block(raw_pek, [5, 6, 7, 8, 9], ['Kategori', 'Laki_Laki', 'Perempuan', 'Jumlah', 'Persen'], 'Kategori', header_col=5, numeric_check_name='Jumlah')
    for c in ['Laki_Laki', 'Perempuan', 'Jumlah', 'Persen']: df_lap[c] = df_lap[c].apply(extract_number)

    raw_kep = pd.read_excel(FILE, sheet_name='kepadatan', header=None)
    df_kep = safe_block(raw_kep, [0, 1, 2], ['Kecamatan', 'Luas', 'Penduduk'], 'Kecamatan', numeric_check_name='Penduduk')
    df_kep['Luas'] = df_kep['Luas'].apply(extract_number)
    df_kep['Penduduk'] = df_kep['Penduduk'].apply(extract_number)
    df_kep['Kepadatan'] = (df_kep['Penduduk'] / df_kep['Luas']).round(0).astype(int)

    raw_kom = pd.read_excel(FILE, sheet_name='komersial', header=None)
    df_kom = safe_block(raw_kom, [0, 1], ['Kecamatan', 'Restoran'], 'Kecamatan', numeric_check_name='Restoran')
    df_kom['Restoran'] = df_kom['Restoran'].apply(extract_number).astype(int)

    raw_eko = pd.read_excel(FILE, sheet_name='ekonomi', header=None)
    df_eko_all = safe_block(raw_eko, [0, 1], ['Kategori', 'PDRB'], 'Kategori', numeric_check_name='PDRB')
    df_eko_all['PDRB'] = df_eko_all['PDRB'].apply(extract_number)
    is_total = df_eko_all['Kategori'].astype(str).str.lower().str.contains('total')
    total_pdrb = df_eko_all.loc[is_total, 'PDRB'].values[0] if is_total.any() else 0.0
    df_eko_sek = df_eko_all[~is_total].dropna(subset=['PDRB']).reset_index(drop=True)

    def _norm(s): return re.sub(r'[\s/\-_.,]', '', str(s).lower())
    df_kep_m = df_kep.copy(); df_kom_m = df_kom.copy()
    df_kep_m['_k'] = df_kep_m['Kecamatan'].apply(_norm)
    df_kom_m['_k'] = df_kom_m['Kecamatan'].apply(_norm)
    df_merge = pd.merge(df_kep_m, df_kom_m[['_k', 'Restoran']], on='_k', how='left').drop(columns=['_k'])
    df_merge['Restoran'] = df_merge['Restoran'].fillna(0).astype(int)

    return (df_umur, df_ijazah, df_status, df_lap, pct_miskin, jml_miskin_str, df_kep, df_kom, df_eko_sek, total_pdrb, df_merge)

(df_umur, df_ijazah, df_status, df_lap, pct_miskin, jml_miskin_str, df_kep, df_kom, df_eko_sek, total_pdrb, df_merge) = load_data()

# ═════════════════════════════════════════════════════════════════════
#  KALKULASI MAKRO KOTA (CITY AGGREGATES)
# ═════════════════════════════════════════════════════════════════════
total_penduduk = df_umur['Jumlah'].sum()
muda = df_umur[df_umur['Kelompok_Umur'].isin(['0–4', '5–9', '10–14'])]['Jumlah'].sum()
tua = df_umur[df_umur['Kelompok_Umur'].isin(['65–69', '70–74', '75+'])]['Jumlah'].sum()
produktif = total_penduduk - muda - tua
dep_ratio = round((muda + tua) / produktif * 100, 1) if produktif > 0 else 0

total_luas_kota = df_kep['Luas'].sum()
kepadatan_kota = (total_penduduk / total_luas_kota) if total_luas_kota > 0 else 0


# ═════════════════════════════════════════════════════════════════════
#  HELPERS & PLOTLY LAYOUT MASTER (Premium Layout)
# ═════════════════════════════════════════════════════════════════════
PCFG = {"displayModeBar": False}

def pro_layout(**kwargs):
    base = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=C["muted"], size=12),
        margin=dict(l=10, r=10, t=60, b=50), 
        xaxis=dict(showgrid=False, zeroline=False, automargin=True, tickangle=0,
                   tickfont=dict(color=C["muted"], size=11), linecolor=C["border"]),
        yaxis=dict(showgrid=True, gridcolor="rgba(43,50,69,0.5)", zeroline=False, automargin=True,
                   tickfont=dict(color=C["muted"], size=11)),
        legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5,
                    font=dict(color=C["muted"], size=11)),
        hoverlabel=dict(bgcolor=C["surface2"], font=dict(family='Inter', color=C["text"]), bordercolor=C["border"])
    )
    base.update(kwargs)
    return base

def insight(teks):
    st.markdown(f"""
    <div class="insight">
      <div class="insight-body">💡 {teks}</div>
    </div>""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════
#  UI RENDERING
# ═════════════════════════════════════════════════════════════════════

# HERO SECTION
st.markdown(f"""
<div class="hero">
  <div class="hero-kicker">Sumber Data · BPS: Kota Bandung Dalam Angka 2026</div>
  <div class="hero-title">Profil Kependudukan <span>Kota Bandung</span></div>
  <p class="hero-desc">Ringkasan Eksekutif Data Demografi, Ketenagakerjaan, dan Distribusi Spasial</p>
</div>
""", unsafe_allow_html=True)

# GLOBAL KPI CARDS
k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "Total Penduduk", f"{total_penduduk:,.0f}", "Jiwa", C["sky"]),
    (k2, "Kepadatan Penduduk", f"{kepadatan_kota:,.0f}", "Jiwa per km²", C["rose"]),
    (k3, "Total PDRB", f"Rp {total_pdrb/1000:.1f} T", "Atas Dasar Harga Berlaku", C["teal"]),
    (k4, "Rasio Ketergantungan", str(dep_ratio), "Tanggungan per 100 usia produktif", C["amber"]),
]

st.markdown('<div style="display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap;">', unsafe_allow_html=True)
for col, label, val, sub, color in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-bar" style="background:{color}"></div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# TABS NAVIGATION
tab1, tab2, tab3 = st.tabs([
    "Demografi & Pendidikan", "Ketenagakerjaan", "Distribusi Spasial"
])

# ── TAB 1: DEMOGRAFI & PENDIDIKAN ──
with tab1:
    # --- PERBAIKAN 3: KARTU PERBANDINGAN GENDER ---
    st.markdown('<div class="sec-title">Analisis Gender & Piramida Penduduk</div>', unsafe_allow_html=True)
    
    tot_laki = df_umur['Laki_Laki'].sum()
    tot_puan = df_umur['Perempuan'].sum()
    sex_ratio = (tot_laki / tot_puan) * 100 if tot_puan > 0 else 0
    
    gl, gp, gr = st.columns(3)
    with gl:
        st.markdown(f"""
        <div class="kpi-wrap" style="padding: 1.2rem;">
            <div class="kpi-bar" style="background:{C['sky']}"></div>
            <div class="kpi-label">Total Laki-Laki</div>
            <div class="kpi-val" style="font-size: 1.8rem; color:{C['sky']}">{tot_laki:,.0f} <span style="font-size:0.9rem; color:{C['muted']}">Jiwa</span></div>
            <div class="kpi-sub">{tot_laki/total_penduduk*100:.1f}% dari total populasi</div>
        </div>
        """, unsafe_allow_html=True)
    with gp:
        st.markdown(f"""
        <div class="kpi-wrap" style="padding: 1.2rem;">
            <div class="kpi-bar" style="background:{C['rose']}"></div>
            <div class="kpi-label">Total Perempuan</div>
            <div class="kpi-val" style="font-size: 1.8rem; color:{C['rose']}">{tot_puan:,.0f} <span style="font-size:0.9rem; color:{C['muted']}">Jiwa</span></div>
            <div class="kpi-sub">{tot_puan/total_penduduk*100:.1f}% dari total populasi</div>
        </div>
        """, unsafe_allow_html=True)
    with gr:
        st.markdown(f"""
        <div class="kpi-wrap" style="padding: 1.2rem;">
            <div class="kpi-bar" style="background:{C['violet']}"></div>
            <div class="kpi-label">Sex Ratio (Rasio Jenis Kelamin)</div>
            <div class="kpi-val" style="font-size: 1.8rem; color:{C['violet']}">{sex_ratio:.1f}</div>
            <div class="kpi-sub">Artinya terdapat ~{int(sex_ratio)} Laki-laki per 100 Perempuan</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    kel = df_umur['Kelompok_Umur'].tolist()
    laki = df_umur['Laki_Laki'].tolist()
    puan = df_umur['Perempuan'].tolist()

    # --- PERBAIKAN 1: SUMBU X SIMETRIS & ANGKA GENAP ---
    max_v_raw = max(max(laki), max(puan))
    # Buat kelipatan angka genap. Kalau datanya > 100k, intervalnya 40k. Kalau < 100k, interval 20k.
    step = 40000 if max_v_raw > 100000 else 20000
    max_val = int(np.ceil(max_v_raw / step) * step) # Membulatkan otomatis ke batas genap terdekat
    
    # Generate label (misal: -160k, -120k, ... 0 ... 120k, 160k)
    ticks = list(range(-max_val, max_val + step, step))
    tlabel = [f"{abs(v)//1000:.0f}k" if v != 0 else "0" for v in ticks]

    fig_pyr = go.Figure()
    fig_pyr.add_trace(go.Bar(y=kel, x=[-v for v in laki], name='Laki-Laki', orientation='h', marker=dict(color=C["sky"], opacity=0.85), hovertemplate="<b>Usia %{y}</b><br>Laki-Laki: %{customdata:,} jiwa<extra></extra>", customdata=laki))
    fig_pyr.add_trace(go.Bar(y=kel, x=puan, name='Perempuan', orientation='h', marker=dict(color=C["rose"], opacity=0.85), hovertemplate="<b>Usia %{y}</b><br>Perempuan: %{x:,} jiwa<extra></extra>"))

    # Shade usia produktif
    fig_pyr.add_shape(
        type="rect", layer="below",
        x0=-max_val, x1=max_val, y0=2.5, y1=12.5,
        fillcolor="rgba(59,130,246,0.05)",
        line=dict(color="rgba(59,130,246,0.1)", width=1, dash="dot"),
    )
    fig_pyr.add_annotation(
        x=max_val*0.8, y=12.6, text="Usia Produktif (15-64)",
        showarrow=False, font=dict(size=10, color=C["muted"]), xanchor="right",
    )

    fig_pyr.update_layout(**pro_layout(
        barmode='overlay', height=450,
        xaxis=dict(range=[-max_val, max_val], tickvals=ticks, ticktext=tlabel, showgrid=True, gridcolor="rgba(43,50,69,0.5)", zeroline=True, zerolinecolor=C["border"]),
        yaxis=dict(showgrid=False)
    ))
    st.plotly_chart(fig_pyr, use_container_width=True, config=PCFG)
    
    # Interpretasi spesifik Gender & Umur
    # Ganti baris insight di Tab 1 (setelah st.plotly_chart(fig_pyr,...)) menjadi seperti ini:
    insight("<strong>Interpretasi Demografi & Gender</strong> : Rasio jenis kelamin secara agregat menunjukkan populasi yang seimbang (Sex Ratio ~101). Namun, piramida penduduk memperlihatkan transisi struktural antar kohort: <strong>Laki-laki mendominasi kelompok usia muda hingga produktif awal</strong>, sementara <strong>Perempuan mendominasi secara absolut di kelompok usia lanjut (65+).</strong> Pergeseran rasio jenis kelamin yang tajam di puncak piramida ini menunjukkan adanya fenomena <i>feminisasi lansia</i>, yang menuntut program perlindungan sosial dan kesehatan yang lebih spesifik gender di masa depan.")

    st.markdown("<br>", unsafe_allow_html=True)

    col_kep, col_edu = st.columns([1, 1.2], gap="large")

    with col_kep:
        st.markdown('<div class="sec-title">Kepadatan Penduduk per Kecamatan (Jiwa/km²)</div>', unsafe_allow_html=True)
        top_kep = df_kep.sort_values('Kepadatan', ascending=True).tail(10)
        
        fig_kep = go.Figure(go.Bar(
            x=top_kep['Kepadatan'], y=top_kep['Kecamatan'], orientation='h', marker=dict(color=C["teal"], opacity=0.85),
            text=[f"{v:,}" for v in top_kep['Kepadatan']], textposition='outside', textfont=dict(color=C["text"], size=11),
            cliponaxis=False 
        ))
        
        fig_kep.update_layout(**pro_layout(
            height=450, 
            xaxis=dict(visible=False, range=[0, top_kep['Kepadatan'].max() * 1.2]), 
            yaxis=dict(showgrid=False), 
            legend=dict(visible=False)
        ))
        st.plotly_chart(fig_kep, use_container_width=True, config=PCFG)

    with col_edu:
        st.markdown('<div class="sec-title">Tingkat Pendidikan Tertinggi yang Ditamatkan (%)</div>', unsafe_allow_html=True)
        
        # --- PERBAIKAN 2: FILTER GRAFIK PENDIDIKAN ---
        edu_filter = st.radio(
            "Tampilan Grafik:", 
            ["Laki-Laki & Perempuan", "Total Gabungan"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        edu_short = {
            'Tidak mempunyai ijazah': 'Tidak Punya<br>Ijazah',
            'Perguruan Tinggi': 'Perguruan<br>Tinggi'
        }
        df_edu = df_ijazah.copy()
        df_edu['Ijazah_Short'] = df_edu['Ijazah'].replace(edu_short)

        fig_edu = go.Figure()
        
        if edu_filter == "Total Gabungan":
            # Karena datanya format persentase, rata-rata adalah proxy terdekat untuk total populasi gabungan
            df_edu['Total_Avg'] = (df_edu['Laki_Laki'] + df_edu['Perempuan']) / 2
            
            fig_edu.add_trace(go.Bar(
                name='Total', x=df_edu['Ijazah_Short'], y=df_edu['Total_Avg'], 
                marker=dict(color=C["violet"], opacity=0.85),
                text=[f"{v:.1f}%" for v in df_edu['Total_Avg']], textposition='outside',
                cliponaxis=False
            ))
            y_max = df_edu['Total_Avg'].max() * 1.25
        else:
            fig_edu.add_trace(go.Bar(
                name='Laki-Laki', x=df_edu['Ijazah_Short'], y=df_edu['Laki_Laki'], 
                marker=dict(color=C["sky"], opacity=0.85),
                text=[f"{v:.1f}%" for v in df_edu['Laki_Laki']], textposition='outside',
                cliponaxis=False
            ))
            fig_edu.add_trace(go.Bar(
                name='Perempuan', x=df_edu['Ijazah_Short'], y=df_edu['Perempuan'], 
                marker=dict(color=C["rose"], opacity=0.85),
                text=[f"{v:.1f}%" for v in df_edu['Perempuan']], textposition='outside',
                cliponaxis=False
            ))
            y_max = max(df_edu['Laki_Laki'].max(), df_edu['Perempuan'].max()) * 1.25
            
        fig_edu.update_layout(**pro_layout(
            barmode='group', height=400, 
            xaxis=dict(tickangle=0, automargin=True),
            yaxis=dict(range=[0, y_max])
        ))
        st.plotly_chart(fig_edu, use_container_width=True, config=PCFG)
        
    insight("<strong>Interpretasi Pendidikan Dasar</strong> : Tingginya capaian pendidikan (terutama lulusan SMA dan Perguruan Tinggi yang merata antar gender) menghasilkan pasokan <i>skilled labor</i> yang sangat ideal untuk menopang sektor jasa dan ekonomi kreatif.")

# ── TAB 2: KETENAGAKERJAAN ──
with tab2:
    col_donut, col_status = st.columns([1, 1.2], gap="large")

    with col_donut:
        st.markdown('<div class="sec-title">Penduduk Bekerja Menurut Lapangan Pekerjaan Utama</div>', unsafe_allow_html=True)
        fig_donut = go.Figure(go.Pie(
            labels=df_lap['Kategori'], values=df_lap['Jumlah'], hole=0.6,
            marker=dict(colors=[C["amber"], C["sky"], C["teal"]], line=dict(color=C["bg"], width=3)),
            textinfo='percent', hoverinfo='label+percent+value'
        ))
        fig_donut.update_layout(**pro_layout(
            margin=dict(t=60, b=10, l=10, r=10)
        ))
        st.plotly_chart(fig_donut, use_container_width=True, config=PCFG)

    with col_status:
        st.markdown('<div class="sec-title">Penduduk Bekerja Menurut Status Pekerjaan Utama</div>', unsafe_allow_html=True)
        
        status_short = {
            'Berusaha sendiri': 'Berusaha<br>Sendiri',
            'Berusaha dibantu buruh tidak tetap/buruh tidak dibayar': 'Dibantu Buruh<br>Tidak Tetap',
            'Berusaha dibantu buruh tetap/buruh dibayar': 'Dibantu Buruh<br>Tetap',
            'Buruh/Karyawan/Pegawai': 'Buruh /<br>Karyawan',
            'Pekerja bebas': 'Pekerja<br>Bebas',
            'Pekerja keluarga/tak dibayar': 'Pekerja<br>Keluarga',
        }
        df_st = df_status.copy()
        df_st['Status_Short'] = df_st['Status'].map(status_short).fillna(df_st['Status'])
        df_st = df_st.sort_values('Jumlah', ascending=False)

        fig_stat = go.Figure()
        fig_stat.add_trace(go.Bar(name='Laki-Laki', x=df_st['Status_Short'], y=df_st['Laki_Laki'], marker=dict(color=C["sky"], opacity=0.85)))
        fig_stat.add_trace(go.Bar(name='Perempuan', x=df_st['Status_Short'], y=df_st['Perempuan'], marker=dict(color=C["rose"], opacity=0.85)))
        
        fig_stat.update_layout(**pro_layout(
            barmode='group', height=420, 
            xaxis=dict(tickangle=0, automargin=True)
        ))
        st.plotly_chart(fig_stat, use_container_width=True, config=PCFG)

    insight("<strong>Interpretasi Ketenagakerjaan</strong> : Serapan tenaga kerja mayoritas terpusat di sektor Jasa dan Perdagangan, berbanding lurus dengan tingginya pekerja berstatus Buruh/Karyawan/Pegawai. Dominasi sektor formal dan tersier ini mengonfirmasi karakteristik Bandung sebagai kota metropolitan yang roda ekonominya digerakkan oleh sektor layanan dan konsumsi, bukan industri padat karya.")

# ── TAB 3: DISTRIBUSI SPASIAL ──
with tab3:
    st.markdown('<div class="sec-title">Pemetaan Potensi Pasar F&B: Kepadatan Penduduk vs Ketersediaan Restoran</div>', unsafe_allow_html=True)

    df_spasial = df_merge.copy().sort_values('Kepadatan', ascending=False)
    
    fig_spasial = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_spasial.add_trace(go.Bar(
        name='Kepadatan (Jiwa/km²)', 
        x=df_spasial['Kecamatan'], 
        y=df_spasial['Kepadatan'], 
        marker=dict(color=C["surface2"], line=dict(color=C["border"], width=1)),
        hovertemplate='<b>%{x}</b><br>Kepadatan: %{y:,} jiwa/km²<extra></extra>'
    ), secondary_y=False)
    
    fig_spasial.add_trace(go.Scatter(
        name='Jumlah Restoran (Unit)', 
        x=df_spasial['Kecamatan'], 
        y=df_spasial['Restoran'], 
        mode='lines+markers',
        marker=dict(color=C["amber"], size=8), 
        line=dict(width=3, shape='spline'),
        hovertemplate='<b>%{x}</b><br>Restoran: %{y} unit<extra></extra>'
    ), secondary_y=True)

    fig_spasial.update_layout(**pro_layout(
        height=550, 
        xaxis=dict(tickangle=-45, automargin=True, tickfont=dict(size=10)),
        yaxis=dict(title="Kepadatan (Jiwa/km²)", showgrid=True),
        yaxis2=dict(title="Jumlah Restoran (Unit)", showgrid=False, tickfont=dict(color=C["amber"]))
    ))
    st.plotly_chart(fig_spasial, use_container_width=True, config=PCFG)
    
    insight("<strong>Interpretasi Spasial</strong> : Distribusi usaha kuliner (restoran) ternyata belum berbanding lurus dengan tingkat kepadatan penduduk. Kecamatan yang sangat padat (seperti Bojongloa Kaler) namun memiliki garis jumlah restoran yang rendah mengindikasikan adanya <strong><i>unmet demand</i></strong> (permintaan pasar yang belum terpenuhi). Area <i>blank spot</i> inilah yang menjadi peluang emas untuk ekspansi bisnis F&B.")

# ═════════════════════════════════════════════════════════════════════
#  FOOTER / WATERMARK
# ═════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="
    margin-top: 4rem; 
    padding-top: 1.5rem; 
    border-top: 1px solid {C['border']}; 
    text-align: center; 
    color: {C['muted']}; 
    font-family: 'Inter', sans-serif; 
    font-size: 0.7rem; 
    letter-spacing: 1.5px;
    text-transform: uppercase;
">
    Created by <strong style="color: {C['text']}; font-weight: 600;">Sulthon Avidi</strong> &nbsp;•&nbsp; 2026
</div>
""", unsafe_allow_html=True)
