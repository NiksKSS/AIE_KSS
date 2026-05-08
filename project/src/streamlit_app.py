import streamlit as st
import pandas as pd
import numpy as np
import joblib
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
from datetime import datetime
from html import escape
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / 'data' / 'data.csv'
MODEL_PATH = PROJECT_ROOT / 'artifacts' / 'model.pkl'
GEOJSON_PATH = PROJECT_ROOT / 'data' / 'Krasnodar_Municipalities_GeoJson.txt'

TARGET_VARS = [
    'precipitation', 'temp', 'tmax', 'tmin', 'solar_radiation',
    'wind_speed', 'wind_direction', 'day_length_hours'
]

TARGET_LABELS = {
    'precipitation': 'Осадки (мм)',
    'temp': 'Средняя температура (°C)',
    'tmax': 'Максимальная температура (°C)',
    'tmin': 'Минимальная температура (°C)',
    'solar_radiation': 'Солнечная радиация (Вт/м²)',
    'wind_speed': 'Скорость ветра (м/с)',
    'wind_direction': 'Направление ветра',
    'day_length_hours': 'Длина светового дня (ч)'
}

TARGET_UNITS = {
    'precipitation': 'мм',
    'temp': '°C',
    'tmax': '°C',
    'tmin': '°C',
    'solar_radiation': 'Вт/м²',
    'wind_speed': 'м/с',
    'day_length_hours': 'ч'
}

REGION_TO_MUNICIPALITY = {
    'Абинск': 'Абинский район',
    'Анапа': 'городской округ Анапа',
    'Апшеронск': 'Апшеронский район',
    'Армавир': 'городской округ Армавир',
    'Белая Глина': 'Белоглинский район',
    'Белореченск': 'Белореченский район',
    'Брюховецкая': 'Брюховецкий район',
    'Выселки': 'Выселковский район',
    'Геленджик': 'городской округ Геленджик',
    'Горячий Ключ': 'городской округ Горячий Ключ',
    'Гулькевичи': 'Гулькевичский район',
    'Динская': 'Динской район',
    'Ейск': 'Ейский район',
    'Калининская': 'Калининский район',
    'Каневская': 'Каневской район',
    'Кореновск': 'Кореновский район',
    'Краснодар': 'городской округ Краснодар',
    'Кропоткин': 'Кавказский район',
    'Крыловская': 'Крыловский район',
    'Крымск': 'Крымский район',
    'Курганинск': 'Курганинский район',
    'Кущёвская': 'Кущёвский район',
    'Лабинск': 'Лабинский район',
    'Ленинградская': 'Ленинградский округ',
    'Мостовской': 'Мостовский район',
    'Новокубанск': 'Новокубанский район',
    'Новопокровская': 'Новопокровский район',
    'Новороссийск': 'городской округ Новороссийск',
    'Отрадная': 'Отрадненский район',
    'Павловская': 'Павловский район',
    'Полтавская': 'Красноармейский район',
    'Приморско-Ахтарск': 'Приморско-Ахтарский округ',
    'Северская': 'Северский район',
    'Славянск-на-Кубани': 'Славянский район',
    'Сочи': 'городской округ Сочи',
    'Староминская': 'Староминский район',
    'Старощербиновская': 'Щербиновский район',
    'Тбилисская': 'Тбилисский район',
    'Темрюк': 'Темрюкский район',
    'Тимашёвск': 'Тимашёвский район',
    'Тихорецк': 'Тихорецкий район',
    'Туапсе': 'Туапсинский район',
    'Успенское': 'Успенский район',
    'Усть-Лабинск': 'Усть-Лабинский район',
}

WIND_DIRECTION_NAMES = [
    'Северный',
    'Северо-восточный',
    'Восточный',
    'Юго-восточный',
    'Южный',
    'Юго-западный',
    'Западный',
    'Северо-западный',
]

DISTRICT_FILL_COLOR = '#dbeafe'
DISTRICT_BORDER_COLOR = '#2563eb'
POINT_FILL_COLOR = '#2563eb'
POINT_BORDER_COLOR = '#ffffff'

st.set_page_config(page_title="Прогноз погоды Краснодарский край", layout="wide")

