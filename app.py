# ══════════════════════════════════════════════════════════
#  BANDUNG CITY INTELLIGENCE DASHBOARD
#  Data: BPS Kota Bandung 2025  ·  Streamlit + Plotly
# ══════════════════════════════════════════════════════════

import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Bandung City Dashboard 2025",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════
#  DESIGN TOKENS
# ══════════════════════════════════════════════════════════
C = {
    "bg"       : "#111318",
    "surface"  : "#191C24",
    "surface2" : "#1F2232",
    "border"   : "#2A2D3E",
    "text"     : "#E8EAF0",
    "muted"    : "#6B7280",
    "amber"    : "#F5A623",
    "sky"      : "#38BDF8",
    "teal"     : "#2DD4BF",
    "rose"     : "#FB7185",
    "violet"   : "#A78BFA",
    "green"    : "#4ADE80",
}

# ── CSS ───────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Nunito:wght@400;500;600&display=swap');

/* ── Kill Streamlit chrome ── */
#MainMenu,footer,header,.stDeployButton{{visibility:hidden}}
[data-testid="stToolbar"],[data-testid="stDecoration"]{{display:none}}

/* ── Root ── */
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>.main,
[data-testid="block-container"]{{
    background:{C["bg"]} !important;
    font-family:'Nunito',sans-serif;
    color:{C["text"]};
}}
[data-testid="stSidebar"]{{background:#0D0F14 !important}}

/* ── Typography ── */
h1,h2,h3,h4{{font-family:'Sora',sans-serif; color:{C["text"]}}}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"]{{
    background:{C["surface"]};
    border:1px solid {C["border"]};
    border-radius:12px; padding:4px; gap:4px;
    border-bottom:none !important;
}}
[data-testid="stTabs"] [role="tab"]{{
    font-family:'Sora',sans-serif !important;
    font-size:.82rem !important; font-weight:600 !important;
    color:{C["muted"]} !important;
    border-radius:9px !important; border:none !important;
    padding:.45rem 1.1rem !important;
    transition:all .15s !important;
    white-space:nowrap !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{{
    background:{C["surface2"]} !important;
    color:{C["amber"]} !important;
    border:1px solid {C["amber"]}44 !important;
}}

/* ── KPI metric card ── */
.m-card{{
    background:{C["surface"]};
    border:1px solid {C["border"]};
    border-radius:14px;
    padding:1.25rem 1.35rem;
    display:flex; flex-direction:column; gap:.18rem;
    position:relative; overflow:hidden;
    transition:border-color .2s;
}}
.m-card:hover{{border-color:{C["amber"]}66}}
.m-card-bar{{position:absolute;top:0;left:0;right:0;height:2px;border-radius:14px 14px 0 0}}
.m-card-label{{font-size:.67rem;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:{C["muted"]}}}
.m-card-value{{font-family:'Sora',sans-serif;font-size:1.85rem;font-weight:800;line-height:1.1}}
.m-card-sub{{font-size:.75rem;color:{C["muted"]}}}

/* ── Section title ── */
.s-title{{font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:700;color:{C["text"]};margin:0 0 .1rem}}
.s-sub{{font-size:.82rem;color:{C["muted"]};margin:0 0 .9rem;line-height:1.5}}

/* ── Insight card ── */
.insight{{
    background:linear-gradient(135deg,{C["surface"]} 0%,{C["surface2"]} 100%);
    border:1px solid {C["border"]};
    border-left:3px solid {C["amber"]};
    border-radius:0 12px 12px 0;
    padding:1rem 1.25rem; margin-top:.5rem;
}}
.insight.sky{{border-left-color:{C["sky"]}}}
.insight.teal{{border-left-color:{C["teal"]}}}
.insight.rose{{border-left-color:{C["rose"]}}}
.insight-head{{font-family:'Sora',sans-serif;font-size:.72rem;font-weight:700;
    letter-spacing:1px;text-transform:uppercase;color:{C["amber"]};margin-bottom:.4rem}}
.insight-head.sky{{color:{C["sky"]}}}
.insight-head.teal{{color:{C["teal"]}}}
.insight-head.rose{{color:{C["rose"]}}}
.insight-body{{font-size:.86rem;color:{C["text"]};line-height:1.65}}
.insight-body strong{{color:{C["amber"]}}}
.insight-body.sky strong{{color:{C["sky"]}}}
.insight-body.teal strong{{color:{C["teal"]}}}
.insight-body.rose strong{{color:{C["rose"]}}}

/* ── Chart wrapper ── */
.chart-wrap{{
    background:{C["surface"]};
    border:1px solid {C["border"]};
    border-radius:14px;padding:1.1rem 1.2rem;
}}

/* ── Hero ── */
.hero{{
    background:linear-gradient(120deg,#0C0E15 0%,#141828 55%,#10192E 100%);
    border:1px solid {C["border"]};border-radius:16px;
    padding:2rem 2.5rem;margin-bottom:1.5rem;
    position:relative;overflow:hidden;
}}
.hero::after{{
    content:'';position:absolute;
    top:-60px;right:-60px;
    width:320px;height:320px;
    background:radial-gradient(circle,{C["amber"]}18 0%,transparent 65%);
    border-radius:50%;pointer-events:none;
}}
.hero-kicker{{font-size:.68rem;font-weight:700;letter-spacing:2px;
    text-transform:uppercase;color:{C["amber"]};margin-bottom:.45rem}}
.hero-title{{font-family:'Sora',sans-serif;font-size:2rem;font-weight:800;
    color:{C["text"]};margin:0 0 .4rem;line-height:1.2}}
.hero-title span{{color:{C["amber"]}}}
.hero-desc{{font-size:.88rem;color:{C["muted"]};max-width:560px;line-height:1.6}}
.pill-row{{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.9rem}}
.pill{{background:{C["surface2"]};border:1px solid {C["border"]};
    border-radius:20px;padding:.18rem .7rem;
    font-size:.7rem;font-weight:600;color:{C["muted"]}}}

/* ── st.info override ── */
[data-testid="stInfo"]{{
    background:{C["surface2"]} !important;
    border:1px solid {C["border"]} !important;
    border-left:3px solid {C["amber"]} !important;
    border-radius:0 10px 10px 0 !important;
    color:{C["text"]} !important;
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  BULLETPROOF DATA UTILITIES  (unchanged)
# ══════════════════════════════════════════════════════════

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
    return s in {'jumlah','total','kota bandung','kota bandung (total)','semua status','nan'}

def find_keyword_value(df, keyword, val_col=1, key_col=0):
    for i, cell in enumerate(df.iloc[:, key_col].astype(str)):
        if keyword.lower() in cell.lower():
            v = df.iloc[i, val_col]
            if not (isinstance(v, float) and np.isnan(v)): return v
    return None

def safe_block(raw, col_indices, col_names, header_keyword,
               header_col=0, numeric_check_name=None):
    hdr = find_header_row(raw, header_keyword, col=header_col)
    hdr = hdr if hdr is not None else 0
    block = raw.iloc[hdr + 1:, col_indices].copy()
    block.columns = col_names
    block = block[~block[col_names[0]].astype(str).apply(is_aggregate_row)]
    check = numeric_check_name or col_names[1]
    block = block[block[check].apply(lambda x: extract_number(x) is not None)]
    return block.reset_index(drop=True)


# ══════════════════════════════════════════════════════════
#  LOAD DATA  (unchanged)
# ══════════════════════════════════════════════════════════

FILE = "Data_Kota_Bandung.xlsx"

@st.cache_data(show_spinner="Memuat data BPS Kota Bandung 2025…")
def load_data():
    raw_umur = pd.read_excel(FILE, sheet_name='Penduduk menurut umur & jk', header=None)
    df_umur = safe_block(raw_umur,[0,1,2,3],
        ['Kelompok_Umur','Laki_Laki','Perempuan','Jumlah'],
        header_keyword='Kelompok', numeric_check_name='Laki_Laki')
    for c in ['Laki_Laki','Perempuan','Jumlah']:
        df_umur[c] = df_umur[c].apply(extract_number)

    raw_kem = pd.read_excel(FILE, sheet_name='kemiskinan', header=None)
    pct_raw   = find_keyword_value(raw_kem,'Persentase')
    jml_raw   = find_keyword_value(raw_kem,'Jumlah Penduduk Miskin')
    garis_raw = find_keyword_value(raw_kem,'Garis')
    pct_num    = extract_number(pct_raw)
    pct_miskin = round(pct_num * 100, 2) if pct_num else 0.0
    jml_miskin_str = str(jml_raw) if jml_raw is not None else "N/A"
    garis_str      = str(garis_raw) if garis_raw is not None else "N/A"

    raw_pend = pd.read_excel(FILE, sheet_name='pendidikan', header=None)
    df_ijazah = safe_block(raw_pend,[4,5,6],
        ['Ijazah','Laki_Laki','Perempuan'],
        header_keyword='Ijazah', header_col=4, numeric_check_name='Laki_Laki')
    for c in ['Laki_Laki','Perempuan']:
        df_ijazah[c] = df_ijazah[c].apply(extract_number)

    raw_pek = pd.read_excel(FILE, sheet_name='pekerjaan', header=None)
    df_status = safe_block(raw_pek,[0,1,2,3],
        ['Status','Laki_Laki','Perempuan','Jumlah'],
        header_keyword='Status Pekerjaan', header_col=0, numeric_check_name='Laki_Laki')
    for c in ['Laki_Laki','Perempuan','Jumlah']:
        df_status[c] = df_status[c].apply(extract_number)
    df_lap = safe_block(raw_pek,[5,6,7,8,9],
        ['Kategori','Laki_Laki','Perempuan','Jumlah','Persen'],
        header_keyword='Kategori', header_col=5, numeric_check_name='Jumlah')
    for c in ['Laki_Laki','Perempuan','Jumlah','Persen']:
        df_lap[c] = df_lap[c].apply(extract_number)

    raw_kep = pd.read_excel(FILE, sheet_name='kepadatan', header=None)
    df_kep = safe_block(raw_kep,[0,1,2],
        ['Kecamatan','Luas','Penduduk'],
        header_keyword='Kecamatan', numeric_check_name='Penduduk')
    df_kep['Luas']      = df_kep['Luas'].apply(extract_number)
    df_kep['Penduduk']  = df_kep['Penduduk'].apply(extract_number)
    df_kep['Kepadatan'] = (df_kep['Penduduk'] / df_kep['Luas']).round(0).astype(int)

    raw_kom = pd.read_excel(FILE, sheet_name='komersial', header=None)
    df_kom = safe_block(raw_kom,[0,1],
        ['Kecamatan','Restoran'],
        header_keyword='Kecamatan', numeric_check_name='Restoran')
    df_kom['Restoran'] = df_kom['Restoran'].apply(extract_number).astype(int)

    raw_eko = pd.read_excel(FILE, sheet_name='ekonomi', header=None)
    df_eko_all = safe_block(raw_eko,[0,1],
        ['Kategori','PDRB'],
        header_keyword='Kategori', numeric_check_name='PDRB')
    df_eko_all['PDRB'] = df_eko_all['PDRB'].apply(extract_number)
    is_total   = df_eko_all['Kategori'].astype(str).str.lower().str.contains('total')
    total_pdrb = df_eko_all.loc[is_total,'PDRB'].values[0] if is_total.any() else 0.0
    df_eko_sek = df_eko_all[~is_total].dropna(subset=['PDRB']).reset_index(drop=True)

    raw_gh = pd.read_excel(FILE, sheet_name='gaya hidup', header=None)
    df_kend = safe_block(raw_gh,[0,1,2],
        ['Jenis_Kendaraan','Status','Total'],
        header_keyword='Jenis Kendaraan', numeric_check_name='Total')
    df_kend['Total'] = df_kend['Total'].apply(extract_number).astype(int)

    def _norm(s): return re.sub(r'[\s/\-_.,]','',str(s).lower())
    df_kep_m = df_kep.copy(); df_kom_m = df_kom.copy()
    df_kep_m['_k'] = df_kep_m['Kecamatan'].apply(_norm)
    df_kom_m['_k'] = df_kom_m['Kecamatan'].apply(_norm)
    df_merge = pd.merge(df_kep_m, df_kom_m[['_k','Restoran']],
                        on='_k', how='left').drop(columns=['_k'])
    df_merge['Restoran'] = df_merge['Restoran'].fillna(0).astype(int)

    return (df_umur, df_ijazah, df_status, df_lap,
            pct_miskin, jml_miskin_str, garis_str,
            df_kep, df_kom, df_eko_sek, total_pdrb,
            df_kend, df_merge)


(df_umur, df_ijazah, df_status, df_lap,
 pct_miskin, jml_miskin_str, garis_str,
 df_kep, df_kom, df_eko_sek, total_pdrb,
 df_kend, df_merge) = load_data()


# ══════════════════════════════════════════════════════════
#  DERIVED VALUES
# ══════════════════════════════════════════════════════════
total_penduduk = df_umur['Jumlah'].sum()
YOUNG = ['0–4','5–9','10–14']
OLD   = ['65–69','70–74','75+']
muda      = df_umur[df_umur['Kelompok_Umur'].isin(YOUNG)]['Jumlah'].sum()
tua       = df_umur[df_umur['Kelompok_Umur'].isin(OLD)]['Jumlah'].sum()
produktif = total_penduduk - muda - tua
dep_ratio = round((muda + tua) / produktif * 100, 1) if produktif > 0 else 0

motor_total  = df_kend[df_kend['Jenis_Kendaraan'].str.contains('Motor',case=False)]['Total'].sum()
motor_pribadi= df_kend[(df_kend['Jenis_Kendaraan'].str.contains('Motor',case=False))
                       & (df_kend['Status']=='Pribadi')]['Total'].sum()

jasa_persen  = df_lap[df_lap['Kategori'].str.lower()=='jasa']['Persen']
jasa_pct     = jasa_persen.values[0] if not jasa_persen.empty else 74.23

total_restoran = df_kom['Restoran'].sum()

pt_mask = df_ijazah['Ijazah'].str.contains('Perguruan',case=False,na=False)
pt_lk   = df_ijazah.loc[pt_mask,'Laki_Laki'].values[0] if pt_mask.any() else 19.6
pt_pr   = df_ijazah.loc[pt_mask,'Perempuan'].values[0] if pt_mask.any() else 19.7


# ══════════════════════════════════════════════════════════
#  CHART HELPERS
# ══════════════════════════════════════════════════════════
CHART_BG = "rgba(0,0,0,0)"

def base_layout(**kw):
    """Shared Plotly layout for all charts."""
    cfg = dict(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="Nunito", color=C["text"], size=12),
        margin=dict(l=4, r=4, t=36, b=4),
        hoverlabel=dict(
            bgcolor=C["surface2"],
            font=dict(family="Nunito", color=C["text"], size=12),
            bordercolor=C["border"],
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=C["muted"], size=11),
            orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5,
        ),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color=C["muted"],size=11),
                   linecolor=C["border"]),
        yaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color=C["muted"],size=11),
                   linecolor=C["border"]),
    )
    cfg.update(kw)
    return cfg

