import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

yf.user_cache_dir = lambda *args: "/tmp"

def main():

    # Streamlit başlık ve açıklama
    st.title("Finansal Veri Analiz ve Görselleştirme Aracı")

    # Kullanıcıdan giriş alma (ticker, tarih aralığı)
    st.sidebar.header("Parametreler")
    ticker = st.sidebar.text_input("Hisse Kodu:", placeholder="(Örn: AAPL, TSLA, BTC-USD)")
    start_date = st.sidebar.date_input("Başlangıç Tarihi")
    end_date = st.sidebar.date_input("Bitiş Tarihi")

    # Veri Çekme
    try:
        if st.sidebar.button("Verileri Getir"):

            if ticker == "":
                st.error("Lütfen hisse kodunu girin.")

            if start_date == end_date:
                st.error("Tarih aralığını genişletin.")

            # Veri Çek
            st.write(f"### {ticker} Hisse Senedi Verileri")
            data = yf.download(ticker, start=start_date, end=end_date)
            
            if data.empty:
                st.error("Veri bulunamadı. Lütfen tarih aralığını ve hisse kodunu kontrol edin.")
            else:
                # Ham Veriyi Göster
                st.success(f"{ticker} için veriler başarıyla çekildi.")
                st.write("#### Ham Veri")
                st.dataframe(data)
                
                # Hareketli Ortalama Hesaplama
                data['SMA_20'] = data['Close'].rolling(window=20).mean()
                data['SMA_50'] = data['Close'].rolling(window=50).mean()

                # Grafik: Hareketli Ortalama
                st.write("#### Fiyat ve Hareketli Ortalamalar")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(data['Close'], label='Kapanış Fiyatı', color='blue')
                ax.plot(data['SMA_20'], label='20 Günlük SMA', color='orange')
                ax.plot(data['SMA_50'], label='50 Günlük SMA', color='green')
                ax.set_title(f"{ticker} Hisse Senedi Analizi")
                ax.set_xlabel("Tarih")
                ax.set_ylabel("Fiyat")
                ax.legend()
                st.pyplot(fig)

                # Veriyi indirme seçeneği
                st.write("#### Veriyi İndir")
                csv_data = data.to_csv(sep=';', index=True).encode('utf-8')
                st.download_button(
                    label="Veriyi CSV Olarak İndir",
                    data=csv_data,
                    file_name=f"{ticker}_data.csv",
                    mime="text/csv",
                )

    except ValueError:
        pass

if __name__ == "__main__":
    main()



