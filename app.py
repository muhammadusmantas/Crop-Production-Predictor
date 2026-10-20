import streamlit as st # For creating the GUI
import joblib # For loading the model
import os     # For loading the correct path of model

st.title('🌾Crop Production Predictor🌿')
crop = st.selectbox(
    'Crop type',
    ['Rice','Maize','Wheat','Moong (Green Gram)','Groundnut (MoongPhali)']
)
st.write('Random Forest is Recommended')
selected_model = st.selectbox(
    'Model',
    ['Random Forest','CatBoost','XGB','LGBM','KNN']
)
season = st.selectbox(
    'Season',
    ['Autumn','Kharif','Rabi','Summer','Whole year','Winter']
)
season_autumn = season == 'Autumn'
season_kharif = season == 'Kharif'
season_rabi = season == 'Rabi'
season_summer = season == 'Summer'
season_whole_year = season == 'Whole year'
season_winter = season == 'Winter'

st.subheader('Features')
col1, col2 = st.columns(2)
with col1:
    area = st.number_input('Area(hectares)',value = None, placeholder = 'Enter Area in hectares ',min_value = 0.0)
    rainfall = st.number_input('Annual Rainfall(mm)',value = None,placeholder = 'Enter Annual Rainfall here',min_value = 0.0)
    max_rainfall = 6552.7
    min_rainfall = 300
    if rainfall is not None and rainfall > max_rainfall:
        st.warning('The model is not trained on too much rainfall, You can still proceed but the Prediction can be suspicious')
    if rainfall is not None and rainfall < min_rainfall:
        st.warning('The model is not trained on too less rainfall, You can still proceed but the Prediction can be suspicious')
with col2:
    fertilizer = st.number_input('Fertilizer(MT)',value = None,placeholder = 'Enter Fertilizer in Metric Tonne\'s',min_value = 0.0)
    pesticide = st.number_input('Pesticide(Kg\'s)',value = None,placeholder = 'Enter Pesticides in Kilogram\'s',min_value = 0.0)
    max_fertilizer_per_area = 0.2
    max_pesticide_per_area = 0.4
    if fertilizer is not None and area is not None and area > 0:
        fertilizer_per_area = fertilizer/area
        if fertilizer_per_area > max_fertilizer_per_area:
            st.warning('Fertilizer Quantity seems unusually high, Please make sure it is in Metric Tonnes')
    if pesticide is not None and area is not None and area > 0:
        pesticide_per_area = pesticide/area
        if pesticide_per_area > max_pesticide_per_area:
            st.warning('Pesticide Quantity seems unusually high, Please make sure it is in Kilograms')
input_data = [[
            area,
            rainfall,
            fertilizer,
            pesticide,
            season_autumn,
            season_kharif,
            season_rabi,
            season_summer,
            season_whole_year,
            season_winter 
        ]]

# For Setting the color of Prediction Button
st.markdown("""
<style>
div.stButton > button {
    background-color: green;
    color: white;
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Code for finding the Base directory, I mean the folder of this file
                                                      # Because the Python was having the problem when loading the model
model_paths = {
    'Rice': {
        'Random Forest': os.path.join(BASE_DIR,'models','Rice RandomForest.pkl'),
        'CatBoost': os.path.join(BASE_DIR,'models','Rice Catboost.pkl'),
        'XGB': os.path.join(BASE_DIR,'models','Rice XGB.pkl'),
        'LGBM': os.path.join(BASE_DIR,'models','Rice LGBM.pkl'),
        'KNN': os.path.join(BASE_DIR,'models','Rice KNN.pkl')

    },
    'Maize': {
        'Random Forest': os.path.join(BASE_DIR,'models','Maize RandomForest.pkl'),
        'CatBoost': os.path.join(BASE_DIR,'models','Maize Catboost.pkl'),
        'XGB': os.path.join(BASE_DIR,'models','Maize XGB.pkl'),
        'LGBM': os.path.join(BASE_DIR,'models','Maize LGBM.pkl'),
        'KNN': os.path.join(BASE_DIR,'models','Maize KNN.pkl')

    },
    'Wheat':{
        'Random Forest': os.path.join(BASE_DIR, 'models','Wheat RandomForest.pkl'),
        'CatBoost': os.path.join(BASE_DIR,'models','Wheat Catboost.pkl'),
        'XGB': os.path.join(BASE_DIR,'models','Wheat XGB.pkl'),
        'LGBM': os.path.join(BASE_DIR,'models','Wheat LGBM.pkl'),
        'KNN': os.path.join(BASE_DIR,'models','Wheat KNN.pkl')
    },
    'Moong (Green Gram)':{
        'Random Forest':os.path.join(BASE_DIR, 'models','Moong RandomForest.pkl'),
        'CatBoost': os.path.join(BASE_DIR,'models','Moong Catboost.pkl'),
        'XGB': os.path.join(BASE_DIR,'models','Moong XGB.pkl'),
        'LGBM': os.path.join(BASE_DIR,'models','Moong LGBM.pkl'),
        'KNN': os.path.join(BASE_DIR,'models','Moong KNN.pkl')
    },
    'Groundnut (MoongPhali)':{
        'Random Forest':os.path.join(BASE_DIR, 'models','Groundnut RandomForest.pkl'),
        'CatBoost': os.path.join(BASE_DIR,'models','Groundnut Catboost.pkl'),
        'XGB': os.path.join(BASE_DIR,'models','Groundnut XGB.pkl'),
        'LGBM': os.path.join(BASE_DIR,'models','Groundnut LGBM.pkl'),
        'KNN': os.path.join(BASE_DIR,'models','Groundnut KNN.pkl')

    }
}
if st.button('Predict Production(Metric Tonnes)'):
    pass
    if None in [area,rainfall,fertilizer,pesticide]:
        st.warning('🎃 Please, Enter all required values')
    else:
        model = joblib.load(model_paths[crop][selected_model])
        prediction = model.predict(input_data)
        if prediction < 0:
            st.error('Oops, Prediction Failed, because Model gave a negative Prediction, which is practically not possible')
        else:
            st.success(f'Predicted production {prediction} Metric Tonnes')