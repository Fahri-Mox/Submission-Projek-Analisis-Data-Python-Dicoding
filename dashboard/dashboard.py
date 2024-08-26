import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib
import matplotlib.image as mpimg

# Fungsi untuk memuat dan memproses data
@st.cache_data
def load_data():
    # Ubah path ini sesuai dengan lokasi file Anda
    all_data = pd.read_csv("./data/all_data.csv")
    geo_df = pd.read_csv("./data/geolocation.csv")
    customers_df = pd.read_csv("./data/customers_dataset.csv")

    return all_data, geo_df, customers_df

# Memuat data
all_data, geo_df, customers_df = load_data()

# Sidebar
st.sidebar.title("Dashboard E-Commerce")
selected_analysis = st.sidebar.selectbox("Pilih Analisis", 
                                         ["Produk Paling Banyak & Sedikit Terjual", 
                                          "Tingkat Kepuasan Customer", 
                                          "Distribusi Geografis Customer"])

# Halaman Utama
st.title("Dashboard Analisis E-Commerce")

if selected_analysis == "Produk Paling Banyak & Sedikit Terjual":
    st.subheader("Produk apa yang paling banyak & sedikit terjual?")
    
    sum_order_items_df = all_data.groupby("product_category_name_english")["product_id"].count().reset_index()
    sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
    sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

    colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=18)
    ax[0].tick_params(axis ='y', labelsize=15)

    sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=18)
    ax[1].tick_params(axis='y', labelsize=15)

    plt.suptitle("Produk apa yang paling banyak & sedikit terjual?", fontsize=20)
    st.pyplot(fig)

    # Conclution for Question 1
    st.markdown("""
    **Kesimpulan:**
    Berdasarkan pada grafik di atas, produk yang paling banyak terjual adalah **bed_bath_table** dan produk yang paling sedikit terjual adalah **auto**.
    """)

elif selected_analysis == "Tingkat Kepuasan Customer":
    st.subheader("Bagaimana tingkat kepuasan customer terhadap layanan kami?")
    
    review_scores = all_data['review_score'].value_counts().sort_values(ascending=False)
    most_common_score = review_scores.idxmax()
    
    sns.set(style="darkgrid")

    plt.figure(figsize=(10, 5))
    sns.barplot(x=review_scores.index,
                y=review_scores.values,
                order=review_scores.index,
                palette=["#068DA9" if score == most_common_score else "#D3D3D3" for score in review_scores.index])

    plt.title("Rating by customers for service", fontsize=15)
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.xticks(fontsize=12)
    st.pyplot(plt)

    # Conclution for Question 2
    st.markdown("""
    **Kesimpulan:**
    Berdasarkan grafik di atas, customer sangat puas dengan layanan yang disediakan, terbukti dengan data bahwa customer yang memberikan rating **5** memiliki jumlah terbanyak dibandingkan rating yang lainnya.
    """)

elif selected_analysis == "Distribusi Geografis Customer":
    st.subheader("Dimana letak geografis yang memiliki customer terbanyak?")
    
    other_state_geolocation = geo_df.groupby(['geolocation_zip_code_prefix'])['geolocation_state'].nunique().reset_index(name='count')
    other_state_geolocation[other_state_geolocation['count']>= 2].shape
    max_state = geo_df.groupby(['geolocation_zip_code_prefix','geolocation_state']).size().reset_index(name='count').drop_duplicates(subset = 'geolocation_zip_code_prefix').drop('count',axis=1)

    geolocation_silver = geo_df.groupby(['geolocation_zip_code_prefix','geolocation_city','geolocation_state'])[['geolocation_lat','geolocation_lng']].median().reset_index()
    geolocation_silver = geolocation_silver.merge(max_state,on=['geolocation_zip_code_prefix','geolocation_state'],how='inner')

    customers_silver = customers_df.merge(geolocation_silver,left_on='customer_zip_code_prefix',right_on='geolocation_zip_code_prefix',how='inner')

    def plot_brazil_map(data):
        brazil = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
        ax = data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10,10), alpha=0.3,s=0.3,c='maroon')
        plt.axis('off')
        plt.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4])
        plt.show()
    
    plot_brazil_map(customers_silver.drop_duplicates(subset='customer_unique_id'))
    st.pyplot(plt)

    # Conclution for Question 3
    st.markdown("""
    **Kesimpulan:**
    Berdasarkan grafik di atas, terdapat lebih banyak customer di bagian tenggara dan selatan Brazil.
    """)
