import streamlit as st
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler

DEFAULT_ETHIC_WEEKLY_QUOTA = 1

# Définition de la fonction "ethic_page"
def ethic_page():
    # Configuration du titre de la page
    st.title("Vente de vêtements respectueuse du CO2")
    # Initialisation du panier comme une liste vide
    st.session_state.cart = []
    # Initialisation des prix comme un dictionnaire vide
    st.session_state.prices = {}

    # Chargement des données depuis le fichier CSV
    data = pd.read_csv("ethicdata.csv")

    # Définition d'une fonction pour filtrer les données en fonction du genre
    def filter_data_by_gender(data, gender):
        # Si le genre est "Homme", la variable gender_str sera "homme", sinon "femme"
        gender_str = "homme" if gender == "Homme" else "femme"
        # Filtrage des données en fonction de la présence de la chaîne de caractères correspondant au genre dans la description
        filtered_data = data[data["description"].str.contains(gender_str, case=False)]
        return filtered_data

    # Définition d'une fonction pour effectuer le clustering sur les données
    def perform_clustering(data):
        # Normalisation de l'empreinte carbone pour qu'elle soit comprise entre 0 et 1
        data['carbon_footprint_scaled'] = MinMaxScaler().fit_transform(data[['carbon_footprint']])
        # Application de la méthode de Ward pour le clustering hiérarchique
        Z = linkage(data[['carbon_footprint_scaled']], method='ward')

        # Définition du nombre de clusters
        n_clusters = 3
        # Initialisation de l'algorithme de clustering hiérarchique agglomératif
        hc = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
        # Prédiction des clusters
        data['cluster'] = hc.fit_predict(data[['carbon_footprint_scaled']])

        # Calcul de la moyenne de l'empreinte carbone pour chaque cluster et tri des clusters par cette moyenne
        cluster_means = data.groupby('cluster')['carbon_footprint'].mean().sort_values().index
        # Attribution d'un ordre de pollution à chaque cluster en fonction de la moyenne de l'empreinte carbone
        for i, cluster in enumerate(cluster_means):
            data.loc[data['cluster'] == cluster, 'pollution_order'] = i

        # Retour des données après le clustering
        return data