def apply_custom_styles():
    st.markdown(
        """
        <style>
            .stApp {
                background: #f6f8fb;
                color: #172033;
            }

            .block-container {
                max-width: 1280px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            h1, h2, h3 {
                color: #172033;
                letter-spacing: 0;
            }

            h1 {
                font-size: 2.15rem;
                font-weight: 750;
                margin-bottom: 0.25rem;
            }

            h2 {
                font-size: 1.35rem;
                font-weight: 700;
                margin-top: 0.5rem;
            }

            h3 {
                font-size: 1.05rem;
                font-weight: 700;
            }

            .app-subtitle {
                color: #5b677a;
                font-size: 1rem;
                margin: -0.15rem 0 1.35rem;
            }

            .result-card {
                background: #ffffff;
                border: 1px solid #dce4ee;
                border-left: 4px solid #2563eb;
                border-radius: 8px;
                padding: 1rem 1.1rem;
                margin: 1rem 0 1.25rem;
                box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
            }

            .result-label {
                color: #5b677a;
                font-size: 0.88rem;
                margin-bottom: 0.25rem;
            }

            .result-value {
                color: #172033;
                font-size: 1.35rem;
                font-weight: 750;
                line-height: 1.25;
            }

            .metric-card {
                background: #ffffff;
                border: 1px solid #dce4ee;
                border-radius: 8px;
                padding: 0.95rem 1rem;
                min-height: 92px;
                box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .metric-card-label {
                color: #5b677a;
                font-size: 0.86rem;
                line-height: 1.25;
                margin-bottom: 0.45rem;
            }

            .metric-card-value {
                color: #172033;
                font-size: 1.28rem;
                font-weight: 750;
                line-height: 1.2;
                word-break: break-word;
            }

            div[data-testid="stTabs"] button {
                color: #44546a;
                font-weight: 600;
            }

            div[data-testid="stTabs"] button[aria-selected="true"] {
                color: #1d4ed8;
                border-bottom-color: #1d4ed8;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #dce4ee;
                border-radius: 8px;
                padding: 0.9rem 1rem;
                box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
            }

            div[data-testid="stMetricLabel"] p {
                color: #5b677a;
                font-size: 0.86rem;
            }

            div[data-testid="stMetricValue"] {
                color: #172033;
                font-weight: 750;
            }

            div[data-testid="stSidebar"] {
                background: #ffffff;
                border-right: 1px solid #dce4ee;
            }

            div[data-testid="stAlert"] {
                border-radius: 8px;
                border: 1px solid #dce4ee;
            }

            iframe {
                border-radius: 8px;
                border: 1px solid #dce4ee;
                background: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-card-label">{escape(str(label))}</div>
            <div class="metric-card-value">{escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_metric_grid(items, columns_count=4):
    for start in range(0, len(items), columns_count):
        cols = st.columns(columns_count)
        for col, (label, value) in zip(cols, items[start:start + columns_count]):
            with col:
                render_metric_card(label, value)

def render_result_card(label, value):
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">{escape(str(label))}</div>
            <div class="result-value">{escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache_resource
def load_model_info():
    return joblib.load(MODEL_PATH)

@st.cache_resource
def load_geojson():
    return gpd.read_file(GEOJSON_PATH)

def get_region_label(region_name):
    district_name = REGION_TO_MUNICIPALITY.get(region_name, region_name)
    return f"{region_name} / {district_name}"

def get_selected_district(region_name, municipalities):
    district_name = REGION_TO_MUNICIPALITY.get(region_name)
    if district_name:
        district = municipalities[municipalities['r_reg_name'] == district_name]
        if not district.empty:
            return district
    
    return municipalities[
        municipalities['r_reg_name'].str.contains(region_name, case=False, na=False)
    ]

def get_district_geometry(district):
    if district.empty:
        return None
    if len(district) == 1:
        return district.geometry.iloc[0]
    return district.geometry.unary_union

def point_is_in_district(row, district_geometry):
    point = Point(row['lon'], row['lat'])
    return district_geometry.covers(point)

def filter_by_district_geometry(df, district_geometry):
    if df.empty or district_geometry is None:
        return df.copy()
    
    inside_mask = df.apply(lambda row: point_is_in_district(row, district_geometry), axis=1)
    return df[inside_mask].copy()

def get_region_points(region_name, data, district_geometry=None):
    point_columns = ['admin_center', 'lat', 'lon', 'sea_border', 'mountain_border']
    region_points = (
        data.loc[data['admin_center'] == region_name, point_columns]
        .drop_duplicates(subset=['lat', 'lon'])
        .copy()
    )
    return filter_by_district_geometry(region_points, district_geometry).reset_index(drop=True)

def get_historical_region_data(region_name, date, data, district_geometry=None):
    selected_date = pd.Timestamp(date).date()
    region_rows = data.loc[data['admin_center'] == region_name].copy()
    historical_data = region_rows.loc[
        region_rows['date'].dt.date == selected_date
    ].copy()
    return filter_by_district_geometry(historical_data, district_geometry)

def get_date_parts(date):
    dt = pd.Timestamp(date)
    return dt.month, dt.day, dt.dayofyear

def prepare_features_for_points(points_df, date, admin_center):
    month, day, dayofyear = get_date_parts(date)
    features_df = points_df[['lat', 'lon', 'sea_border', 'mountain_border']].copy()
    features_df['month'] = month
    features_df['day'] = day
    features_df['dayofyear'] = dayofyear
    features_df['mountain_border'] = features_df['mountain_border'].astype(int)
    features_df['admin_center'] = admin_center
    
    return features_df[
        ['lat', 'lon', 'month', 'day', 'dayofyear', 'sea_border', 'mountain_border', 'admin_center']
    ]

def predict_weather_for_points(features_df, model):
    if features_df.empty:
        return pd.DataFrame(columns=TARGET_VARS)
    
    predictions = model.predict(features_df)
    predictions_df = pd.DataFrame(predictions, columns=TARGET_VARS)
    predictions_df['wind_direction'] = predictions_df['wind_direction'] % 360
    return predictions_df

def circular_mean_degrees(values):
    series = pd.to_numeric(pd.Series(values), errors='coerce').dropna()
    if series.empty:
        return np.nan
    
    radians = np.deg2rad(series % 360)
    sin_mean = np.sin(radians).mean()
    cos_mean = np.cos(radians).mean()
    
    if np.isclose(sin_mean, 0) and np.isclose(cos_mean, 0):
        return np.nan
    
    return (np.rad2deg(np.arctan2(sin_mean, cos_mean)) + 360) % 360

def aggregate_parameter(values, parameter):
    if parameter == 'wind_direction':
        return circular_mean_degrees(values)
    
    return pd.to_numeric(pd.Series(values), errors='coerce').mean()

def aggregate_weather(df):
    return {
        parameter: aggregate_parameter(df[parameter], parameter)
        for parameter in TARGET_VARS
    }

def wind_direction_to_text(value):
    if pd.isna(value):
        return "Нет данных"
    
    normalized = value % 360
    direction_index = int((normalized + 22.5) // 45) % len(WIND_DIRECTION_NAMES)
    return WIND_DIRECTION_NAMES[direction_index]

def format_weather_value(parameter, value, with_unit=False):
    if pd.isna(value):
        return "Нет данных"
    
    if parameter == 'wind_direction':
        return wind_direction_to_text(value)
    
    decimals = 0 if parameter == 'solar_radiation' else 2
    formatted_value = f"{value:.{decimals}f}"
    
    if with_unit and parameter in TARGET_UNITS:
        return f"{formatted_value} {TARGET_UNITS[parameter]}"
    
    return formatted_value

def create_map_for_district(district, tiles):
    if district.empty:
        return folium.Map(location=[45.0, 39.0], zoom_start=7, tiles=tiles)
    
    min_lon, min_lat, max_lon, max_lat = district.total_bounds
    map_center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
    weather_map = folium.Map(location=map_center, zoom_start=10, tiles=tiles, control_scale=True)
    weather_map.fit_bounds(
        [[min_lat, min_lon], [max_lat, max_lon]],
        padding=(24, 24),
        max_zoom=12
    )
    return weather_map

def get_map_component_key(prefix, region_name, date, parameter=None):
    key_parts = [prefix, region_name, str(date)]
    if parameter:
        key_parts.append(parameter)
    return "_".join(str(part).replace(" ", "_").replace("/", "_") for part in key_parts)

def add_selected_district_to_map(weather_map, district, region_name):
    if district.empty:
        return
    
    folium.GeoJson(
        district,
        name=get_region_label(region_name),
        style_function=lambda x: {
            'fillColor': DISTRICT_FILL_COLOR,
            'color': DISTRICT_BORDER_COLOR,
            'weight': 2,
            'fillOpacity': 0.28
        },
        tooltip=folium.GeoJsonTooltip(fields=['r_reg_name'], aliases=['Район:'])
    ).add_to(weather_map)

def add_point_to_map(weather_map, lat, lon, popup_text):
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        popup=popup_text,
        color=POINT_BORDER_COLOR,
        weight=2,
        fill=True,
        fillColor=POINT_FILL_COLOR,
        fillOpacity=0.95
    ).add_to(weather_map)

def main():
    apply_custom_styles()
    st.title("Прогноз погоды в Краснодарском крае")
    st.markdown(
        '<div class="app-subtitle">Муниципальные районы Краснодарского края</div>',
        unsafe_allow_html=True
    )
    
    data = load_data()
    model_info = load_model_info()
    model = model_info['model']
    municipalities = load_geojson()
    
    regions = sorted(data['admin_center'].unique().tolist())
    
    st.sidebar.header("Настройки карты")
    map_tiles = st.sidebar.selectbox("Подложка", ["CartoDB Positron", "OpenStreetMap", "CartoDB Dark Matter"], key="map_tiles")
    
    tab1, tab2, tab3 = st.tabs(["Погода в прошлом", "Прогноз погоды", "Карта погоды"])
    
    with tab1:
        st.header("Погода в прошлом")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_region = st.selectbox(
                "Выберите город / район",
                regions,
                format_func=get_region_label,
                key="tab1_region"
            )
        with col2:
            selected_date = st.date_input("Выберите дату", value=datetime(2023, 6, 15), min_value=datetime(1995, 1, 1), max_value=datetime(2023, 12, 31), key="tab1_date")
        
        selected_param = st.selectbox(
            "Выберите параметр для карты",
            TARGET_VARS,
            format_func=lambda x: TARGET_LABELS[x],
            key="tab1_param"
        )
        
        if selected_region and selected_date:
            selected_district = get_selected_district(selected_region, municipalities)
            
            if selected_district.empty:
                st.warning("Не найден мультиполигон для выбранного района")
            else:
                district_geometry = get_district_geometry(selected_district)
                historical_data = get_historical_region_data(
                    selected_region,
                    selected_date,
                    data,
                    district_geometry
                )
                
                if historical_data.empty:
                    st.warning("Нет данных для выбранной даты")
                else:
                    value = aggregate_parameter(historical_data[selected_param], selected_param)
                    render_result_card(
                        f"{TARGET_LABELS[selected_param]} в {get_region_label(selected_region)} на {selected_date}",
                        format_weather_value(selected_param, value, with_unit=True)
                    )
                    
                    st.subheader("Параметры района")
                    metric_items = []
                    for var in TARGET_VARS:
                        val = aggregate_parameter(historical_data[var], var)
                        metric_items.append((TARGET_LABELS[var], format_weather_value(var, val, with_unit=True)))
                    render_metric_grid(metric_items)
                    
                    st.subheader("Карта района")
                    
                    m = create_map_for_district(selected_district, map_tiles)
                    add_selected_district_to_map(m, selected_district, selected_region)
                    
                    point_values = (
                        historical_data
                        .groupby(['lat', 'lon'])[selected_param]
                        .apply(lambda values: aggregate_parameter(values, selected_param))
                        .reset_index(name='value')
                    )
                    region_points = get_region_points(selected_region, data, district_geometry)
                    points_data = (
                        region_points[['lat', 'lon']]
                        .merge(point_values, on=['lat', 'lon'], how='left')
                    )
                    
                    for _, row in points_data.iterrows():
                        popup_text = (
                            f"<b>{get_region_label(selected_region)}</b><br>"
                            f"{TARGET_LABELS[selected_param]}: "
                            f"{format_weather_value(selected_param, row['value'], with_unit=True)}"
                        )
                        
                        add_point_to_map(m, row['lat'], row['lon'], popup_text)
                    
                    st_folium(
                        m,
                        height=600,
                        use_container_width=True,
                        returned_objects=[],
                        key=get_map_component_key("history_map", selected_region, selected_date, selected_param)
                    )
    
    with tab2:
        st.header("Прогноз погоды")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_region_forecast = st.selectbox(
                "Выберите город / район",
                regions,
                format_func=get_region_label,
                key="tab2_region"
            )
        with col2:
            selected_date_forecast = st.date_input("Выберите дату", value=datetime.now(), key="tab2_date")
        
        if selected_region_forecast and selected_date_forecast:
            selected_district_forecast = get_selected_district(selected_region_forecast, municipalities)
            
            if selected_district_forecast.empty:
                st.warning("Не найден мультиполигон для выбранного района")
            else:
                district_geometry = get_district_geometry(selected_district_forecast)
                region_points = get_region_points(selected_region_forecast, data, district_geometry)
                
                if region_points.empty:
                    st.warning("В выбранном районе нет точек из датасета")
                else:
                    features_df = prepare_features_for_points(
                        region_points,
                        selected_date_forecast,
                        selected_region_forecast
                    )
                    point_predictions = predict_weather_for_points(features_df, model)
                    predictions = aggregate_weather(point_predictions)
                    
                    st.subheader(f"Прогноз погоды в {get_region_label(selected_region_forecast)} на {selected_date_forecast}")
                
                    forecast_cards = [
                        (TARGET_LABELS['temp'], format_weather_value('temp', predictions['temp'], with_unit=True)),
                        (TARGET_LABELS['tmax'], format_weather_value('tmax', predictions['tmax'], with_unit=True)),
                        (TARGET_LABELS['tmin'], format_weather_value('tmin', predictions['tmin'], with_unit=True)),
                        (TARGET_LABELS['precipitation'], format_weather_value('precipitation', predictions['precipitation'], with_unit=True)),
                        (TARGET_LABELS['wind_speed'], format_weather_value('wind_speed', predictions['wind_speed'], with_unit=True)),
                        (TARGET_LABELS['wind_direction'], format_weather_value('wind_direction', predictions['wind_direction'], with_unit=True)),
                        (TARGET_LABELS['solar_radiation'], format_weather_value('solar_radiation', predictions['solar_radiation'], with_unit=True)),
                        (TARGET_LABELS['day_length_hours'], format_weather_value('day_length_hours', predictions['day_length_hours'], with_unit=True)),
                    ]
                    render_metric_grid(forecast_cards)
    
    with tab3:
        st.header("Карта погоды")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_city_map = st.selectbox(
                "Выберите город / район",
                regions,
                format_func=get_region_label,
                key="tab3_region"
            )
        with col2:
            map_date = st.date_input("Выберите дату", value=datetime.now(), key="tab3_date")
        with col3:
            map_param = st.selectbox("Выберите параметр", TARGET_VARS, format_func=lambda x: TARGET_LABELS[x], key="tab3_param")
        
        if selected_city_map and map_date:
            selected_district_map = get_selected_district(selected_city_map, municipalities)
            
            if selected_district_map.empty:
                st.warning("Не найден мультиполигон для выбранного района")
            else:
                district_geometry = get_district_geometry(selected_district_map)
                region_points = get_region_points(selected_city_map, data, district_geometry)
                
                if region_points.empty:
                    st.warning("В выбранном районе нет точек из датасета")
                else:
                    features_df = prepare_features_for_points(region_points, map_date, selected_city_map)
                    point_predictions = predict_weather_for_points(features_df, model)
                    predictions_df = pd.concat(
                        [
                            region_points[['lat', 'lon']].reset_index(drop=True),
                            point_predictions.reset_index(drop=True)
                        ],
                        axis=1
                    )
                    
                    st.subheader(f"{TARGET_LABELS[map_param]} в {get_region_label(selected_city_map)} на {map_date}")
                    
                    m = create_map_for_district(selected_district_map, map_tiles)
                    add_selected_district_to_map(m, selected_district_map, selected_city_map)
                    
                    for _, row in predictions_df.iterrows():
                        popup_text = (
                            f"<b>{get_region_label(selected_city_map)}</b><br>"
                            f"Широта: {row['lat']:.2f}<br>"
                            f"Долгота: {row['lon']:.2f}<br>"
                            f"{TARGET_LABELS[map_param]}: "
                            f"{format_weather_value(map_param, row[map_param], with_unit=True)}"
                        )
                        
                        add_point_to_map(m, row['lat'], row['lon'], popup_text)
                    
                    st_folium(
                        m,
                        height=600,
                        use_container_width=True,
                        returned_objects=[],
                        key=get_map_component_key("forecast_map", selected_city_map, map_date, map_param)
                    )

if __name__ == "__main__":
    main()
