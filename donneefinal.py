import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout="wide")

# Charger les données
df = pd.read_csv('./Data/df_lieu_equip_cult.csv')
df_departements_de_france = pd.read_csv('./Data/departements-france.csv')

festival_first_10_cols = pd.read_csv('./Data/festival_first_10_cols.csv')
df_site_architecture= pd.read_csv('./Data/df_site_architecture.csv')
concat_musee_dataframe_departement= pd.read_csv('./Data/concat_musee_dataframe_departement.csv')

col1, col3 = st.columns([4, 2], gap="small")

col1.header ("_La France touristique_")



 #Département cible
department_to_focus = "38"  # Remplacez par le département à cibler

# Filtrer les données du DataFrame pour le département spécifique
filtered_department_df = df[df['N_Département'] == department_to_focus]



# Sélectionner le département
unique_departement = ["Tous les départements"] + sorted(df['N_Département'].unique().tolist())
Option_N_département = st.selectbox("Choisissez un département :", unique_departement, key="departement_selectbox" )  # Unique key 


# Filtrer les villes en fonction du département sélectionné
if Option_N_département == "Tous les départements":
    unique_villes = ["Toutes les villes"] + sorted(df['Ville'].dropna().unique().tolist())
else:
    unique_villes = ["Toutes les villes"] + sorted(df[df['N_Département'] == Option_N_département]['Ville'].dropna().unique().tolist())

# Sélectionner la ville
Option_unique_ville = st.selectbox("Choisissez une ville :", unique_villes, key="ville_selectbox")

# Filtrer les données en fonction du département et de la ville
if Option_N_département == "Tous les départements":
    # Si "Tous les départements" est sélectionné, on ne filtre pas par département
    filtered_df = df[df['Ville'] == Option_unique_ville] if Option_unique_ville != "Toutes les villes" else df
else:
    # Si un département est sélectionné
    if Option_unique_ville == "Toutes les villes":
        filtered_df = df[df['N_Département'] == Option_N_département]
    else:
        # Si un département et une ville spécifiques sont sélectionnés
        filtered_df = df[(df['N_Département'] == Option_N_département) & (df['Ville'] == Option_unique_ville)]

#Supprimer les lignes avec des coordonnées manquantes (NaN)
filtered_df = filtered_df.dropna(subset=['latitude', 'longitude'])



 #Vérifier si des données filtrées existent
if not filtered_department_df.empty:
    # Calculer le centre de la carte basé sur les données filtrées
     center_lat = filtered_department_df['latitude'].mean()
     center_lon = filtered_department_df['longitude'].mean()
else:
     center_lat, center_lon = 48.8566, 2.3522  # Par défaut, Paris si aucune donnée trouvée


department_to_zoom = Option_N_département
ville_to_zoom = Option_unique_ville


#Calculate the center of the map based on filtered data




    
if Option_N_département != "Tous les départements":
    filtered_department_df = df[df['N_Département'] == Option_N_département]
    center_lat = filtered_department_df['latitude'].mean()
    center_lon = filtered_department_df['longitude'].mean()
    lat_diff = filtered_department_df['latitude'].max() - filtered_department_df['latitude'].min()
    lon_diff = filtered_department_df['longitude'].max() - filtered_department_df['longitude'].min()

    # Zoom logic
    if Option_unique_ville == "Toutes les villes":
        zoom_level = max(8 - (lat_diff + lon_diff) * 5, 6)  # Zoom on department
    else:
        zoom_level = max(10 - (lat_diff + lon_diff) * 5, 8)  # Zoom on city
else:
    center_lat, center_lon = 48.8566, 2.3522  # Default to Paris
    zoom_level = 5


    
    #afficher texte


nb_musee1 = (concat_musee_dataframe_departement['Catégorie']== 'Musée')
nb_musee_2 = concat_musee_dataframe_departement[nb_musee1][concat_musee_dataframe_departement['N_Département'].astype(str) == str(Option_N_département)]
nb_musee2 = len(nb_musee_2)




    
if Option_N_département != "Tous les départements":
    filtered_department_df = df[df['N_Département'] == Option_N_département]
    center_lat = filtered_department_df['latitude'].mean()
    center_lon = filtered_department_df['longitude'].mean()
    lat_diff = filtered_department_df['latitude'].max() - filtered_department_df['latitude'].min()
    lon_diff = filtered_department_df['longitude'].max() - filtered_department_df['longitude'].min()

    # Zoom logic
    if Option_unique_ville == "Toutes les villes":
        zoom_level = max(8 - (lat_diff + lon_diff) * 5, 6)  # Zoom on department
    else:
        zoom_level = max(10 - (lat_diff + lon_diff) * 5, 8)  # Zoom on city
