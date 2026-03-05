# ╔══════════════════════════════════════════════════════════════════════╗
# ║     PROFIL KEPENDUDUKAN KOTA BANDUNG  ·  Official BPS Format         ║
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
# PAGE CONFIG & CSS
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Profil Kependudukan Bandung",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Palet Elegan Modern (Midnight Slate)
BG_PAGE  = "#0F172A" # Slate 900
BG_CARD  = "#1E293B" # Slate 800
BORDER   = "#334155" # Slate 700
TEXT_PRI = "#F8FAFC" # Slate 50
TEXT_SEC = "#94A3B8" # Slate 400

COLOR_1 = "#3B82F6" # Blue (Laki-laki / Utama)
COLOR_2 = "#F43F5E" # Rose (Perempuan)
COLOR_3 = "#10B981" # Teal
COLOR_4 = "#F59E0B" # Amber

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap');

#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none; }}

html, body, [data-testid="stAppViewContainer"], .main {{
    background-color: {BG_PAGE} !important;
    font-family: 'Inter', sans-serif;
    color: {TEXT_PRI};
}}

.hero-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.2rem; font-weight: 700;
    color: {TEXT_PRI}; margin: 1rem 0 0.5rem; letter-spacing: -0.5px;
}}
.hero-sub {{ font-size: 1.05rem; color: {TEXT_SEC}; margin: 0 0 2rem 0; }}

/* Global KPI Cards */
.kpi-container {{ display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }}
.kpi-wrap {{
    background: {BG_CARD}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 1.5rem; flex: 1; min-width: 200px;
    border-top: 3px solid {COLOR_1};
}}
.kpi-wrap:nth-child(2) {{ border-top-color: {COLOR_2}; }}
.kpi-wrap:nth-child(3) {{ border-top-color: {COLOR_3}; }}
.kpi-wrap:nth-child(4) {{ border-top-color: {COLOR_4}; }}

.kpi-label {{ font-size: 0.8rem; color: {TEXT_SEC}; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 0.5rem; }}
.kpi-val {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2rem; font-weight: 700; color: {TEXT_PRI}; margin-bottom: 0.2rem; }}
.kpi-sub {{ font-size: 0.8rem; color: {TEXT_SEC}; }}

.sec-title {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.2rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: {TEXT_PRI}; }}
.divider {{ height: 1px; background: {BORDER}; border: none; margin: 2rem 0; }}

/* Tabs Styling */
[data-testid="stTabs"] [role="tablist"] {{ border-bottom: 2px solid {BORDER}; padding-bottom: 0; gap: 1.5rem; }}
[data-testid="stTabs"] [role="tab"] {{ font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.95rem !important; color: {TEXT_SEC} !important; background: transparent !important; border: none !important; padding: 0.8rem 0 !important; }}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{ color: {TEXT_PRI} !important; border-bottom: 2px solid {COLOR_1} !important; }}

[data-testid="stInfo"] {{ background: {BG_CARD} !important; border: 1px solid {BORDER} !important; border-left: 4px solid {COLOR_1} !important; border-radius: 8px !important; }}
[data-testid="stInfo"] p {{ color: #E2E8F0 !important; font-size: 0.95rem !important; line-height: 1.6 !important; }}
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
#  PLOTLY LAYOUT MASTER (ANTI-NABRAK & ANTI-MIRING)
# ═════════════════════════════════════════════════════════════════════
def clean_layout(**kwargs):
    base = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_SEC, size=11),
        margin=dict(l=10, r=10, t=60, b=50), 
        xaxis=dict(showgrid=False, zeroline=False, automargin=True, tickangle=0),
        yaxis=dict(showgrid=True, gridcolor=BORDER, zeroline=False, automargin=True),
        legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
        hoverlabel=dict(bgcolor=BG_CARD, font=dict(color=TEXT_PRI), bordercolor=BORDER)
    )
    base.update(kwargs)
    return base


# ═════════════════════════════════════════════════════════════════════
#  UI RENDERING
# ═════════════════════════════════════════════════════════════════════

st.markdown('<div class="hero-title">Profil Kependudukan Kota Bandung 2025</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Ringkasan Eksekutif Data Demografi, Ketenagakerjaan, dan Distribusi Spasial (Sumber: BPS)</div>', unsafe_allow_html=True)

