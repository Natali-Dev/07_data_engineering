import duckdb
import os 
from pathlib import Path
# from dash import df_mart, df_total_vacancies

# working_directory = Path(__file__).parents[1]
# os.chdir(working_directory)
with duckdb.connect("../ads_data_warehouse.duckdb") as connection:
    df_mart = connection.execute("SELECT * FROM mart.mart_ads").df()
    df_education = connection.execute("SELECT * FROM mart.mart_pedagogik").df()
    df_healthcare = connection.execute("SELECT * FROM mart.mart_sjukvård").df()
    df_technical = connection.execute("SELECT * FROM mart.mart_teknisk").df()
    df_total_vacancies = connection.execute("SELECT * FROM mart.mart_total_vacancies").df()
    
#1. totalt antal lediga jobb. # totalt antal städer. 



# 2.TOP 3: yrkesgrupper med mest lediga jobb. TOP 3 kommuner med mest lediga jobb 
def top_occupations():
    top_occupation = df_mart.groupby("occupation_field")["vacancies"].sum().sort_values(ascending=False).reset_index().head(5)
    occ_1 = top_occupation["occupation_field"][0]
    occ_2 = top_occupation["occupation_field"][1]
    occ_3 = top_occupation["occupation_field"][2]
    occ_4 = "Alla"
    # occ_4 = top_occupation["occupation"][3]
    # occ_5 = top_occupation["occupation"][4]
    
    return occ_1, occ_2, occ_3, occ_4 #,occ_5

def vacancies_by_group():
    top_field = df_mart.groupby("occupation_field")["vacancies"].sum().sort_values(ascending=False).reset_index().head(5)
    city_1 = top_field["vacancies"][0]
    city_2 = top_field["vacancies"][1]
    city_3 = top_field["vacancies"][2]
    # city_4 = top_municipality["workplace_municipality"][3]
    # city_5 = top_municipality["workplace_municipality"][4]
    return city_1 ,city_2, city_3, #city_4, city_5

def top_municipalitys():
    top_municipality = df_mart.groupby("municipality")["vacancies"].sum().sort_values(ascending=False).reset_index().head(5)
    city_1 = top_municipality["municipality"][0]
    city_2 = top_municipality["municipality"][1]
    city_3 = top_municipality["municipality"][2]
    city_4 = top_municipality["municipality"][3]
    city_5 = top_municipality["municipality"][4]
    
    
    vac_1 = top_municipality["vacancies"][0]
    vac_2 = top_municipality["vacancies"][1]
    vac_3 = top_municipality["vacancies"][2]
    vac_4 = top_municipality["vacancies"][3]
    vac_5 = top_municipality["vacancies"][4]
    return city_1 ,city_2, city_3,city_4,city_5, vac_1, vac_2, vac_3, vac_4, vac_5

def attributes_per_field (field): 
    if field == "Alla": 
        df_attributes = df_mart[["experience_required", "driver_licence", "access_to_own_car"]].sum()
        experience = df_attributes["experience_required"]
        licence = df_attributes["driver_licence"]
        car = df_attributes["access_to_own_car"]
    else:
        df = df_mart[df_mart["occupation_field"] == field]
        df_attributes = df.groupby("occupation_field")[["experience_required", "driver_licence", "access_to_own_car"]].sum().reset_index()
        experience = df_attributes["experience_required"]
        licence = df_attributes["driver_licence"]
        car = df_attributes["access_to_own_car"]
    
    return experience, licence, car