else:
    center_lat, center_lon = 48.8566, 2.3522  # Default to Paris
    zoom_level = 5


    
    #afficher texte


nb_musee1 = (concat_musee_dataframe_departement['Catégorie']== 'Musée')
nb_musee_2 = concat_musee_dataframe_departement[nb_musee1][concat_musee_dataframe_departement['N_Département'].astype(str) == str(Option_N_département)]
nb_musee2 = len(nb_musee_2)





# Filtrer en une seule étape avec les deux conditions
nb_culturel_2 = df[(df['Catégorie'] == 'Bibliothèque') & (df['N_Département'].astype(str) == str(Option_N_département))]
nb_culturel2 = len(nb_culturel_2 )




# Filtrer le nom du département correspondant à l'option sélectionnée
# departement_correspondant = df_site_architecture['Département'][df_site_architecture['N_Département'].astype(str) == str(Option_N_département)]




df_site_architecture.columns = df_site_architecture.columns.str.strip()
                                                                                    
#df_site_architecture['N_Département'] = df_site_architecture['N_Département'].astype(str).str.strip()


# n = df_departements_de_france[N_departement].dtype
# st.write('Emiliedept', n)


#festival_first_10_cols = festival_first_10_cols.columns.str.strip()
                                  
#df_site_architecture['N_Département'] = df_site_architecture['N_Département'].astype(str).str.strip()


Option_N_départementAsFloat = float(Option_N_département)


festival_first_10_cols['N_Département'] = (
    festival_first_10_cols['N_Département']
    .astype(str)           # ensure everything is a string
    .str.strip()           # remove spaces
    .str.replace(',', '.') # handle commas if present
)



# Ensure the N_Département column is converted to float safely
festival_first_10_cols['N_Département'] = pd.to_numeric(
    festival_first_10_cols['N_Département'], errors='coerce'
).astype(float)

st.write('emilie', festival_first_10_cols['N_Département'].head())
st.write('emilie 2', Option_N_département)
st.write('emilie 3', Option_N_départementAsFloat)
st.write('emilie 4', festival_first_10_cols.query('N_Département == @Option_N_départementAsFloat'))


festival_correspondant = festival_first_10_cols.query('N_Département == @Option_N_départementAsFloat')["Département"]
festival_departement_name = festival_correspondant.iloc[0] if not festival_correspondant.empty else "Inconnu"
nb_festival_department_name_count = len (festival_correspondant) 




departement_correspondant = df_site_architecture.query('N_Département == @Option_N_départementAsFloat')["Département"]

departement_name = departement_correspondant.iloc[0] if not departement_correspondant.empty else "Inconnu"

nb_site_architecture=len(departement_correspondant)



# for display departement name in the box

df_departements_de_france.rename(columns={'N_Departement':'N_Département'}, inplace = True)
df_departements_de_france.rename(columns= {'Departement': 'Département'}, inplace = True)


df_departements_de_france['N_Département'] = (
df_departements_de_france['N_Département']
    .astype(str)           # ensure everything is a string
    .str.strip()           # remove spaces
    .str.replace(',', '.') # handle commas if present
)

# Ensure the N_Département column is converted to float safely
df_departements_de_france['N_Département'] = pd.to_numeric(
df_departements_de_france['N_Département'], errors='coerce'
)
departement_de_france_correspondant = df_departements_de_france.query('N_Département == @Option_N_départementAsFloat')["Département"]

st.write('emilie2', len (departement_de_france_correspondant))

departement_de_france_name = departement_de_france_correspondant.iloc[0] if not departement_de_france_correspondant.empty else "Inconnu"












# Afficher le nom du département dans le sous-titre
col3.subheader(f"Département : {departement_de_france_name}")

if not nb_culturel_2.empty:
    col3.write(f":blue[Nombre de bibliothéques] {nb_culturel2} ")
else:
   col3.write(f":blue[Nombre de bibliothéques]: Inconnu")



#col3.write(f":blue[Département:]{Option_N_département }")
if not nb_musee_2.empty:
    col3.write(f":blue[Nombre de musées:] {nb_musee2} ")
else: 
    col3.write(f":blue[Nombre de musées]: Inconnu")


if nb_festival_department_name_count > 0: 
    col3.write(f":blue[Nombre de festivals:] {nb_festival_department_name_count}")
else:
   col3.write(f":blue[Nombre de Festival]: Inconnu")