# La fonction `pollution_level` prend une valeur d'impact en entrée (un nombre réel entre 0 et 1, si nous considérons que l'impact est normalisé)  
    def pollution_level(impact):
        #Si l'impact est inférieur ou égal à 0.33, alors le niveau de pollution est considéré comme "Faible"
        if impact <= 0.33: 
            return "Faible"
        #Si l'impact est inférieur ou égal à 0.66 (mais supérieur à 0.33), alors le niveau de pollution est considéré comme "Modéré"
        elif impact <= 0.66:
            return "Modéré"
        #Sinon (c'est-à-dire si l'impact est supérieur à 0.66), le niveau de pollution est considéré comme "Sévère"
        else:
            return "Sévère"
    
    def display_product_details(selected_product, filtered_data):
        #Récupère les détails du produits sélécionné à partir des données filtrées
        product_details = filtered_data[filtered_data["description"] == selected_product]
        #Récupère le prix du produit à partir de l'état de session Streamlit
        price = st.session_state.prices[selected_product]
        # Affiche la description du produit
        st.write(f"Description : {selected_product}")
        # Affiche l'émission de CO2 du produit
        st.write(f"Émission de CO2 : {product_details['carbon_footprint'].values[0]} kg")
        # Affiche le prix du produit
        st.write(f"Prix : €{price}")
        # Calcule l'impact du produit à partir de son empreinte carbone normalisée
        impact = product_details['carbon_footprint_scaled'].values[0]
        # Affiche le niveau de pollution du produit en appelant la fonction `pollution_level`
        st.write(f"Impact du vêtement : {pollution_level(impact)}")
        # Affiche une barre de progression en fonction de l'impact
        st.progress(impact)
        # Retourne le prix et l'empreinte carbone du produit
        return price, product_details['carbon_footprint'].values[0]
    
    #Affiche un message dans la barre latérale indiquant qu'il s'agit d'un affichage sans authentification
    st.sidebar.write("Affichage sans authentification")
    #Permet à l'utilisateur de choisir son genre à l'aide d'une boîte de sélection dans la barre latérale
    gender = st.sidebar.selectbox("Choisissez votre genre", ["Homme", "Femme"])
    #Filtre les données en fonction du genre sélectionné à l'aide de la fonction "filter_data_by_gender"
    filtered_data = filter_data_by_gender(data, gender)
    #Permet à l'utilisateur de choisir son quota de CO2 à l'aide d'un curseur dans la barre latérale
    co2_quota = st.sidebar.slider("Choisissez votre quota de CO2 (kg)", min_value=1, max_value=2, value=1, step=1)
    
    #Filtre les données pour ne garder que les produits dont l'empreinte carbone est inférieure ou égale au quota de CO2 sélectionné
    filtered_data = filtered_data[filtered_data['carbon_footprint'] <= co2_quota]
    #Applique le clustering sur les données filtrées à l'aide de la fonction "perform_clustering"
    filtered_data = perform_clustering(filtered_data)
    
    #Affiche les vêtements disponibles pour le quota de CO2 et le genre sélectionnés
    st.write(f"Vêtements disponibles pour un quota de {co2_quota} kg de CO2 et le genre {gender} :")
    #Récupère la liste des descriptions de produits à partir des données filtrées
    product_list = filtered_data["description"].tolist()
    #Permet à l'utilisateur de sélectionner plusieurs produits à l'aide d'une boîte de sélection multiple dans la barre latérale
    selected_products = st.sidebar.multiselect("Choisissez des produits", product_list)
    
    #Calcule le quota éthique hebdomadaire en multipliant le quota de CO2 par une constante prédéfinie (DEFAULT_ETHIC_WEEKLY_QUOTA)
    ethic_weekly_quota = DEFAULT_ETHIC_WEEKLY_QUOTA * co2_quota
    
    
    if selected_products:
        #Initialisation des variables pour le prix total et l'impact total
        total_price = 0
        total_impact = 0
        #Parcours des produits sélectionnés
        for product in selected_products:
            #Vérifie si le produit n'est pas déjà dans les prix de la session
            if product not in st.session_state.prices:
                #Génère un prix aléatoire entre 10 et 100 pour le produit
                st.session_state.prices[product] = round(np.random.uniform(10, 100), 2)
              
            #Appelle la fonction display_product_details pour afficher les détails du produit et récupérer le prix et l'impact
            price, impact = display_product_details(product, filtered_data)
            #Ajoute le prix du produit au prix total
            total_price += price
            #Ajoute l'impact du produit à l'impact total
            total_impact += impact
        
        
        #Calcul du pourcentage du quota éthique atteint
        quota_percentage = min(total_impact / ethic_weekly_quota, 1)
        
        #Affichage du prix total, de l'impact total et du progrès par rapport au quota dans la barre latérale
        st.sidebar.write(f"Total du panier : €{round(total_price, 2):.2f}")
        st.sidebar.write(f"Total CO2 : {round(total_impact, 2):.2f} kg")
        st.sidebar.write(f"Progrès par rapport au quota ({co2_quota} kg) :")
        st.sidebar.progress(quota_percentage)
        
        #Vérification du dépassement du quota de CO2
        if total_impact > co2_quota:
            st.error("Paiement bloqué: Veuillez respecté le Quota d'article.")
            #Réinitialisation du panier et des prix de la session
            st.session_state.cart = []
            st.session_state.prices = {}
        
        # Bouton de paiement
        elif st.sidebar.button("Payer"):
            #Vérification si le prix total est supérieur à 0
            if total_price <= 0:
                st.error("Erreur lors du paiement. Le panier est vide.")
            else:
                #Affichage d'un message de paiement réussi avec le montant total
                st.success(f"Paiement réussi! Votre commande a été effectuée pour un montant total de €{round(total_price, 2):.2f}.")
                #Réinitialisation du panier et des prix de la session
                st.session_state.cart = []
                st.session_state.prices = {}
                
    else:
        #Message indiquant de sélectionner des produits
        st.write("Sélectionnez des produits pour afficher les détails et les ajouter à votre panier.")

if __name__ == "__main__":
    # Appel de la fonction ethic_page
    ethic_page()

            

            
            





        




    

    

    









    

    

