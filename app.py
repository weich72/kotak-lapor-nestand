import streamlit as st
import requests
from datetime import datetime, timezone, timedelta

# Pengaturan Halaman
st.set_page_config(
    page_title="Kotak Lapor Rahasia - Sahabat Nestand",
    page_icon="🛡️",
    layout="centered"
)

# Desain Tampilan Ramah HP & Tombol Besar
st.markdown("""
    <style>
    .main {background-color: #f4f7f6;}
    .stButton>button {
        width: 100%;
        height: 3.5em;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        background-color: #1e88e5;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565c0;
        color: white;
    }
    .banner-box {
        background: linear-gradient(135deg, #0d47a1, #1976d2);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Aplikasi
st.markdown("""
    <div class="banner-box">
        <h2>🛡️ SAHABAT NESTAND</h2>
        <p style="margin:0; font-size:15px;">Kotak Lapor Rahasia & Peduli Keamanan Sekolah<br><b>SMPN 1 Tanjungmedar</b></p>
    </div>
""", unsafe_allow_html=True)

st.info("🔒 **Identitasmu 100% Rahasia.** Aplikasi ini tidak mencatat nama, nomor HP, atau akunmu. Laporan langsung diterima oleh Guru Pembina/BK untuk menjaga keselamatan kita bersama.")

# Fungsi Kirim ke Telegram
def kirim_telegram(pesan):
    try:
        token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": pesan,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        return False

# Formulir Laporan
with st.form("form_lapor", clear_on_submit=True):
    st.subheader("1. Pilih Jenis Kejadian / Bahaya")
    kategori = st.selectbox(
        "Apa yang ingin kamu laporkan?",
        [
            "🚨 Rencana Tawuran / Bentrokan Pelajar",
            "🔪 Info Siswa Membawa Senjata Tajam (Sajam)",
            "📱 Provokasi Geng / Ajakan Tawuran di Medsos",
            "😢 Perundungan (Bullying) / Pemalakan / Ancaman",
            "🚬 Penyalahgunaan Rokok / Miras / Obat Terlarang",
            "💡 Saran & Curhat Keamanan Sekolah Lainnya"
        ]
    )

    st.subheader("2. Tingkat Mendesak")
    urgensi = st.radio(
        "Seberapa mendesak kejadian ini?",
        ["🟢 Info Awal / Pencegahan", "🟡 Perlu Segera Dicek", "🔴 DARURAT (Sedang / Akan Terjadi Hari Ini!)"],
        horizontal=False
    )

    st.subheader("3. Ceritakan Singkat & Jelas")
    lokasi = st.text_input(
        "Lokasi / Tempat Kejadian (Opsional)",
        placeholder="Contoh: Dekat pertigaan kebun, gerbang belakang, atau grup WA/IG..."
    )

    detail = st.text_area(
        "Detail Informasi (Wajib diisi)",
        height=130,
        placeholder="Ceritakan apa yang kamu ketahui (waktu kejadian, ciri-ciri, nama akun medsos provokator, atau kronologi singkat)..."
    )

    identitas = st.text_input(
        "Nama / Kelas (Boleh dikosongkan agar tetap Anonim)",
        placeholder="Kosongkan saja jika ingin 100% rahasia..."
    )

    kirim = st.form_submit_button("📨 KIRIM LAPORAN RAHASIA SEKARANG")

    if kirim:
        if not detail.strip():
            st.warning("⚠️ Mohon isi bagian **Detail Informasi** terlebih dahulu agar Bapak/Ibu Guru bisa menindaklanjuti.")
        else:
            # Waktu WIB (UTC+7)
            wib = timezone(timedelta(hours=7))
            waktu_sekarang = datetime.now(wib).strftime("%d-%m-%Y %H:%M WIB")
            pengirim = identitas.strip() if identitas.strip() else "Anonim (Dirahasiakan)"
            lokasi_info = lokasi.strip() if lokasi.strip() else "Tidak disebutkan"

            pesan_tg = (
                f"🛡️ <b>LAPORAN BARU - SAHABAT NESTAND</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🕒 <b>Waktu:</b> {waktu_sekarang}\n"
                f"📌 <b>Kategori:</b> {kategori}\n"
                f"⚠️ <b>Status:</b> {urgensi}\n"
                f"📍 <b>Lokasi:</b> {lokasi_info}\n"
                f"👤 <b>Pelapor:</b> {pengirim}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📝 <b>Isi Laporan:</b>\n{detail.strip()}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<i>Segera tindak lanjuti secara bijak & rahasia.</i>"
            )

            with st.spinner("Mengirim laporan rahasia ke Guru Pembina..."):
                sukses = kirim_telegram(pesan_tg)

            if sukses:
                st.success("✅ **Laporan berhasil terkirim dengan aman!** Terima kasih sudah berani peduli menjaga keselamatan teman-teman dan sekolah kita.")
                st.balloons()
            else:
                st.error("❌ Gagal mengirim laporan. Pastikan koneksi internet aktif atau hubungi admin sekolah.")

st.caption("© 2026 Sahabat Nestand - SMPN 1 Tanjungmedar | Sistem Pencegahan Dini & Perlindungan Siswa")
