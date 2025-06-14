import streamlit as st
import requests

# Fonction pour récupérer le taux de change
def get_exchange_rate(from_currency, to_currency):
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        data = response.json()
        return data['rates'][to_currency]
    except Exception as e:
        st.error(f"Erreur lors de la récupération du taux de change : {e}")
        return None

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Convertisseur EUR-ALL",
    page_icon="💶",
    layout="centered",
    initial_sidebar_state="auto",
)

# Titre de l'application
st.title("Convertisseur de devises")
st.header("EUR 🇪🇺 vers ALL 🇦🇱")

# Récupérer le taux de change
rate_eur_to_all = get_exchange_rate('EUR', 'ALL')
rate_all_to_eur = get_exchange_rate('ALL', 'EUR')

if rate_eur_to_all and rate_all_to_eur:
    st.subheader("Taux de change actuels")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="EUR ➡️ ALL", value=f"{rate_eur_to_all:.4f} ALL")
    with col2:
        st.metric(label="ALL ➡️ EUR", value=f"{rate_all_to_eur:.4f} EUR")
    
    st.markdown("---")

    # Options de conversion
    conversion_direction = st.radio(
        "Choisissez le sens de la conversion :",
        ('EUR vers ALL', 'ALL vers EUR')
    )

    # Champ de saisie pour le montant
    amount = st.number_input("Montant à convertir", min_value=0.0, format="%.2f")

    # Calcul et affichage du résultat
    if st.button("Convertir"):
        if conversion_direction == 'EUR vers ALL':
            converted_amount = amount * rate_eur_to_all
            st.success(f"**{amount:.2f} EUR = {converted_amount:.2f} ALL**")
            st.write(f"_(Taux utilisé : 1 EUR = {rate_eur_to_all:.4f} ALL)_")
        else:
            converted_amount = amount * rate_all_to_eur
            st.success(f"**{amount:.2f} ALL = {converted_amount:.2f} EUR**")
            st.write(f"_(Taux utilisé : 1 ALL = {rate_all_to_eur:.4f} EUR)_")

else:
    st.warning("Impossible de récupérer le taux de change. Veuillez réessayer plus tard.")