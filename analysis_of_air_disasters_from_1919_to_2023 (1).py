# -*- coding: utf-8 -*-
"""Analysis of air disasters from 1919 to 2023.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13TAKwnDuIsvQ0ZOnr2osoTBvP3Yr7o8N

# Analysis of air disasters from 1919 to 2023
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

accidents = pd.read_csv("https://proai-datasets.s3.eu-west-3.amazonaws.com/aviation-accidents.csv", sep = ',', encoding='utf-8')

accidents.info()
accidents.describe()

"""### Cleaning the data and correcting any errors within the dataset"""

def clean_data(accidents):

    accidents['operator'] = accidents['operator'].apply(lambda x: str(x).encode('latin1', 'ignore').decode('utf-8', 'ignore'))
    accidents['location'] = accidents['location'].str.strip(" ,.?")

    return accidents

accidents.loc[accidents["year"] == "unknown", "year"] = None
accidents.loc[accidents["country"] == "Unknown country", "country"] = None
accidents['fatalities'] = pd.to_numeric(accidents['fatalities'], errors='coerce')
accidents['fatalities'] = accidents['fatalities'].fillna(0)
accidents = accidents.dropna(subset=['fatalities'])

accidents['date'] = pd.to_datetime(accidents['date'], format='%d-%b-%Y', errors='coerce')
accidents.dropna(subset=['date'], inplace = True)

accidents["year"] = accidents["year"].astype(int)

accidents.info()

"""### From the graph it can be observed that the country in which the most accidents have occurred is the USA"""

accidents_country = accidents["country"].value_counts().head(10)
plt.figure(figsize=(10, 6))
accidents_country.plot(kind='bar', color='skyblue')
plt.title('Top 10 countries with the highest number of accidents')
plt.xlabel('Country')
plt.ylabel('Number of accidents')
plt.xticks(rotation=45)
plt.show()

"""### The day of the week in which the most accidents occur is Friday"""

accidents["day_of_week"] = accidents["date"].dt.day_name()

accidents_by_day = accidents["day_of_week"].value_counts()

plt.figure(figsize=(10, 6))
accidents_by_day.plot(kind="bar", color="lightgreen")
plt.title("Accidents by day of the weeka")
plt.xlabel("Day of the week")
plt.ylabel("Number of accidents")
plt.style.use('ggplot')
plt.xticks(rotation=45)
plt.show()

"""### These are the safest operators, based on the number of accidents"""

safe_operators = accidents[["fatalities", "operator"]].groupby(["operator"]).sum()
safe_operators

pd.Series(accidents["operator"].unique()).sort_values()

"""### The vehicle that caused the most deaths is Douglas C-47A (DC-3)"""

total_victims_by_type = accidents ["type"].value_counts().head(10)
plt.figure(figsize=(10, 6))
total_victims_by_type.plot(kind='bar', color='blue')

plt.title('Total number of victims by type of accident')
plt.xlabel('Type of accident')
plt.ylabel('Total number of victims')
plt.show()

"""### After September 11th the number of accidents decreased, but we can see that the period in which there were more accidents was 1940-1945, due to the world conflict."""

accidents_before_11_september = accidents[accidents['date'] < '2001-09-11']
accidents_after_11_september = accidents[accidents['date'] >= '2001-09-11']

accidents_first_by_year = accidents_before_11_september.groupby(accidents_before_11_september['date'].dt.year).size()
accidents_after_by_year = accidents_after_11_september.groupby(accidents_after_11_september['date'].dt.year).size()

plt.figure(figsize=(10, 6))

plt.plot(accidents_first_by_year.index, accidents_first_by_year.values, color='red', label="Before")
plt.plot(accidents_after_by_year.index, accidents_after_by_year.values, color='green', label="After")

plt.title("Number of incidents before and after September 11, 2001")
plt.xlabel("Year")
plt.ylabel("Number of accidents")

plt.legend()
plt.grid(True)

plt.annotate('September 11, 2001', xy=(2001, accidents_first_by_year.loc[2001]), xytext=(2002, 300),
             arrowprops=dict(facecolor='black'))

plt.show()

"""### Number of accidents by country"""

import plotly.express as px

accidents_by_country = accidents['country'].value_counts().reset_index()
accidents_by_country.columns = ['country', 'accidents']

fig = px.choropleth(accidents_by_country,
                    locations='country',
                    locationmode='country names',
                    color='accidents',
                    hover_name='country',
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title='Number of accidents by country')
fig.show()

"""In conclusion, the analysis of aviation disasters from 1919 to 2023 allowed us to obtain a detailed overview of aviation safety. By identifying the country where the most accidents occur, the temporal trends and the
Safer and non-safer airline operators.
"""