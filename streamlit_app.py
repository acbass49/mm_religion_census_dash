import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from urllib.request import urlopen
import json

# Load GeoJSON
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Load data
data = pd.read_csv('https://raw.githubusercontent.com/acbass49/mm_religion_census_dash/refs/heads/main/lds_urban_rural_merged.csv')
data['fips_str'] = data['fips'].astype(str).str.zfill(5)
data['pct_change_lds_filled'] = data['pct_change_lds'].fillna(0)
data['membership_change'] = data['LDSADH_2020'].fillna(0) - data['LDSADH'].fillna(0)
data['congregation_change'] = data['LDSCNG_2020'].fillna(0) - data['LDSCNG'].fillna(0)
data['pct_change_cong_filled'] = data['pct_change_cong'].fillna(0)
data['LDSADH'] = data['LDSADH'].fillna(0)
data['LDSADH_2020'] = data['LDSADH_2020'].fillna(0)
data['LDSCNG'] = data['LDSCNG'].fillna(0)
data['LDSCNG_2020'] = data['LDSCNG_2020'].fillna(0)
data['number_of_congregations_2010'] = data['LDSCNG'].fillna(0)
data['number_of_congregations_2020'] = data['LDSCNG_2020'].fillna(0)
data['number_of_members_2010'] = data['LDSADH'].fillna(0)
data['number_of_members_2020'] = data['LDSADH_2020'].fillna(0)

# Define state zoom settings
state_zoom_settings = {
    "AL": {"lat": 32.806671, "lon": -86.791130, "projection_scale": 5},
    "AK": {"lat": 61.370716, "lon": -152.404419, "projection_scale": 2.5},
    "AZ": {"lat": 33.729759, "lon": -111.431221, "projection_scale": 3.5},
    "AR": {"lat": 34.969704, "lon": -92.373123, "projection_scale": 4},
    "CA": {"lat": 36.116203, "lon": -119.681564, "projection_scale": 2},
    "CO": {"lat": 39.059811, "lon": -105.311104, "projection_scale": 5},
    "CT": {"lat": 41.597782, "lon": -72.755371, "projection_scale": 6},
    "DE": {"lat": 39.318523, "lon": -75.507141, "projection_scale": 7},
    "FL": {"lat": 27.766279, "lon": -81.686783, "projection_scale": 3},
    "GA": {"lat": 33.040619, "lon": -83.643074, "projection_scale": 4},
    "HI": {"lat": 21.094318, "lon": -157.498337, "projection_scale": 4},
    "ID": {"lat": 44.240459, "lon": -114.478828, "projection_scale": 5},
    "IL": {"lat": 40.349457, "lon": -88.986137, "projection_scale": 4},
    "IN": {"lat": 39.849426, "lon": -86.258278, "projection_scale": 4},
    "IA": {"lat": 42.011539, "lon": -93.210526, "projection_scale": 4},
    "KS": {"lat": 38.526600, "lon": -96.726486, "projection_scale": 4},
    "KY": {"lat": 37.668140, "lon": -84.670067, "projection_scale": 4},
    "LA": {"lat": 31.169546, "lon": -91.867805, "projection_scale": 4},
    "ME": {"lat": 44.693947, "lon": -69.381927, "projection_scale": 5},
    "MD": {"lat": 39.063946, "lon": -76.802101, "projection_scale": 5},
    "MA": {"lat": 42.230171, "lon": -71.530106, "projection_scale": 5.5},
    "MI": {"lat": 43.326618, "lon": -84.536095, "projection_scale": 4},
    "MN": {"lat": 45.694454, "lon": -93.900192, "projection_scale": 4},
    "MS": {"lat": 32.741646, "lon": -89.678696, "projection_scale": 4},
    "MO": {"lat": 38.456085, "lon": -92.288368, "projection_scale": 4},
    "MT": {"lat": 46.921925, "lon": -110.454353, "projection_scale": 4},
    "NE": {"lat": 41.125370, "lon": -98.268082, "projection_scale": 4},
    "NV": {"lat": 38.313515, "lon": -117.055374, "projection_scale": 4},
    "NH": {"lat": 43.452492, "lon": -71.563896, "projection_scale": 5},
    "NJ": {"lat": 40.298904, "lon": -74.521011, "projection_scale": 5.5},
    "NM": {"lat": 34.840515, "lon": -106.248482, "projection_scale": 4},
    "NY": {"lat": 42.165726, "lon": -74.948051, "projection_scale": 4},
    "NC": {"lat": 35.630066, "lon": -79.806419, "projection_scale": 4},
    "ND": {"lat": 47.528912, "lon": -99.784012, "projection_scale": 4},
    "OH": {"lat": 40.388783, "lon": -82.764915, "projection_scale": 4},
    "OK": {"lat": 35.565342, "lon": -96.928917, "projection_scale": 4},
    "OR": {"lat": 44.572021, "lon": -122.070938, "projection_scale": 4},
    "PA": {"lat": 40.590752, "lon": -77.209755, "projection_scale": 4},
    "RI": {"lat": 41.680893, "lon": -71.511780, "projection_scale": 7},
    "SC": {"lat": 33.856892, "lon": -80.945007, "projection_scale": 4},
    "SD": {"lat": 44.299782, "lon": -99.438828, "projection_scale": 4},
    "TN": {"lat": 35.747845, "lon": -86.692345, "projection_scale": 4},
    "TX": {"lat": 31.054487, "lon": -97.563461, "projection_scale": 3},
    "UT": {"lat": 39.321000, "lon": -111.093731, "projection_scale": 4},
    "VT": {"lat": 44.045876, "lon": -72.710686, "projection_scale": 6},
    "VA": {"lat": 37.769337, "lon": -78.169968, "projection_scale": 4},
    "WA": {"lat": 47.400902, "lon": -121.490494, "projection_scale": 4},
    "WV": {"lat": 38.491226, "lon": -80.954456, "projection_scale": 5},
    "WI": {"lat": 44.268543, "lon": -89.616508, "projection_scale": 4},
    "WY": {"lat": 42.755966, "lon": -107.302490, "projection_scale": 4},
    "DC": {"lat": 38.897438, "lon": -77.026817, "projection_scale": 7}
}