def subtle_grid_y():
    return dict(showgrid=True, gridcolor="rgba(42,45,62,0.6)", zeroline=False,
                tickfont=dict(color=C["muted"],size=11))

PCFG = {"displayModeBar": False}

def kpi(col, icon, label, value, sub, color):
    col.markdown(f"""
    <div class="m-card">
      <div class="m-card-bar" style="background:{color}"></div>
      <div class="m-card-label">{icon}&nbsp; {label}</div>
      <div class="m-card-value" style="color:{color}">{value}</div>
      <div class="m-card-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def section(title, sub=""):
    st.markdown(f'<div class="s-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="s-sub">{sub}</div>', unsafe_allow_html=True)

def insight(body, color="amber"):
    labels = {"amber":"Analisis","sky":"Analisis","teal":"Analisis","rose":"Analisis"}
    st.markdown(f"""
    <div class="insight {color if color!='amber' else ''}">
      <div class="insight-head {color if color!='amber' else ''}">📌 {labels.get(color,'Analisis')}</div>
      <div class="insight-body {color if color!='amber' else ''}">{body}</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-kicker">Kota Bandung · BPS 2025 · Jawa Barat</div>
  <div class="hero-title">City Intelligence <span>Dashboard</span></div>
  <p class="hero-desc">
    Ringkasan data ekonomi, demografi, bisnis, dan modal manusia Kota Bandung
    untuk mendukung pengambilan keputusan berbasis data.
  </p>
  <div class="pill-row">
    <span class="pill">🏙 2.548.784 Jiwa</span>
    <span class="pill">💰 PDRB Rp 404 T</span>
    <span class="pill">🗺 167 km² Luas Wilayah</span>
    <span class="pill">🍜 {total_restoran:,} Restoran</span>
    <span class="pill">🏍 {motor_total:,} Motor</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "📈  Ekonomi Makro",
    "🍜  Bisnis & Mobilitas",
    "👥  Modal Manusia",
])


