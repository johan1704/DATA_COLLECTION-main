import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import numpy as np

donnees = pd.read_csv("datas/teldakarvente.csv",dtype={'marque': str, 'prix': str})
donnees['prix'].fillna('N/A', inplace=True)

st.markdown("""
<style>
    .st-emotion-cache-10trblm e1nzilvr1{
        text-color:'red'
    }
</style>            
""",unsafe_allow_html=True)

def scrap(id,nb_page):
    df = pd.DataFrame()
    for p in range(1,nb_page):
        url = f'https://dakarvente.com/index.php?page=annonces_categorie&id={id}&sort=&nb={p}'
        resp = get(url)
        soup = bs(resp.text,'html.parser')
        articles = soup.find_all('article', id = 'div-desktop')
        data=[]
        for article in articles:
            try:
                content_price = article.findAll('div', class_ = 'content-price')
                marque = article.find('div',class_ = 'content-desc').find("a",class_ = "mv-overflow-ellipsis").text

                try:
                    prix = content_price[0].find("span").text.replace(" FCFA","")
                except:
                    pass

                adresse = content_price[1].find("span").text
                img = article.find('div',class_ = '').find("h2").find("a").find("img" ).get('src')

                obj = {
                    "marque":marque,
                    "prix":prix,
                    "adresse":adresse,
                    "img":img
                }
                data.append(obj)
            except:
                pass
    DF = pd.DataFrame(data)
    df = pd.concat([df, DF],axis=0).reset_index(drop = True)
        
    return df

st.sidebar.subheader("Filtrer le scraping")
nb_page = st.sidebar.slider("Choisissez le nombre de page a scraper" , min_value=1,max_value=111)
print(nb_page)
st.sidebar.markdown("---")
res = st.sidebar.selectbox("Naviguez sur l'application",options=("Scrapper les données avec BS","Dashboard","Scrapper les données avec web Scraper","Formulaire de contact"))

if res == "Scrapper les données avec BS":
    st.title("Dashboard de scrapping")
    st.markdown("Ces données sont scrapées sur le site [dakarvente](https://www.dakarvente.com)")
    st.text("Ci-dessous se trouve les données disponible pour le scraping")
    st.markdown("---")
    # st.table(table)
    st.header("Voiture")
    
    st.image("images/mustang.jpg")
    click = st.button("Scrapper les données des voitures en location")

    if click:
        sc = scrap(8,nb_page)
        st.dataframe(sc)

    click = st.button("Scrapper les données des voitures en ventes")

    if click:
        sc = scrap(2,nb_page)
        st.dataframe(sc)


    st.header("Motos")
    st.image("images/moto2.jpg")
    click = st.button("Scrapper les données des motos")

    if click:
        sc = scrap(3,nb_page)
        st.dataframe(sc)

    st.header("Telephone")
    st.image("images/telep.jpg")
    click = st.button("Scrapper les données des telephones")

    if click:
        sc = scrap(32,nb_page)
        st.dataframe(sc)

elif res == "Formulaire de contact":
    st.markdown("""<iframe src="https://ee.kobotoolbox.org/i/cXvfevZE" width="800" height="600"></iframe>""",unsafe_allow_html=True)
elif res == "Dashboard":

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    st.title("Graphique Matplotlib avec Streamlit")

    graph_type = st.selectbox("Choisissez le type de graphique", ["ligne", "Nuage de points","barre","histogramme"])
        
    fig, ax = plt.subplots()

    if graph_type == "Nuage de points":
        plt.scatter(donnees['marque'], donnees['prix'])
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Nuage de points')
        plt.show()
    elif graph_type == "barre":
        plt.bar(donnees['marque'], donnees['prix'])
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Titre du graphique')
        plt.show()
    elif graph_type == "ligne":
        plt.plot(donnees['marque'], donnees['prix'], marker='o')
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Diagramme en lignes')
        plt.show()
    elif graph_type == "histogramme":
        plt.hist(donnees['prix'], bins=10, edgecolor='black')
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Histogramme')
        plt.show()

    st.pyplot(fig)
elif res == "Scrapper les données avec web Scraper":
    st.title("Scraping avec Web Scrapper")
    st.markdown("Ces données sont scrapées sur le site [dakarvente](https://www.dakarvente.com)")
    st.text("Ci-dessous se trouve les données disponible pour le scraping")
    st.markdown("---")
    # st.table(table)
    st.header("Voiture")
    
    st.image("images/mustang.jpg")
    click = st.button("Scrapper les données des voitures en location")

    if click:
        df = pd.read_csv("datas/autolocdakarvente.csv")
        st.dataframe(df)

    click = st.button("Scrapper les données des voitures en ventes")

    if click:
        df = pd.read_csv("datas/autodakarvente.csv")
        st.dataframe(df)


    st.header("Motos")
    st.image("images/moto2.jpg")
    click = st.button("Scrapper les données des motos")

    if click:
        df = pd.read_csv("datas/motodakarvente.csv")
        st.dataframe(df)

    st.header("Telephone")
    st.image("images/telep.jpg")
    click = st.button("Scrapper les données des telephones")

    if click:
        df = pd.read_csv("datas/teldakarvente.csv")
        st.dataframe(df)