if nb_site_architecture > 0:
    col3.write(f":blue[Nombre de sites architecturaux:] {nb_site_architecture}")
else:
   col3.write(f":blue[Nombre de Festival]: Inconnu")


# Création de la première figure


fig3 = go.Figure()

fig3.add_trace(
    go.Scattermapbox(
        lat=concat_musee_dataframe_departement['latitude'],
        lon=concat_musee_dataframe_departement['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5,
            color='rgb(100, 255, 100)',  # Green color
            opacity=1.0
        ),
         name="Musées",
        customdata=concat_musee_dataframe_departement[['Nom', 'Intérêt','Adresse', 'Ville']],
        hovertemplate="<br>".join([
            "Nom: %{customdata[0]}",
            "Intérêt: %{customdata[1]}",
            "Adresse: %{customdata[2]}",
            "Ville: %{customdata[3]}"
        ])
    )
)


# Création de la deuxième figure

fig = go.Figure()
fig.add_trace(go.Scattermapbox(
    lat=filtered_df["latitude"],
    lon=filtered_df["longitude"],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=5,
        color='rgb(255,0,50)',  # Couleur rouge
        opacity=1.0
    ),
     name="Lieux culturels",
    customdata=filtered_df[['Nom', 'Adresse', 'Ville']].values,
    hovertemplate="<br>".join([
        "Nomination : %{customdata[0]}",
        "Adresse : %{customdata[1]}",
        "Ville : %{customdata[2]}"
    ])))

fig4 = go.Figure()
fig4.add_trace(go.Scattermapbox(
    lat=festival_first_10_cols['Géocodage x'],
    lon=festival_first_10_cols['Géocodage y'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=5,
        color='rgb(0,0,525)',  # Couleur bleue
        opacity=1.0
    ),
     name="Festival",
    customdata = festival_first_10_cols[['Nom', 'Discipline dominante', 'Période principale de déroulement du festival', 'Site internet du festival']].values,
    hovertemplate="<br>".join([
        "Nom du festival : %{customdata[0]}",
        "Discipline dominante: %{customdata[1]}",
        "Période principale de déroulement du festival: %{customdata[2]}",
        "Site internet du festival: %{customdata[3]}"
    
    ])))

# Add traces from fig2 (e.g., Musées)

fig2 = go.Figure()


fig2.add_trace(
    go.Scattermapbox(
        lat=df_site_architecture['latitude'],
        lon=df_site_architecture['longitude'],
        mode='markers',
        marker=dict(
            size=5,
            color='rgb(0, 0, 0)',  # Grey color
            opacity=1.0
        ),
         name="Sites architecturaux",
        customdata=df_site_architecture[['Nomination', 'Description', 'Adresse','Ville']],
        hovertemplate="<br>".join([
            "Nom: %{customdata[0]}",
            "Intérêt: %{customdata[1]}",
            "Adresse: %{customdata[2]}",
            "Ville: %{customdata[3]}"
        ])
))




#Combinaison des figures
combined_fig = go.Figure()

st.markdown("""
    <style>
        .plot-frame {
            border: 4px solid #4CAF50;               /* green frame */
            border-radius: 15px;                     /* rounded corners */
        
        }
    </style>
""", unsafe_allow_html=True)






# Mise à jour du layout
combined_fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=zoom_level,
        center=dict(lat=center_lat, lon=center_lon)
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend=dict(
        title="Catégories",
        orientation="v",
        x=0.01,
        y=0.99,
        tracegroupgap=5,      # Space between legend items
        itemsizing='trace',   # Sizing of items in the legend
        font=dict(size=12)    # Font size for the legend items
    )
)





#Add traces from fig

combined_fig=go.Figure()

for trace in fig.data:
    combined_fig.add_trace(trace)
  
# Add traces from fig2
for trace in fig2.data:
    combined_fig.add_trace(trace)

# Add traces from fig3
for trace in fig3.data:
    combined_fig.add_trace(trace)

for trace in fig4.data:
    combined_fig.add_trace(trace)

# Set a common layout for the combined map
combined_fig.update_layout(
    mapbox=dict(
        style="carto-positron",  # Map style
        zoom=zoom_level,
        center=dict(lat=center_lat, lon=center_lon) # Center the map (example: Paris coordinates)
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0}, # Remove margins for better fit
    legend=dict(
        title="Catégories",  # Title of the legend
        orientation="v",     # Vertical orientation
        x=0.01,              # Position of the legend
        y=0.99
    ))



#st.write(f"Département sélectionné : {Département} département")
col1.write(combined_fig)