# ╔════════════════════════════════════════════════════════╗
# ║  TAB 1 — EKONOMI MAKRO                               ║
# ╚════════════════════════════════════════════════════════╝
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI row ──────────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4, gap="small")
    kpi(c1,"🏙","Total Penduduk",  f"{total_penduduk/1e6:.2f} Juta",
        f"{total_penduduk:,} jiwa · luas 167,31 km²", C["amber"])
    kpi(c2,"💰","Total PDRB",      f"Rp {total_pdrb/1000:.0f} T",
        "Produk Domestik Regional Bruto 2025",       C["sky"])
    kpi(c3,"⚖","Dependency Ratio", f"{dep_ratio}",
        f"per 100 penduduk produktif (usia 15–64)",  C["teal"])
    kpi(c4,"🏚","Penduduk Miskin",  jml_miskin_str,
        f"{pct_miskin:.2f}% · garis {garis_str}",   C["rose"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PDRB ─────────────────────────────────────────────
    section("Kontribusi Sektor terhadap PDRB",
            "Nilai output ekonomi tiap sektor usaha utama (Miliar Rupiah), 2025")

    lmap = {
        "Perdagangan Besar dan Eceran; Reparasi Mobil & Motor": "Perdagangan & Eceran",
        "Industri Pengolahan":                "Industri Pengolahan",
        "Informasi dan Komunikasi":           "Informasi & Komunikasi",
        "Transportasi dan Pergudangan":       "Transportasi & Pergudangan",
        "Konstruksi":                         "Konstruksi",
        "Jasa Keuangan dan Asuransi":         "Jasa Keuangan & Asuransi",
        "Penyediaan Akomodasi dan Makan Minum":"Akomodasi & F&B",
        "Jasa Pendidikan":                    "Jasa Pendidikan",
    }
    df_p = df_eko_sek.copy().sort_values("PDRB", ascending=True)
    df_p["Label"] = df_p["Kategori"].map(lmap).fillna(df_p["Kategori"])
    df_p["Pct"]   = (df_p["PDRB"] / total_pdrb * 100).round(1)
    df_p["IsTop"] = df_p["PDRB"] == df_p["PDRB"].max()

    bar_colors = [C["amber"] if top else "rgba(56,189,248,0.6)"
                  for top in df_p["IsTop"]]
    text_vals  = [f" Rp {v/1000:.0f}T ({p}%)" if top else f" {p}%"
                  for v,p,top in zip(df_p["PDRB"], df_p["Pct"], df_p["IsTop"])]

    fig_pdrb = go.Figure(go.Bar(
        x=df_p["PDRB"], y=df_p["Label"], orientation="h",
        marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0)")),
        text=text_vals, textposition="outside",
        textfont=dict(size=11, color=C["text"]),
        hovertemplate="<b>%{y}</b><br>Rp %{x:,.0f} Miliar<extra></extra>",
        cliponaxis=False,
    ))
    fig_pdrb.update_layout(**base_layout(
        height=310,
        margin=dict(l=4, r=160, t=10, b=4),
        title=dict(text="PDRB per Sektor Usaha  (2025)",
                   font=dict(family="Sora",size=13,color=C["muted"]), x=0),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color=C["text"], size=12)),
    ))
    st.plotly_chart(fig_pdrb, use_container_width=True, config=PCFG)

    insight(
        f"<strong>Perdagangan & Eceran</strong> mendominasi PDRB dengan kontribusi terbesar "
        f"(<strong>Rp {df_p.loc[df_p['IsTop'],'PDRB'].values[0]/1000:.0f} T, "
        f"{df_p.loc[df_p['IsTop'],'Pct'].values[0]:.1f}%</strong>). "
        f"Gabungan sektor Jasa (Perdagangan + Informasi + Keuangan + Pendidikan) "
        f"menyumbang lebih dari 60% ekonomi kota — Bandung adalah kota jasa, bukan kota industri. "
        f"Peluang investasi terbesar justru di sektor <strong>Informasi & Komunikasi</strong> "
        f"yang tumbuh cepat namun kontribusinya masih di urutan ketiga.",
        "amber"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Lapangan Pekerjaan + Status Pekerjaan ────────────
    section("Struktur Ketenagakerjaan",
            "Siapa yang bekerja dan di mana — 1,27 juta penduduk usia produktif aktif bekerja")

    col_donut, col_stat = st.columns([1, 1.4], gap="large")

    with col_donut:
        total_workers = df_lap["Jumlah"].sum()
        fig_dn = go.Figure(go.Pie(
            labels=df_lap["Kategori"].tolist(),
            values=df_lap["Jumlah"].tolist(),
            hole=0.62,
            marker=dict(colors=[C["teal"], C["sky"], C["amber"]],
                        line=dict(color=C["surface"], width=3)),
            textinfo="label+percent",
            textfont=dict(size=12, color=C["text"]),
            hovertemplate="<b>%{label}</b><br>%{value:,} pekerja (%{percent})<extra></extra>",
            pull=[0.02, 0, 0.04],
            direction="clockwise",
            rotation=90,
        ))
        fig_dn.add_annotation(
            text=f"<b>{total_workers/1e6:.2f}Jt</b><br><span style='font-size:10px'>Pekerja</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=C["text"], family="Sora"),
        )
        fig_dn.update_layout(**base_layout(
            height=290, margin=dict(l=0,r=0,t=10,b=40),
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        font=dict(color=C["muted"],size=11)),
        ))
        st.plotly_chart(fig_dn, use_container_width=True, config=PCFG)

    with col_stat:
        short_map = {
            "Berusaha sendiri":                                       "Berusaha Sendiri",
            "Berusaha dibantu buruh tidak tetap/buruh tidak dibayar": "Buruh Tidak Tetap",
            "Berusaha dibantu buruh tetap/buruh dibayar":             "Buruh Tetap",
            "Buruh/Karyawan/Pegawai":                                 "Karyawan / Buruh",
            "Pekerja bebas":                                          "Pekerja Bebas",
            "Pekerja keluarga/tak dibayar":                           "Pekerja Keluarga",
        }
        df_st = df_status.copy()
        df_st["Label"] = df_st["Status"].map(short_map).fillna(df_st["Status"])
        df_st = df_st.sort_values("Jumlah", ascending=False)

        fig_st = go.Figure()
        fig_st.add_trace(go.Bar(
            name="Laki-Laki", x=df_st["Label"], y=df_st["Laki_Laki"],
            marker=dict(color=C["sky"], opacity=0.85),
            text=[f"{int(v/1000)}k" for v in df_st["Laki_Laki"]],
            textposition="outside", textfont=dict(size=10, color=C["muted"]),
            hovertemplate="<b>%{x}</b><br>Laki-Laki: %{y:,}<extra></extra>",
        ))
        fig_st.add_trace(go.Bar(
            name="Perempuan", x=df_st["Label"], y=df_st["Perempuan"],
            marker=dict(color=C["rose"], opacity=0.85),
            text=[f"{int(v/1000)}k" for v in df_st["Perempuan"]],
            textposition="outside", textfont=dict(size=10, color=C["muted"]),
            hovertemplate="<b>%{x}</b><br>Perempuan: %{y:,}<extra></extra>",
        ))
        fig_st.update_layout(**base_layout(
            barmode="group", height=290,
            margin=dict(l=4,r=4,t=10,b=55),
            xaxis=dict(showgrid=False,zeroline=False,
                       tickfont=dict(color=C["muted"],size=10),tickangle=-20),
            yaxis=dict(**subtle_grid_y(), range=[0, df_st["Laki_Laki"].max()*1.25]),
            bargap=0.22, bargroupgap=0.08,
        ))
        st.plotly_chart(fig_st, use_container_width=True, config=PCFG)

    insight(
        f"<strong>74% tenaga kerja terserap di sektor Jasa</strong> — menempatkan Bandung sejajar dengan "
        f"kota-kota jasa berkembang di Asia Tenggara. Status pekerjaan terbesar adalah "
        f"<strong>Karyawan/Buruh (662 ribu jiwa)</strong>, segmen ini adalah konsumen utama produk cicilan, "
        f"asuransi, dan platform digital. Perempuan mendominasi kategori 'Pekerja Keluarga Tak Dibayar' — "
        f"mencerminkan potensi program pemberdayaan ekonomi perempuan yang belum digarap optimal.",
        "sky"
    )


