from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    r2_score,
)
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pathlib import Path
import os
import duckdb
import plotly.express as px

# Hjälp rekryterare som jobbar med de specifika occupation_fields genom att skapa en dashboard.
## Metrics:
# 1. totalt antal lediga jobb. 2 totalt antal städer. #3. TOP 3: yrken med mest lediga jobb. 4. TOP 3 regioner med mest lediga jobb  något mer?
# vilket yrke har högst andel lediga jobb? linjediagram med en linje per yrke
# vilken stad har högst andel lediga jobb? linjediagram med en linje per yrke

## Sålla per yrkesgrupp (occ_field eller df:arna):
# vilken arbetsgivare har högst andel lediga jobb? barchart
# vilken yrkesgrupp har högst andel lediga jobb? occ_group      barchart
# andel jobb som kräver körkort + egen bil + erfarenhet

# avancerat: hur lång är application_deadline i snitt? Vilken stad har störst variation av yrken? Vilka kommuner erbjuder heltid oftast?
# diagram för region så det är sveriges karta
from kpi import (
    top_occupations,
    vacancies_by_group,
    top_municipalitys,
    attributes_per_field,
)
from chart import chart_top_occupations, pie_chart

# def show_metrics(df:pd.DataFrame, metric_labels:str, metric_kpis:str, metric_amount:int):
#     """Function for generating metrics

#     Args:
#         df (dataframe): dataframe to filter metrics from
#         metric_labels (str): string for metric labels using df["metric_labels"] to filter out label values from df
#         metric_kpis (str): string for metric kpis using df["metric_kpis"] to filter out kpi values from df
#         metric_amount (int): integer for amount of metric columns to use
#     """
#     labels = df[metric_labels].head(metric_amount)
#     cols = st.columns(metric_amount)
#     kpis = df[metric_kpis].head(metric_amount)


#     for col, label, kpi in zip(cols, labels, kpis):
#         with col:
#             st.metric(label=label, value=kpi)
def show_metric(labels, cols, kpis):
    for label, col, kpi in zip(labels, cols, kpis):
        with col:
            st.metric(label=label, value=kpi)


def layout():
    total_citys = df_mart["municipality"].nunique()
    total_vacancies = df_total_vacancies["total_vacancies"].sum()
    st.markdown("# Job Ads Dashboard")
    # Total layout for sweden:
    st.write(
        "En Dashboard för att hjälpa rekryterare som jobbar med specifika yrkesgrupper att få en bra översikt över arbetsmarknaden just nu."
    )

    labels = ["Totalt antal lediga jobb", "Totalt antal städer"]
    cols = st.columns(2)
    kpis = round(total_vacancies), total_citys
    show_metric(labels, cols, kpis)

    st.markdown("### Lediga jobb i:")
    labels = top_occupations()
    cols = st.columns(3)
    kpis = vacancies_by_group()
    show_metric(labels, cols, kpis)

    st.plotly_chart(pie_chart())

    st.markdown("### Finsortera på yrkesgrupp och kommun/yrke:")
    field = st.selectbox(" Select your field ", top_occupations())
    sort_on = st.selectbox("Sort on", ["municipality", "occupation"])
    fig = chart_top_occupations(field, sort_on)
    st.plotly_chart(fig)
    ## Efter sortering på yrkesgrupp, visa hur många jobb som kräver attributes
    st.markdown(f"### Antal jobb för grupp {field} som kräver:")  # TODO gör i procent?
    labels = ["Erfarenhet", "Körkort", "Tillgång till egen bil"]
    cols = st.columns(3)
    kpis = attributes_per_field(field)
    show_metric(labels, cols, kpis)

    
    # city_1, city_2, city_3, city_4, city_5, vac_1, vac_2, vac_3, vac_4, vac_5 = (
    #     top_municipalitys()
    # )

    # labels = [city_1, city_2, city_3, city_4, city_5]
    # kpis = [vac_1, vac_2, vac_3, vac_4, vac_5]  # jobb per kommun
    # cols = st.columns(5)
    # for label, col, kpi in zip(labels, cols, kpis):
    #     with col:
    #         st.metric(label=label, value=kpi)


if __name__ == "__main__":
    # working_directory = Path(__file__).parents[1]
    # os.chdir(working_directory)
    with duckdb.connect("../ads_data_warehouse.duckdb") as connection:
        df_mart = connection.execute("SELECT * FROM mart.mart_ads").df()
        df_education = connection.execute("SELECT * FROM mart.mart_pedagogik").df()
        df_healthcare = connection.execute("SELECT * FROM mart.mart_sjukvård").df()
        df_technical = connection.execute("SELECT * FROM mart.mart_teknisk").df()
        df_total_vacancies = connection.execute(
            "SELECT * FROM mart.mart_total_vacancies"
        ).df()

    layout()

    # city = "workplace_municipality"
    # occupation = "occupation"
    # df_test = vacancies(df_technical, city)
    # x_input = st.selectbox("Select x value", ["workplace_municipality", "city"])
    # y_input = st.selectbox("Select y value", ["vacancies"])
    # fig1 = px.bar(df_ads, x=x_input, y=y_input)
    # st.plotly_chart(fig1)
