import streamlit as st
import requests
import base64
import os
from datetime import datetime, timedelta

# Konfigurasi Halaman
st.set_page_config(
    page_title="SOBAT NESTAND - Kotak Lapor Rahasia",
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

# Gaya Tampilan (CSS) dengan Wallpaper Sekolah + Efek Kaca Elegan
bg_css = ""
if bg_base64:
    bg_css = f"""
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(10, 25, 50, 0.72), rgba(10, 25, 50, 0.78)),
                          url("data:image/jpeg;base64,{bg_base64}");
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

    /* Kartu Header Atas */
    .header-box {{
        text-align: center;
        padding: 10px 15px 20px 15px;
        color: #ffffff;
    }}
    .header-box img {{
        width: 110px;
        height: auto;
        margin-bottom: 12px;
        border-radius: 14px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        background: rgba(255, 255, 255, 0.92);
        padding: 6px;
    }}
    .header-title {{
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.45);
    }}
    .header-sub {{
        font-size: 1rem;
        color: #e3f2fd;
        margin-top: 6px;
        font-weight: 500;
    }}
    .badge-aman {{
        display: inline-block;
        background: rgba(25, 118, 210, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.35);
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        margin-top: 12px;
        font-weight: 600;
    }}

    /* Kartu Formulir Putih Bersih */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.95);
        padding: 28px 26px;
        border-radius: 18px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.6);
    }}

    /* Pastikan tulisan label di dalam formulir selalu gelap & jelas terbaca */
    [data-testid="stForm"] label,
    [data-testid="stForm"] p,
    [data-testid="stForm"] h3 {{
        color: #1a237e !important;
        font-weight: 600;
    }}

    /* Tombol Kirim */
    div.stFormSubmitButton > button {{
        background: linear-gradient(90deg, #0d47a1, #1976d2);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.2rem;
        width: 100%;
        box-shadow: 0 4px 14px rgba(13, 71, 161, 0.4);
        transition: all 0.2s ease;
    }}
    div.stFormSubmitButton > button:hover {{
        background: linear-gradient(90deg, #1565c0, #1e88e5);
        transform: translateY(-1px);
    }}

    .footer-note {{
        text-align: center;
        color: #e3f2fd;
        font-size: 0.82rem;
        margin-top: 18px;
        text-shadow: 0 1px 4px rgba(0,0,0,0.5);
    }}
</style>
""", unsafe_allow_html=True)

# Tampilan Header + Logo Sekolah
logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Logo SMPN 1 Tanjungmedar">' if logo_base64 else '<div style="font-size:3rem;">🛡️</div>'

st.markdown(f"""
<div class="header-box">
    {logo_html}
    <h1 class="header-title">SOBAT NESTAND</h1>
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
        height=140,
        placeholder="Tuliskan apa yang terjadi dengan jelas. Kamu aman bercerita di sini..."
    )

    identitas = st.text_input(
        "Nama / Kelas Pelapor (Boleh Dikosongkan agar 100% Anonim)",
        placeholder="Kosongkan jika ingin tetap rahasia"
    )

    submit = st.form_submit_button("📨 KIRIM/SUBMITE LAPORAN RAHASIA SEKARANG")

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
<div class="footer-note">
    © Sobat Nestand • SMPN 1 Tanjungmedar • Ruang Aman untuk Semua Siswa
</div>
""", unsafe_allow_html=True)
