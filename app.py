from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Dashboard Penjualan PT CKL",
    page_icon="📊",
    layout="wide",
)

BASE_DIR = Path(__file__).parent
FILE_EXCEL = BASE_DIR / "Penjualan2025.xlsx"


@st.cache_data
def load_data(file_path, file_mtime):
  df = pd.read_excel(file_path, sheet_name="Rekap 2025", header=1)

  for kolom in ["QTY", "HARGA", "TOTAL"]:
    if kolom in df.columns:
      df[kolom] = pd.to_numeric(df[kolom], errors="coerce")

  # Sesuai Colab: keluarkan baris TOTAL == 0
  df = df[df["TOTAL"] != 0].copy()

  df["CUSTOMER"] = (
      df["CUSTOMER"].fillna("Tidak Diketahui").astype(str).str.strip()
  )
  df["TANGGAL"] = pd.to_datetime(df["TANGGAL"], errors="coerce")
  df["BULAN"] = df["TANGGAL"].dt.to_period("M").astype(str)
  df.loc[df["TANGGAL"].isna(), "BULAN"] = None

  return df


def rupiah(nilai):
  nilai = 0 if pd.isna(nilai) else nilai
  return "Rp " + f"{nilai:,.0f}".replace(",", ".")


def angka(nilai):
  nilai = 0 if pd.isna(nilai) else nilai
  return f"{nilai:,.0f}".replace(",", ".")


if not FILE_EXCEL.exists():
  st.error("File Penjualan2025.xlsx tidak ditemukan di folder yang sama.")
  st.stop()

df = load_data(str(FILE_EXCEL), FILE_EXCEL.stat().st_mtime)

total_penjualan = df["TOTAL"].sum()
total_transaksi = df["ID TRANSAKSI"].nunique()
total_pelanggan = df["CUSTOMER"].nunique()
total_produk = df["ITEM"].nunique()

# Sidebar Navigasi
st.sidebar.title("📊 Dashboard PT CKL")
menu = st.sidebar.radio(
    "Menu Navigasi",
    ["🏠 Beranda", "📈 Analisis Penjualan", "🔍 Hasil Apriori"],
)
st.sidebar.divider()
st.sidebar.caption("Sistem Informasi | Data Science")
st.sidebar.caption("PT Cakrawala Kemasindo Lestari")

# 1. HALAMAN BERANDA
if menu == "🏠 Beranda":
  st.title("📊 Dashboard Penjualan PT CKL")
  st.write(
      "Ringkasan informasi penjualan PT Cakrawala Kemasindo Lestari tahun"
      " 2025."
  )
  st.divider()

  c1, c2 = st.columns(2)
  c1.metric("Total Penjualan", rupiah(total_penjualan))
  c2.metric("Jumlah Transaksi", angka(total_transaksi))

  c3, c4 = st.columns(2)
  c3.metric("Jumlah Pelanggan", angka(total_pelanggan))
  c4.metric("Jenis Produk", angka(total_produk))

# 2. HALAMAN ANALISIS PENJUALAN
elif menu == "📈 Analisis Penjualan":
  st.title("📈 Analisis Penjualan")
  st.write("Ringkasan data penjualan dan produk terlaris.")
  st.divider()

  produk_terlaris = (
      df.groupby("ITEM")["QTY"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
  )

  if not produk_terlaris.empty:
    st.subheader("10 Produk dengan QTY Tertinggi")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(
        produk_terlaris["ITEM"].iloc[::-1], produk_terlaris["QTY"].iloc[::-1]
    )
    ax.set_xlabel("Total QTY")
    ax.set_ylabel("UK Produk")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

  st.subheader("Tabel Data Penjualan")
  st.dataframe(df, use_container_width=True, hide_index=True)

# 3. HALAMAN HASIL APRIORI
elif menu == "🔍 Hasil Apriori":
  st.title("🔍 Hasil Penelitian Apriori")
  st.info(
      "Halaman hasil Apriori sudah siap. Nanti bisa kita isi sesuai parameter"
      " dan aturan asosiasi dari Colab."
  )
