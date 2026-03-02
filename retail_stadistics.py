import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    dataframe = get_dataframe("Business_sales_EDA.csv")
    dataframe = clean_dataframe(dataframe)
    calculate_mean_sales_promotion(dataframe)
    calculate_mean_product_position(dataframe)
    print("diferencia entre ventas promocionales y no promocionales: ", dataframe[dataframe["Promotion"] == "Yes"]["Sales Volume"].mean() - dataframe[dataframe["Promotion"] == "No"]["Sales Volume"].mean())
    scatter_plot_price_salesVolume(dataframe)
    

def get_dataframe(file_path): 
    return pd.read_csv(file_path, sep=";")

def clean_dataframe(dataframe):
    # Remove leading/trailing whitespace from column names  
    dataframe.columns = dataframe.columns.str.strip()
    
   # change Seasonal values from Yes/No to 1/0
    dataframe["Seasonal"] = dataframe["Seasonal"].apply(lambda x: 1 if str(x).strip().capitalize() == "Yes" else 0)
   #check null values
    dataframe = dataframe.dropna()
    return dataframe

def calculate_mean_sales_promotion(dataframe):
    # Calculate means of total sales for promotional and non-promotional products
    promotion_sales = dataframe[dataframe["Promotion"] == "Yes"]["Sales Volume"].mean()
    non_promotion_sales = dataframe[dataframe["Promotion"] == "No"]["Sales Volume"].mean()
    print(f"Mean Sales Volume for Promotional Products: {promotion_sales.round(2)}")
    print(f"Mean Sales Volume for Non-Promotional Products: {non_promotion_sales.round(2)}")

def calculate_mean_product_position(dataframe): #Considering just Aisle vs Endcap
    # Calculate means of total sales for products in Aisle and Endcap positions
    aisle_sales = dataframe[dataframe["Product Position"] == "Aisle"]["Sales Volume"].mean()
    endcap_sales = dataframe[dataframe["Product Position"] == "End-cap"]["Sales Volume"].mean()
    print(f"Mean Sales Volume for Products in Aisle: {aisle_sales.round(2)}")
    print(f"Mean Sales Volume for Products in Endcap: {endcap_sales.round(2)}")

def scatter_plot_price_salesVolume(dataframe):
    plt.scatter(dataframe["price"], dataframe["Sales Volume"])
    plt.title("Price vs Sales Volume")
    plt.xlabel("Price")
    plt.ylabel("Sales Volume")
    plt.show()

if __name__ == "__main__":
    main()