# ╔════════════════════════════════════════════════════════╗
# ║  TAB 2 — BISNIS & MOBILITAS                          ║
# ╚════════════════════════════════════════════════════════╝
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI mini row ─────────────────────────────────────
    total_kend_all = df_kend["Total"].sum()
    rasio_res = round(total_penduduk / total_restoran)
    b1,b2,b3,b4 = st.columns(4, gap="small")
    kpi(b1,"🍜","Total Rumah Makan", f"{total_restoran:,}",
        "unit aktif di seluruh Kota Bandung 2025", C["amber"])
    kpi(b2,"👥","1 Restoran Melayani", f"{rasio_res:,} Jiwa",
        "rata-rata cakupan populasi per unit F&B", C["sky"])
    kpi(b3,"🏍","Sepeda Motor Pribadi", f"{motor_pribadi/1e6:.2f} Juta",
        f"dari {motor_total:,} motor · dominasi armada kota", C["teal"])
    kpi(b4,"🚗","Total Kendaraan", f"{total_kend_all/1e6:.2f} Juta",
        "semua jenis & status · terdaftar 2025", C["violet"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Komposisi Armada Kendaraan (Kota) ────────────────
    section("Komposisi Armada Kendaraan Kota Bandung",
            "Distribusi total unit berdasarkan jenis kendaraan — sepeda motor mendominasi lebih dari 70%")

    # Aggregate by vehicle type
    kend_by_type = df_kend.groupby("Jenis_Kendaraan")["Total"].sum().reset_index()
    kend_by_type = kend_by_type.sort_values("Total", ascending=False)
    type_colors  = [C["amber"], C["sky"], C["teal"], C["violet"]]

    col_donut2, col_stat2 = st.columns([1, 1.3], gap="large")

    with col_donut2:
        fig_ktype = go.Figure(go.Pie(
            labels=kend_by_type["Jenis_Kendaraan"].tolist(),
            values=kend_by_type["Total"].tolist(),
            hole=0.58,
            marker=dict(colors=type_colors,
                        line=dict(color=C["surface"], width=3)),
            textinfo="label+percent",
            textfont=dict(size=11, color=C["text"]),
            hovertemplate="<b>%{label}</b><br>%{value:,} unit (%{percent})<extra></extra>",
            pull=[0.05, 0, 0, 0],
        ))
        fig_ktype.add_annotation(
            text=f"<b>{total_kend_all/1e6:.2f}Jt</b><br><span style='font-size:10px'>Total Unit</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=C["text"], family="Sora"),
        )
        fig_ktype.update_layout(**base_layout(
            height=300, margin=dict(l=0,r=0,t=10,b=40),
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center",
                        font=dict(color=C["muted"],size=10)),
        ))
        st.plotly_chart(fig_ktype, use_container_width=True, config=PCFG)

    with col_stat2:
        # Grouped bar: Pribadi vs Dinas vs Umum per jenis kendaraan
        status_order  = ["Pribadi", "Dinas", "Umum"]
        status_colors = [C["sky"], C["teal"], C["violet"]]

        fig_kstat = go.Figure()
        for st_name, st_color in zip(status_order, status_colors):
            df_s = df_kend[df_kend["Status"] == st_name]
            if df_s.empty:
                continue
            fig_kstat.add_trace(go.Bar(
                name=st_name,
                x=df_s["Jenis_Kendaraan"],
                y=df_s["Total"],
                marker=dict(color=st_color, opacity=0.85),
                text=[f"{v:,}" for v in df_s["Total"]],
                textposition="outside",
                textfont=dict(size=9, color=C["muted"]),
                hovertemplate=f"<b>%{{x}}</b><br>{st_name}: %{{y:,}} unit<extra></extra>",
            ))
        fig_kstat.update_layout(**base_layout(
            barmode="group", height=300,
            margin=dict(l=4,r=4,t=10,b=65),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(color=C["muted"],size=9), tickangle=-15),
            yaxis=dict(showgrid=True, gridcolor="rgba(42,45,62,0.6)",
                       zeroline=False, tickfont=dict(color=C["muted"],size=10)),
            bargap=0.22, bargroupgap=0.08,
        ))
        st.plotly_chart(fig_kstat, use_container_width=True, config=PCFG)

    insight(
        f"Sepeda motor mendominasi dengan <strong>{motor_total:,} unit ({motor_total/total_kend_all*100:.0f}%)</strong> "
        f"dari total armada — hampir semuanya kepemilikan pribadi. Ini bukan sekadar data transportasi: "
        f"Bandung adalah <strong>kota motor</strong>. Setiap keputusan desain bisnis — dari lebar parkir, "
        f"lebar pintu masuk, hingga radius delivery — harus bertolak dari fakta ini. "
        f"Sedan/mobil penumpang terbagi rata antara pribadi, dinas, dan umum, "
        f"mencerminkan kelas menengah yang mulai bertransisi ke empat roda.",
        "amber"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Kendaraan ────────────────────────────────────────
    section("Kepemilikan Kendaraan Bermotor",
            "Komposisi kendaraan berdasarkan jenis dan status kepemilikan, 2025")

    kend_plot = df_kend.copy()
    kend_plot["Label"] = kend_plot["Jenis_Kendaraan"] + "  ·  " + kend_plot["Status"]
    sc = {"Pribadi": C["sky"], "Dinas": C["teal"], "Umum": C["violet"]}
    kend_plot["Color"] = kend_plot["Status"].map(sc).fillna(C["muted"])
    kend_s = kend_plot.sort_values("Total", ascending=True)

    fig_knd = go.Figure(go.Bar(
        x=kend_s["Total"], y=kend_s["Label"],
        orientation="h",
        marker=dict(color=kend_s["Color"].tolist(), opacity=0.82,
                    line=dict(color="rgba(0,0,0,0)")),
        text=[f"  {v:,}" for v in kend_s["Total"]],
        textposition="outside", textfont=dict(size=11, color=C["text"]),
        hovertemplate="<b>%{y}</b><br>%{x:,} unit<extra></extra>",
        cliponaxis=False,
    ))
    fig_knd.update_layout(**base_layout(
        height=320, margin=dict(l=4,r=120,t=10,b=4),
        xaxis=dict(visible=False),
        yaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color=C["text"],size=11)),
    ))
    st.plotly_chart(fig_knd, use_container_width=True, config=PCFG)

    insight(
        f"Dengan <strong>{motor_pribadi:,} sepeda motor pribadi</strong> — "
        f"{motor_pribadi/df_kend['Total'].sum()*100:.0f}% dari seluruh kendaraan — "
        f"Bandung adalah kota berbasis motor. Implikasinya konkret: "
        f"<strong>drive-thru, parkir motor luas, dan layanan delivery</strong> bukan fitur bonus, "
        f"melainkan keharusan desain bisnis. Brand F&B atau retail yang mengabaikan aksesibilitas motor "
        f"akan kehilangan sebagian besar potensi pelanggannya.",
        "teal"
    )