# Streamlit UI
st.set_page_config(layout="wide")
st.title("LDS Membership and Congregation Change by County (2010–2020)")

# Sidebar
state = st.sidebar.selectbox("Select a state to focus", ["US Overall"] + list(state_zoom_settings.keys()))
color_range = st.sidebar.selectbox("Select color range (+/-)", [1, 5, 10, 100, 1000, 5000, 10000], index=4)

# Top metrics
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

if state == "US Overall":
    df_filtered = data
else:
    df_filtered = data[data['state_abbr'] == state]

# Aggregate metrics
col1.metric(f"{state} Membership 2010", value=f"{int(df_filtered['LDSADH'].sum()):,}")
col2.metric(f"{state} Membership 2020", value=f"{int(df_filtered['LDSADH_2020'].sum()):,}")
col3.metric(f"{state} Congregations 2010", value=f"{int(df_filtered['LDSCNG'].sum()):,}")
col4.metric(f"{state} Congregations 2020", value=f"{int(df_filtered['LDSCNG_2020'].sum()):,}")

member_delta = df_filtered['LDSADH_2020'].sum() - df_filtered['LDSADH'].sum()
cong_delta = df_filtered['LDSCNG_2020'].sum() - df_filtered['LDSCNG'].sum()
member_pct = (member_delta / df_filtered['LDSADH'].sum()) * 100 if df_filtered['LDSADH'].sum() != 0 else 0
cong_pct = (cong_delta / df_filtered['LDSCNG'].sum()) * 100 if df_filtered['LDSCNG'].sum() != 0 else 0

col5.metric(f"{state} Membership Change", f"{int(member_delta):,}" if member_delta < 0 else f"+{int(member_delta):,}")
col6.metric(f"{state} % Membership Change", f"{member_pct:.2f}%" if member_pct < 0 else f"+{member_pct:.2f}%")
col7.metric(f"{state} Congregation Change", f"{int(cong_delta):,}" if cong_delta < 0 else f"+{int(cong_delta):,}")
col8.metric(f"{state} % Congregation Change", f"{cong_pct:.2f}%" if cong_pct < 0 else f"+{cong_pct:.2f}%")

# Plot selection
y_choice = st.sidebar.selectbox("Select value to plot", [
    "membership_change", "pct_change_lds_filled",
    "LDSADH", "LDSADH_2020",
    "congregation_change", "pct_change_cong_filled",
    "LDSCNG", "LDSCNG_2020"
], format_func=lambda x: {
    "membership_change": "Change in Membership",
    "pct_change_lds_filled": "% Change in Membership",
    "LDSADH": "Membership in 2010",
    "LDSADH_2020": "Membership in 2020",
    "congregation_change": "Change in Congregations",
    "pct_change_cong_filled": "% Change in Congregations",
    "LDSCNG": "Congregations in 2010",
    "LDSCNG_2020": "Congregations in 2020"
}[x])

text_format_dict = {
    "membership_change": "Change in Membership",
    "pct_change_lds_filled": "% Change in Membership",
    "LDSADH": "Membership in 2010",
    "LDSADH_2020": "Membership in 2020",
    "congregation_change": "Change in Congregations",
    "pct_change_cong_filled": "% Change in Congregations",
    "LDSCNG": "Congregations in 2010",
    "LDSCNG_2020": "Congregations in 2020"
}

