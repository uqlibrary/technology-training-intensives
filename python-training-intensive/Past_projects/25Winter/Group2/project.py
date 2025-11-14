# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 14:46:00 2025

@author: namuu
"""

import pandas as pd
df=pd.read_csv("Python/data/qld_fuel.csv")

df.columns
df.info()
df.describe()


# picking out individual column
df["Price"]

df["Price"].unique()
df["Price"].describe()

df["Site_Suburb"]
df["Site_Suburb"].unique()
condition=df["Site_Suburb"] =="St Lucia"

sns.catplot(data=df,x="Fuel_Type", y="Price")

#filter out
df.info("X_id")
df["X_id"]

df["Price"] = df["Fuel_Type"].map(Price)

import pandas as pd
df=pd.read_csv("Python/data/qld_fuel.csv")
fp=df["Price"]
ft=df["Fuel_Type"]
ft.describe()
# Count
fp.count() 

#measures of central tendency
fp.mean()
fp.mode()
fp.median()

#measures of variance
fp.min()
fp.max()


import matplotlib.pyplot as plt

# 1. Bar plot (mean price per type)
sns.barplot(data=df, x=ft, y=fp, errorbar=None, width=0.6, palette="muted")

# 2. Rotate x-ticks
plt.xticks(rotation=45, ha='right')

# 3. Title and labels
plt.title("Average Fuel Prices by Type in QLD")
plt.xlabel("Fuel Type")
plt.ylabel("Price ($/L)")

plt.tight_layout()
plt.show()

import pandas as pd
df_raw = pd.read_csv("data/qld_fuel.csv")
df_raw.shape
df_raw.columns
df = df_raw.copy()

df.shape
df_column = df.columns
df_categorical_column = ["Site_Suburb", "Fuel_Type", "Site_Name"]
df_numerical_column = ["Site_Name", "Site_Latitude", "Site_Longtitude", "Price", "X_id"]


df["Price"].max()
df["Price"].min()
df["Price"].mean()
df["Price"].median()
df["Price"].std()
df["Price"].mode()

df.describe()

# remove nulls
df[df["X_id"].notna()]
df_full_X_id = df[df["X_id"].notna()]
df_full_X_id.shape


df["Site_Suburb"].count()
df["Site_Suburb"].unique()
df["Site_Suburb"].value_counts()

df["Fuel_Type"].count()
df["Fuel_Type"].unique()
df["Fuel_Type"].value_counts()

# from GPT
df["TransactionDateutc"] = pd.to_datetime(df["TransactionDateutc"])
df["date_only"] = df["TransactionDateutc"].dt.date



# subset
gb = df.groupby("date_only")
avg_price_by_date = gb["Price"].agg("mean").reset_index()
avg_price_by_date.to_csv("data/avg_price_by_date.csv")  # export subset

df["TransactionDateutc"].dtypes

df["year_month"] = df["TransactionDateutc"].dt.to_period("M")
gb_year_month = df.groupby("year_month")
avg_price_by_year_month = gb_year_month["Price"].agg("mean").reset_index()
avg_price_by_year_month.to_csv("data/avg_price_by_year_month.csv")
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt



type("year_month")
type("date_only")

avg_price_by_year_month["year_month"] = avg_price_by_year_month["year_month"].dt.to_timestamp()
sns.relplot(data = avg_price_by_date, x = "date_only", y = "Price", hue = "Price")
sns.lineplot(data =avg_price_by_year_month, x = "year_month", y = "Price", color = "red")

Fuel price variability across suburbs in Queensland 
import pandas as pd 
import seaborn as sns
import matplotlib. pyplot as plt


df = pd.read_csv("qld_fuel.csv")
df["TransactionDateutc"] = pd.to_datetime(df["TransactionDateutc"])
df["Price"] = df["Price"] / 100 

# removing outliers 
df = df[df["Price"] < 50] 
df = df[df["Price"] > 10] 

# summary stats 
summary_stats = df.groupby("Site_Suburb")["Price"].agg(min_price = "min", max_price = "max")

summary_stats["price_range"] = summary_stats["max_price"] - summary_stats["min_price"]

# Top 3 and bottom 3 suburbs 

top3_change = summary_stats.sort_values(by="price_range", ascending= False). head(3)
bottom3_change = summary_stats.sort_values(by="price_range", ascending= True). head(3)

selected_suburbs = top3_change.index.tolist() + bottom3_change.index.tolist()
df_selected = df[df["Site_Suburb"].isin(selected_suburbs)]

df_selected["Site_Suburb"] = df_selected["Site_Suburb"].str.strip().str.title()

# Plot
sns.catplot(data = df_selected, x = "Site_Suburb", y = "Price", kind = "box")
plt.xlabel ("Site_Suburb")
plt.ylabel ("Price")
plt.savefig ("tb.png")
plt.show()