# GLOBAL KPI CARDS
k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "Total Penduduk", f"{total_penduduk:,.0f}", "Jiwa"),
    (k2, "Kepadatan Penduduk", f"{kepadatan_kota:,.0f}", "Jiwa per km²"),
    (k3, "Total PDRB", f"Rp {total_pdrb/1000:.1f} T", "Atas Dasar Harga Berlaku"),
    (k4, "Rasio Ketergantungan", str(dep_ratio), "Tanggungan per 100 usia produktif"),
]

st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
for col, label, val, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-label">{label}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs([
    "Demografi & Pendidikan", "Ketenagakerjaan", "Distribusi Spasial"
])

# ── TAB 1: DEMOGRAFI & PENDIDIKAN ──
with tab1:
    st.markdown('<div class="sec-title">Piramida Penduduk Kota Bandung</div>', unsafe_allow_html=True)

    kel = df_umur['Kelompok_Umur'].tolist()
    laki = df_umur['Laki_Laki'].tolist()
    puan = df_umur['Perempuan'].tolist()

    fig_pyr = go.Figure()
    fig_pyr.add_trace(go.Bar(y=kel, x=[-v for v in laki], name='Laki-Laki', orientation='h', marker=dict(color=COLOR_1)))
    fig_pyr.add_trace(go.Bar(y=kel, x=puan, name='Perempuan', orientation='h', marker=dict(color=COLOR_2)))

    max_val = max(max(laki), max(puan)) * 1.15
    ticks = [int(v) for v in np.linspace(-max_val, max_val, 7)]
    tlabel = [f"{abs(v)//1000:.0f}k" for v in ticks]

    fig_pyr.add_hrect(
        y0=2.5, y1=12.5, fillcolor="#1E293B", opacity=0.8, line_width=0, layer="below",
        annotation_text="Usia Produktif (15-64)", annotation_position="top right", annotation_font=dict(color=TEXT_SEC)
    )

    fig_pyr.update_layout(**clean_layout(
        barmode='overlay', height=400,
        xaxis=dict(range=[-max_val, max_val], tickvals=ticks, ticktext=tlabel, showgrid=True, gridcolor=BORDER),
        yaxis=dict(showgrid=False)
    ))
    st.plotly_chart(fig_pyr, use_container_width=True, config={'displayModeBar': False})

    col_kep, col_edu = st.columns([1, 1], gap="large")

    with col_kep:
        st.markdown('<div class="sec-title">Kepadatan Penduduk per Kecamatan (Jiwa/km²)</div>', unsafe_allow_html=True)
        top_kep = df_kep.sort_values('Kepadatan', ascending=True).tail(10)
        
        fig_kep = go.Figure(go.Bar(
            x=top_kep['Kepadatan'], y=top_kep['Kecamatan'], orientation='h', marker=dict(color=COLOR_3),
            text=[f"{v:,}" for v in top_kep['Kepadatan']], textposition='outside', textfont=dict(color=TEXT_PRI),
            cliponaxis=False # ANTI-KEPOTONG
        ))
        
        # Tambah margin khusus X biar angka yg panjang dapet space
        fig_kep.update_layout(**clean_layout(
            height=400, 
            xaxis=dict(visible=False, range=[0, top_kep['Kepadatan'].max() * 1.2]), 
            yaxis=dict(showgrid=False), 
            legend=dict(visible=False)
        ))
        st.plotly_chart(fig_kep, use_container_width=True, config={'displayModeBar': False})

    with col_edu:
        st.markdown('<div class="sec-title">Tingkat Pendidikan Tertinggi yang Ditamatkan (%)</div>', unsafe_allow_html=True)
        
        edu_short = {
            'Tidak mempunyai ijazah': 'Tidak Punya<br>Ijazah',
            'Perguruan Tinggi': 'Perguruan<br>Tinggi'
        }
        df_edu = df_ijazah.copy()
        df_edu['Ijazah_Short'] = df_edu['Ijazah'].replace(edu_short)

        fig_edu = go.Figure()
        fig_edu.add_trace(go.Bar(
            name='Laki-Laki', x=df_edu['Ijazah_Short'], y=df_edu['Laki_Laki'], 
            marker=dict(color=COLOR_1),
            text=[f"{v:.1f}%" for v in df_edu['Laki_Laki']], textposition='outside',
            cliponaxis=False
        ))
        fig_edu.add_trace(go.Bar(
            name='Perempuan', x=df_edu['Ijazah_Short'], y=df_edu['Perempuan'], 
            marker=dict(color=COLOR_2),
            text=[f"{v:.1f}%" for v in df_edu['Perempuan']], textposition='outside',
            cliponaxis=False
        ))
        
        fig_edu.update_layout(**clean_layout(
            barmode='group', height=400, 
            xaxis=dict(tickangle=0, automargin=True),
            yaxis=dict(range=[0, max(df_edu['Laki_Laki'].max(), df_edu['Perempuan'].max()) * 1.25])
        ))
        st.plotly_chart(fig_edu, use_container_width=True, config={'displayModeBar': False})