# Plot map
fig = px.choropleth(
    df_filtered,
    geojson=counties,
    locations='fips_str',
    color=y_choice,
    color_continuous_scale=[[0.0, "darkred"], [0.5, "white"], [1.0, "darkgreen"]],
    range_color=(-color_range, color_range),
    scope="usa",
    labels={y_choice: y_choice.replace("_", " ").title()},
    title=f"{y_choice.replace('_', ' ').title()} by County",
    hover_data={
        'fips_str': False,
        'state_abbr': True,
        'county_name': True,
        'urban_rural_category': True,
        'number_of_members_2010': True,
        'number_of_members_2020': True,
        'membership_change': True,
        'number_of_congregations_2010': True,
        'number_of_congregations_2020': True,
        'congregation_change': True,
    },
)

if state != "US Overall":
    zoom = state_zoom_settings[state]
    fig.update_geos(center={"lat": zoom["lat"], "lon": zoom["lon"]}, projection_scale=zoom["projection_scale"])
else:
    pass

fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    plot_bgcolor="#0f1116",
    paper_bgcolor="#0f1116",
    geo=dict(bgcolor="#0f1116")
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<sub><i>Note: Some counties have only zeros, this is due to the religion census not reporting LDS data for those counties likely because of a very small number of people.</i></sub>", unsafe_allow_html=True)

# Layout the bottom charts in a 2x2 grid
col1, col2 = st.columns(2)
with col1:
    top_growth = df_filtered.sort_values(y_choice, ascending=False).head(10)
    fig_top_bar = px.bar(
        top_growth,
        x="county_name",
        y=y_choice,
        title=f"{state}: Top 10 Counties By {text_format_dict[y_choice]}",
        labels={"county_name": "County", y_choice: text_format_dict[y_choice]},
        color_discrete_sequence=["green"]
    )
    st.plotly_chart(fig_top_bar, use_container_width=True)

with col2:
    bottom_growth = df_filtered.sort_values(y_choice, ascending=True).head(10)
    fig_bottom_bar = px.bar(
        bottom_growth,
        x="county_name",
        y=y_choice,
        title=f"{state}: Bottom 10 Counties By {text_format_dict[y_choice]}",
        labels={"county_name": "County", y_choice: text_format_dict[y_choice]},
        color_discrete_sequence=["red"]
    )
    st.plotly_chart(fig_bottom_bar, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig_hist = px.histogram(
        df_filtered,
        x=y_choice,
        nbins=50,
        title=f"{state}: Distribution of Counties' {text_format_dict[y_choice]}",
        labels={y_choice: text_format_dict[y_choice]},
        color_discrete_sequence=["#888"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col4:
    # Urban-Rural Summary Chart
    if y_choice == 'pct_change_lds_filled':
        adh_2010 = df_filtered.groupby("urban_rural_category")["LDSADH"].sum()
        adh_2020 = df_filtered.groupby("urban_rural_category")["LDSADH_2020"].sum()
        summary_df = ((adh_2020 - adh_2010) / adh_2010 * 100).reset_index(name="pct_change")
        y_display = "pct_change"
        
        fig_urban_rural = px.bar(
            summary_df,
            x="urban_rural_category",
            y=y_display,
            title=f"{state}: {text_format_dict[y_choice]} by Urban/Rural Category",
            labels={"urban_rural_category": "Urban-Rural Category", y_choice: text_format_dict[y_choice]},
            color_discrete_sequence=["#1f77b4"]
        )

    elif y_choice == 'pct_change_cong_filled':
        cng_2010 = df_filtered.groupby("urban_rural_category")["LDSCNG"].sum()
        cng_2020 = df_filtered.groupby("urban_rural_category")["LDSCNG_2020"].sum()
        summary_df = ((cng_2020 - cng_2010) / cng_2010 * 100).reset_index(name="pct_change")
        y_display = "pct_change"
        
        fig_urban_rural = px.bar(
            summary_df,
            x="urban_rural_category",
            y=y_display,
            title=f"{state}: {text_format_dict[y_choice]} by Urban/Rural Category",
            labels={"urban_rural_category": "Urban-Rural Category", y_choice: text_format_dict[y_choice]},
            color_discrete_sequence=["#1f77b4"]
        )

    else:
        summary_df = df_filtered.groupby("urban_rural_category")[y_choice].sum().reset_index()
        y_display = y_choice

        fig_urban_rural = px.bar(
            summary_df,
            x="urban_rural_category",
            y=y_choice,
            title=f"{state}: {text_format_dict[y_choice]} by Urban/Rural Category",
            labels={"urban_rural_category": "Urban-Rural Category", y_choice: text_format_dict[y_choice]},
            color_discrete_sequence=["#1f77b4"]
        )
    st.plotly_chart(fig_urban_rural, use_container_width=True) 

st.caption("Dashboard Created by [Alex](https://alexbass.me/) from [Mormon Metrics](https://mormonmetrics.substack.com/). View source code on [GitHub](https://github.com/acbass49/mormon_metrics_datasets).")
st.caption("Data from the [2010 and 2020 U.S. Religion Census](https://www.usreligioncensus.org/) and the [National Center for Health Statistics](https://www.cdc.gov/nchs/data-analysis-tools/urban-rural.html).")