# ╔════════════════════════════════════════════════════════╗
# ║  TAB 3 — MODAL MANUSIA                               ║
# ╚════════════════════════════════════════════════════════╝
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI mini row ─────────────────────────────────────
    h1,h2,h3,h4 = st.columns(4, gap="small")
    kpi(h1,"🎓","Lulusan PT",    f"{(pt_lk+pt_pr)/2:.1f}%",
        "rata-rata laki-laki & perempuan usia 15+",   C["amber"])
    kpi(h2,"👶","Penduduk Muda", f"{muda/1e6:.2f} Jt",
        "usia 0–14 tahun · calon konsumen masa depan", C["sky"])
    kpi(h3,"👷","Usia Produktif", f"{produktif/1e6:.2f} Jt",
        "usia 15–64 · menanggung {:.0f}% populasi".format((muda+tua)/total_penduduk*100), C["teal"])
    kpi(h4,"👴","Dependency Ratio", f"{dep_ratio}",
        "setiap 100 pekerja menanggung ini orang",    C["violet"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Piramida ─────────────────────────────────────────
    section("Piramida Penduduk Kota Bandung 2025",
            "Distribusi usia dan jenis kelamin — lebar tiap batang menunjukkan jumlah jiwa (ribuan)")

    kel  = df_umur["Kelompok_Umur"].tolist()
    laki = df_umur["Laki_Laki"].tolist()
    puan = df_umur["Perempuan"].tolist()
    max_v = max(max(laki), max(puan)) * 1.18

    fig_pyr = go.Figure()

    # Shade productive band
    fig_pyr.add_shape(
        type="rect", layer="below",
        x0=-max_v, x1=max_v, y0=2.5, y1=12.5,
        fillcolor="rgba(45,212,191,0.05)",
        line=dict(color="rgba(45,212,191,0.2)", width=1, dash="dot"),
    )
    fig_pyr.add_annotation(
        x=max_v*0.75, y=12.6, text="Usia Produktif  15–64 →",
        showarrow=False, font=dict(size=9, color=C["teal"]), xanchor="right",
    )

    fig_pyr.add_trace(go.Bar(
        y=kel, x=[-v for v in laki],
        name="Laki-Laki", orientation="h",
        marker=dict(color=C["sky"], opacity=0.8, line=dict(color="rgba(0,0,0,0)")),
        customdata=laki,
        text=[f"{int(v/1000)}k" for v in laki],
        textposition="inside", textfont=dict(size=9, color="#0E1117"),
        hovertemplate="<b>Usia %{y}</b><br>Laki-Laki: %{customdata:,} jiwa<extra></extra>",
    ))
    fig_pyr.add_trace(go.Bar(
        y=kel, x=puan,
        name="Perempuan", orientation="h",
        marker=dict(color=C["rose"], opacity=0.8, line=dict(color="rgba(0,0,0,0)")),
        text=[f"{int(v/1000)}k" for v in puan],
        textposition="inside", textfont=dict(size=9, color="#0E1117"),
        hovertemplate="<b>Usia %{y}</b><br>Perempuan: %{x:,} jiwa<extra></extra>",
    ))

    ticks   = [int(v) for v in np.linspace(-max_v*0.9, max_v*0.9, 5)]
    tlabels = [f"{abs(v)//1000:.0f}k" for v in ticks]

    fig_pyr.update_layout(**base_layout(
        barmode="overlay", height=500,
        margin=dict(l=4,r=4,t=30,b=10),
        xaxis=dict(range=[-max_v, max_v],
                   tickvals=ticks, ticktext=tlabels,
                   showgrid=True, gridcolor="rgba(42,45,62,0.53)",
                   zeroline=True, zerolinecolor=C["border"],
                   tickfont=dict(color=C["muted"],size=10)),
        yaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color=C["text"],size=11)),
        bargap=0.1,
        annotations=[
            dict(x=-max_v*0.55, y=len(kel)-0.4, text="← Laki-Laki",
                 showarrow=False, font=dict(size=11, color=C["sky"])),
            dict(x=max_v*0.55,  y=len(kel)-0.4, text="Perempuan →",
                 showarrow=False, font=dict(size=11, color=C["rose"])),
        ],
    ))
    st.plotly_chart(fig_pyr, use_container_width=True, config=PCFG)

    insight(
        f"Piramida menunjukkan <strong>bonus demografi aktif</strong>: puncak populasi ada di usia "
        f"20–29 tahun — kelompok yang paling produktif sekaligus paling konsumtif. "
        f"Dengan dependency ratio <strong>{dep_ratio}</strong> (tergolong rendah), beban ekonomi "
        f"per pekerja masih ringan, artinya daya beli rumah tangga relatif lebih baik. "
        f"Ini jendela waktu yang terbatas — investor dan pelaku bisnis memiliki 10–15 tahun ke depan "
        f"untuk memanfaatkan pasar urban muda Bandung sebelum piramida mulai menua.",
        "teal"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Ijazah + Kepadatan ────────────────────────────────
    col_edu, col_kep = st.columns([1, 1], gap="large")

    with col_edu:
        section("Capaian Pendidikan per Gender",
                "% penduduk 15+ berdasarkan ijazah tertinggi yang dimiliki")

        fig_edu = go.Figure()
        fig_edu.add_trace(go.Bar(
            name="Laki-Laki", x=df_ijazah["Ijazah"], y=df_ijazah["Laki_Laki"],
            marker=dict(color=C["sky"], opacity=0.82),
            text=[f"{v:.1f}%" for v in df_ijazah["Laki_Laki"]],
            textposition="outside", textfont=dict(size=11, color=C["text"]),
            hovertemplate="<b>%{x}</b><br>Laki-Laki: %{y:.1f}%<extra></extra>",
        ))
        fig_edu.add_trace(go.Bar(
            name="Perempuan", x=df_ijazah["Ijazah"], y=df_ijazah["Perempuan"],
            marker=dict(color=C["rose"], opacity=0.82),
            text=[f"{v:.1f}%" for v in df_ijazah["Perempuan"]],
            textposition="outside", textfont=dict(size=11, color=C["text"]),
            hovertemplate="<b>%{x}</b><br>Perempuan: %{y:.1f}%<extra></extra>",
        ))
        fig_edu.update_layout(**base_layout(
            barmode="group", height=310,
            margin=dict(l=4,r=4,t=10,b=55),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(color=C["muted"],size=10), tickangle=-15),
            yaxis=dict(**subtle_grid_y(), range=[0, 55]),
            bargap=0.25, bargroupgap=0.1,
        ))
        st.plotly_chart(fig_edu, use_container_width=True, config=PCFG)

        insight(
            f"Lulusan SMA/SMK mendominasi (~43%) — ini pasar terbesar untuk pelatihan vokasi "
            f"dan upskilling digital. Lulusan Perguruan Tinggi hampir seimbang antara pria "
            f"(<strong>{pt_lk:.1f}%</strong>) dan wanita (<strong>{pt_pr:.1f}%</strong>), "
            f"menandakan kelas menengah terdidik yang homogen dan terbuka pada produk premium, "
            f"investasi, serta gaya hidup berbasis nilai.",
            "amber"
        )

    with col_kep:
        section("Komposisi Usia Kota Bandung",
                "Tiga kelompok besar: anak-anak, usia produktif, dan lansia")

        # City-level age composition
        cat_labels = ["Anak-anak\n(0–14)", "Usia Produktif\n(15–64)", "Lansia\n(65+)"]
        cat_values = [muda, produktif, tua]
        cat_colors = [C["sky"], C["teal"], C["violet"]]
        cat_pcts   = [v / total_penduduk * 100 for v in cat_values]

        fig_age = go.Figure(go.Pie(
            labels=cat_labels,
            values=cat_values,
            hole=0.58,
            marker=dict(colors=cat_colors,
                        line=dict(color=C["surface"], width=3)),
            textinfo="label+percent",
            textfont=dict(size=11, color=C["text"]),
            hovertemplate="<b>%{label}</b><br>%{value:,} jiwa (%{percent})<extra></extra>",
            pull=[0, 0.05, 0],
            direction="clockwise",
            rotation=160,
        ))
        fig_age.add_annotation(
            text=f"<b>{total_penduduk/1e6:.2f}Jt</b><br><span style='font-size:10px'>Total Jiwa</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=C["text"], family="Sora"),
        )
        fig_age.update_layout(**base_layout(
            height=310, margin=dict(l=0,r=0,t=10,b=40),
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center",
                        font=dict(color=C["muted"],size=10)),
        ))
        st.plotly_chart(fig_age, use_container_width=True, config=PCFG)

        insight(
            f"<strong>{cat_pcts[1]:.1f}% penduduk Bandung berada di usia produktif</strong> "
            f"({produktif/1e6:.2f} juta jiwa) — proporsi yang sangat menguntungkan. "
            f"Hanya <strong>{cat_pcts[2]:.1f}% lansia</strong> yang perlu ditopang, "
            f"jauh di bawah rata-rata kota-kota di Eropa dan Jepang yang sudah di atas 20%. "
            f"Ini artinya daya beli kolektif kota masih sangat kuat dan akan bertahan "
            f"setidaknya satu dekade ke depan.",
            "rose"
        )


# ══════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:3rem;padding-top:1.2rem;
     border-top:1px solid {C['border']};
     text-align:center;color:{C['muted']};font-size:.75rem;
     font-family:'Nunito',sans-serif;">
  Bandung City Intelligence Dashboard &nbsp;·&nbsp;
  Sumber: BPS Kota Bandung 2025 &nbsp;·&nbsp;
  Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