# ── TAB 2: KETENAGAKERJAAN ──
with tab2:
    col_donut, col_status = st.columns([1, 1.2], gap="large")

    with col_donut:
        st.markdown('<div class="sec-title">Penduduk Bekerja Menurut Lapangan Pekerjaan Utama</div>', unsafe_allow_html=True)
        fig_donut = go.Figure(go.Pie(
            labels=df_lap['Kategori'], values=df_lap['Jumlah'], hole=0.6,
            marker=dict(colors=[COLOR_4, COLOR_1, COLOR_3], line=dict(color=BG_PAGE, width=3)),
            textinfo='percent', hoverinfo='label+percent+value'
        ))
        fig_donut.update_layout(**clean_layout(
            margin=dict(t=60, b=10, l=10, r=10)
        ))
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

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
        fig_stat.add_trace(go.Bar(name='Laki-Laki', x=df_st['Status_Short'], y=df_st['Laki_Laki'], marker=dict(color=COLOR_1)))
        fig_stat.add_trace(go.Bar(name='Perempuan', x=df_st['Status_Short'], y=df_st['Perempuan'], marker=dict(color=COLOR_2)))
        
        fig_stat.update_layout(**clean_layout(
            barmode='group', height=420, 
            xaxis=dict(tickangle=0, automargin=True)
        ))
        st.plotly_chart(fig_stat, use_container_width=True, config={'displayModeBar': False})

# ── TAB 3: DISTRIBUSI SPASIAL (KEPADATAN VS KOMERSIAL) ──
with tab3:
    st.markdown('<div class="sec-title">Analisis Titik Jenuh: Kepadatan Penduduk vs Ketersediaan Sarana Komersial</div>', unsafe_allow_html=True)

    # Urutkan berdasarkan Kepadatan secara descending
    df_spasial = df_merge.copy().sort_values('Kepadatan', ascending=False)
    
    fig_spasial = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Bar Chart: Sekarang menggunakan Kepadatan, bukan Jumlah Penduduk
    fig_spasial.add_trace(go.Bar(
        name='Kepadatan (Jiwa/km²)', 
        x=df_spasial['Kecamatan'], 
        y=df_spasial['Kepadatan'], 
        marker=dict(color=BORDER),
        hovertemplate='<b>%{x}</b><br>Kepadatan: %{y:,} jiwa/km²<extra></extra>'
    ), secondary_y=False)
    
    # Line Chart: Jumlah Restoran
    fig_spasial.add_trace(go.Scatter(
        name='Jumlah Restoran (Unit)', 
        x=df_spasial['Kecamatan'], 
        y=df_spasial['Restoran'], 
        mode='lines+markers',
        marker=dict(color=COLOR_4, size=8), 
        line=dict(width=3),
        hovertemplate='<b>%{x}</b><br>Restoran: %{y} unit<extra></extra>'
    ), secondary_y=True)

    fig_spasial.update_layout(**clean_layout(
        height=550, 
        xaxis=dict(tickangle=-45, automargin=True, tickfont=dict(size=10)),
        yaxis=dict(title="Kepadatan (Jiwa/km²)", showgrid=True, gridcolor=BORDER),
        yaxis2=dict(title="Jumlah Restoran (Unit)", showgrid=False, tickfont=dict(color=COLOR_4))
    ))
    st.plotly_chart(fig_spasial, use_container_width=True, config={'displayModeBar': False})
    
    st.info("💡 **Diagnosis Spasial:** Perhatikan area di mana batang abu-abu (Kepadatan) sangat tinggi tetapi garis oranye (Restoran) sangat rendah. Area tersebut adalah **zona unmet demand** yang sangat potensial untuk pembukaan cabang baru karena persaingan belum sepadat populasinya.")
