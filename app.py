import streamlit as st
import requests
import base64
import os
from datetime import datetime, timedelta

# Konfigurasi Halaman
st.set_page_config(
    page_title="SAHABAT NESTAND - Kotak Lapor Rahasia",
    page_icon="🛡️",
    layout="centered"
)

# Fungsi membaca gambar lokal menjadi Base64 agar bisa jadi background & logo
def get_image_base64(keywords):
    for filename in os.listdir("."):
        lower_name = filename.lower()
        if any(k in lower_name for k in keywords) and lower_name.endswith((".jpg", ".jpeg", ".png")):
            with open(filename, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

bg_base64 = get_image_base64(["wallpaper", "bg", "latar"])
logo_base64 = get_image_base64(["logo"])

# Gaya Tampilan (CSS) dengan Wallpaper Sekolah Bening Tanpa Overlay Gelap
if bg_base64:
    bg_css = f"""
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """
else:
    bg_css = """
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%);
    }
    """

st.markdown(f"""
<style>
    {bg_css}

    [data-testid="stHeader"] {{
        background: rgba(0, 0, 0, 0);
    }}

    /* Tulisan Share & ikon pojok kanan atas jadi gelap tegas + kapsul tipis */
    [data-testid="stToolbar"] {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(4px);
        padding: 4px 10px;
        border-radius: 20px;
        margin-top: 6px;
        margin-right: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }}
    [data-testid="stToolbar"] button,
    [data-testid="stToolbar"] span,
    [data-testid="stToolbar"] svg {{
        color: #0d2850 !important;
        fill: #0d2850 !important;
        font-weight: 700 !important;
    }}

    /* Kartu Header Atas */
    .header-box {{
        text-align: center;
        max-width: 560px;
        margin: 0 auto 12px auto;
        padding: 14px 18px 18px 18px;
        color: #ffffff;
        background: rgba(13, 40, 80, 0.38);
        border-radius: 16px;
        backdrop-filter: blur(2px);
    }}
    .header-box img {{
        width: 105px;
        height: auto;
        margin: 0 auto 10px auto;
        display: block;
        border-radius: 14px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        background: rgba(255, 255, 255, 0.95);
        padding: 6px;
    }}
    .header-title {{
        display: block;
        width: 100%;
        text-align: center !important;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0 auto !important;
        padding: 0 !important;
        color: #ffffff;
        text-shadow: 0 2px 12px rgba(0, 0, 0, 0.75);
    }}
    .header-sub {{
        display: block;
        width: 100%;
        text-align: center !important;
        font-size: 0.96rem;
        color: #ffffff;
        margin: 6px auto 0 auto !important;
        padding: 0 !important;
        font-weight: 600;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.75);
    }}
    .badge-aman {{
        display: inline-block;
        background: rgba(13, 71, 161, 0.92);
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #ffffff;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.82rem;
        margin-top: 10px;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
    }}

    /* Kartu Formulir Elegan & Cukupannya Pas */
    [data-testid="stForm"] {{
        max-width: 560px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.94);
        padding: 20px 22px;
        border-radius: 16px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
        border: 1px solid rgba(255, 255, 255, 0.75);
    }}

    /* Pastikan tulisan label di dalam formulir selalu gelap & jelas terbaca */
    [data-testid="stForm"] label,
    [data-testid="stForm"] p,
    [data-testid="stForm"] h3 {{
        color: #1a237e !important;
        font-weight: 600;
        font-size: 0.92rem;
    }}
    [data-testid="stForm"] h3 {{
        font-size: 1.15rem !important;
        margin-bottom: 12px !important;
        text-align: center !important;
    }}

    /* Tombol Kirim */
    div.stFormSubmitButton > button {{
        background: linear-gradient(90deg, #0d47a1, #1976d2);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.92rem;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        width: 100%;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.35);
        transition: all 0.2s ease;
    }}
    div.stFormSubmitButton > button * {{
        color: #ffffff !important;
        text-align: center !important;
    }}
    div.stFormSubmitButton > button:hover {{
        background: linear-gradient(90deg, #1565c0, #1e88e5);
        transform: translateY(-1px);
    }}

    .footer-note {{
        text-align: center;
        color: #ffffff;
        font-size: 0.8rem;
        margin-top: 12px;
        padding: 6px 14px;
        display: inline-block;
        background: rgba(13, 40, 80, 0.45);
        border-radius: 10px;
        text-shadow: 0 1px 6px rgba(0, 0, 0, 0.8);
    }}
    .footer-wrap {{
        text-align: center;
        margin-top: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# Tampilan Header + Logo Sekolah
logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Logo SMPN 1 Tanjungmedar">' if logo_base64 else '<div style="font-size:3rem;">🛡️</div>'

st.markdown(f"""
<div class="header-box">
    {logo_html}
    <div class="header-title">SOBAT NESTAND</div>
    <div class="header-sub">Kotak Lapor Rahasia & Peduli Keamanan Sekolah<br><b>SMPN 1 Tanjungmedar</b></div>
    <div class="badge-aman">🔒 Identitas Pelapor 100% Dirahasiakan</div>
</div>
""", unsafe_allow_html=True)

# Formulir Laporan
with st.form("form_laporan", clear_on_submit=True):
    st.markdown("### 📝 Formulir Pengaduan / Curhat Aman")

    kategori = st.selectbox(
        "Kategori Kejadian",
        [
            "Perundungan / Bullying",
            "Kekerasan / Ancaman / Pemalakan",
            "Kenakalan / Bahaya di Lingkungan Sekolah",
            "Curhat / Konseling Pribadi (BK)",
            "Saran & Masukan Keamanan Sekolah",
            "Lainnya"
        ]
    )

    urgensi = st.radio(
        "Tingkat Urgensi",
        ["🟢 Normal", "🟡 Penting (Perlu Segera Dicek)", "🔴 Darurat (Butuh Penanganan Cepat)"],
        horizontal=True
    )

    lokasi = st.text_input(
        "Lokasi Kejadian (Opsional)",
        placeholder="Contoh: Lapangan, belakang kelas 8B, kantin, grup WA..."
    )

    detail = st.text_area(
        "Ceritakan Detail Informasi / Kronologi *",
        height=110,
        placeholder="Tuliskan apa yang terjadi dengan jelas. Kamu aman bercerita di sini..."
    )

    identitas = st.text_input(
        "Nama / Kelas Pelapor (Boleh Dikosongkan agar 100% Anonim)",
        placeholder="Kosongkan jika ingin tetap rahasia"
    )

    submit = st.form_submit_button("📨 KIRIM/SUBMIT LAPORAN RAHASIA SEKARANG")

# Proses Kirim ke Telegram
if submit:
    if not detail.strip():
        st.warning("⚠️ Mohon tuliskan detail informasi/kejadian terlebih dahulu sebelum mengirim.")
    else:
        try:
            token = st.secrets["TELEGRAM_TOKEN"]
            chat_id = st.secrets["TELEGRAM_CHAT_ID"]

            waktu_wib = (datetime.utcnow() + timedelta(hours=7)).strftime("%d-%m-%Y %H:%M WIB")
            pelapor_txt = identitas.strip() if identitas.strip() else "Anonim (Dirahasiakan)"
            lokasi_txt = lokasi.strip() if lokasi.strip() else "Tidak disebutkan"

            pesan = (
                f"🛡️ *LAPORAN BARU - SOBAT NESTAND*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🕒 *Waktu:* {waktu_wib}\n"
                f"📂 *Kategori:* {kategori}\n"
                f"🚨 *Urgensi:* {urgensi}\n"
                f"📍 *Lokasi:* {lokasi_txt}\n"
                f"👤 *Pelapor:* {pelapor_txt}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📝 *Detail Informasi:*\n{detail.strip()}"
            )

            url_api = f"https://api.telegram.org/bot{token}/sendMessage"
            resp = requests.post(
                url_api,
                data={"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"},
                timeout=15
            )

            if resp.status_code == 200:
                st.balloons()
                st.success("✅ Laporan berhasil terkirim dengan aman! Terima kasih sudah berani peduli.")
            else:
                st.error(f"❌ Gagal mengirim laporan (Kode: {resp.status_code}). Coba lagi beberapa saat.")
        except Exception as e:
            st.error(f"❌ Terjadi kendala sistem saat mengirim laporan: {e}")

st.markdown("""
<div class="footer-wrap">
    <div class="footer-note">
        © Wei_ch Sobat Nestand • SMPN 1 Tanjungmedar • Ruang Aman untuk Semua Murid<br>
        Copyright : @wei_ch
    </div>
</div>
""", unsafe_allow_html=True)
