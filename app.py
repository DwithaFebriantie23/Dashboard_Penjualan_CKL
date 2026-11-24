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


if not FILE_EXCEL.exists():
  st.error("File Penjualan2025.xlsx tidak ditemukan di folder yang sama.")
  st.stop()

df = load_data(str(FILE_EXCEL), FILE_EXCEL.stat().st_mtime)

total_penjualan = df["TOTAL"].sum()
total_transaksi = df["ID TRANSAKSI"].nunique()
total_pelanggan = df["CUSTOMER"].nunique()
total_produk = df["ITEM"].nunique()

st.title("📊 Dashboard Penjualan PT CKL")
st.write("Ringkasan penjualan PT Cakrawala Kemasindo Lestari tahun 2025.")
st.divider()

c1, c2 = st.columns(2)
c1.metric(
    "Total Penjualan", "Rp " + f"{total_penjualan:,.0f}".replace(",", ".")
)
c2.metric("Jumlah Transaksi", f"{total_transaksi:,.0f}".replace(",", "."))

c3, c4 = st.columns(2)
c3.metric("Jumlah Pelanggan", f"{total_pelanggan:,.0f}".replace(",", "."))
c4.metric("Jenis Produk", f"{total_produk:,.0f}".replace(",", "."))