import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    dataframe = get_dataframe("Business_sales_EDA.csv")
    dataframe = clean_dataframe(dataframe)
    #calculate_mean_sales_promotion(dataframe)
    #calculate_mean_product_position(dataframe)
    #print("diferencia entre ventas promocionales y no promocionales: ", dataframe[dataframe["Promotion"] == "Yes"]["Sales Volume"].mean() - dataframe[dataframe["Promotion"] == "No"]["Sales Volume"].mean())
    #scatter_plot_price_salesVolume(dataframe)
    #top5_terms_by_sales(dataframe)
    #best_selling_promo(dataframe)
    #best_selling_by_material(dataframe)
    #print(dataframe["price"].corr(dataframe["Sales Volume"])) #Elasticidad precio-ventas 
    #best_selling_by_seasonality(dataframe)
    #correlation_terms(dataframe)
    # revenue_analysis(dataframe)
    highest_cost_revenue_products(dataframe)


def get_dataframe(file_path): 
    return pd.read_csv(file_path, sep=";")

def clean_dataframe(dataframe):
    # Remove leading/trailing whitespace from column names  
    dataframe.columns = dataframe.columns.str.strip()
    
   # change Seasonal values from Yes/No to 1/0
    dataframe["Seasonal"] = dataframe["Seasonal"].apply(lambda x: 1 if str(x).strip().capitalize() == "Yes" else 0)
    # change sales volume and price to numeric values
    dataframe["Sales Volume"] = dataframe["Sales Volume"].astype(int)
    dataframe["price"] = dataframe["price"].astype(float)
    #clean Promotion column by stripping whitespace
    dataframe["Promotion"] = dataframe["Promotion"].str.strip()
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
    print("Correlation Price vs Sales:", dataframe["price"].corr(dataframe["Sales Volume"]))
    plt.scatter(dataframe["price"], dataframe["Sales Volume"])
    plt.title("Price vs Sales Volume")
    plt.xlabel("Price")
    plt.ylabel("Sales Volume")
    plt.show()

def  top5_terms_by_sales(dataframe):
    top5 = dataframe.groupby("terms")["Sales Volume"].sum().sort_values(ascending=False).head(5) #group by terms, sum sales volume, sort descending and get top 5
    return top5

def  best_selling_promo(dataframe):
    best_selling_promo = dataframe[dataframe["Promotion"] == "Yes"].groupby("terms")["Sales Volume"].sum().sort_values(ascending=False).head() #filter promotional products first, then group by terms, sum sales volume, sort descending
    print("Best selling promotional products:")
    print(best_selling_promo)

def best_selling_by_material(dataframe):
    best_selling_material = dataframe.groupby("material")["Sales Volume"].sum().sort_values(ascending=False).head() #group by Material, sum sales volume, sort descending 
    print("Best selling products by material:")
    print(best_selling_material)

def best_selling_by_seasonality(dataframe):
  
    # Calculate total sales for seasonal vs non-seasonal products
    seasonal_sales = dataframe[dataframe["Seasonal"] == 1]["Sales Volume"].sum()
    non_seasonal_sales = dataframe[dataframe["Seasonal"] == 0]["Sales Volume"].sum()
    
    # Create a bar chart to compare sales
    categories = ['Seasonal Products', 'Non-Seasonal Products']
    sales = [seasonal_sales, non_seasonal_sales]
    
    plt.figure(figsize=(8, 5))
    plt.bar(categories, sales, color=['skyblue', 'lightcoral'])
    plt.title('Total Sales Volume: Seasonal vs Non-Seasonal Products')
    plt.ylabel('Total Sales Volume')
    plt.xlabel('Product Type')
    for i, v in enumerate(sales):
        plt.text(i, v + max(sales)*0.01, str(v), ha='center', va='bottom')
    plt.show()

    #correlacion entre price y sales per terms for each term, to see if there is a relationship between price and sales volume for different terms
def correlation_terms(dataframe):
    terms = dataframe["terms"].unique()
    correlations = {}
    
    for term in terms:
        term_data = dataframe[dataframe["terms"] == term]
        correlation = term_data["price"].corr(term_data["Sales Volume"])
        correlations[term] = correlation
    
    print("Correlation between Price and Sales Volume for each Term:")
    for term, corr in correlations.items():
        print(f"{term}: {corr:.2f}")

#Revenue Analysis: Calculate total revenue for each term and identify which terms generate the most revenue. This can help in understanding which product categories are most profitable.
def revenue_analysis(dataframe):
    dataframe["Revenue"] = dataframe["price"] * dataframe["Sales Volume"]
    revenue_by_term = dataframe.groupby("terms")["Revenue"].sum().sort_values(ascending=False)
    print("Total Revenue by Term:")
    print(revenue_by_term)
    #promo vs non promo revenue
    promo_revenue = dataframe[dataframe["Promotion"] == "Yes"]["Revenue"].sum()
    non_promo_revenue = dataframe[dataframe["Promotion"] == "No"]["Revenue"].sum()
    print(f"Total Revenue from Promotional Products: {promo_revenue:.2f}")
    print(f"Total Revenue from Non-Promotional Products: {non_promo_revenue:.2f}")
    #sales volumen promo vs non promo sales volume
    promo_sales_volume = dataframe[dataframe["Promotion"] == "Yes"]["Sales Volume"].sum()
    non_promo_sales_volume = dataframe[dataframe["Promotion"] == "No"]["Sales Volume"].sum()
    print(f"Total Sales Volume from Promotional Products: {promo_sales_volume}")
    print(f"Total Sales Volume from Non-Promotional Products: {non_promo_sales_volume}")

def highest_cost_revenue_products(dataframe):
    # define a mask for high‑cost items (price in the top quartile)
    price_threshold = dataframe["price"].quantile(0.75)
    high_cost_mask = dataframe["price"] >= price_threshold
    low_cost_mask = dataframe["price"] < price_threshold
    # compute full revenue column once (price * quantity)
    dataframe["Revenue"] = dataframe["price"] * dataframe["Sales Volume"]
    
    # totals for the filtered subset (not just the head)
    total_revenue_high = dataframe.loc[high_cost_mask, "Revenue"].sum()
    total_sales_high = dataframe.loc[high_cost_mask, "Sales Volume"].sum()
    total_revenue_low = dataframe.loc[low_cost_mask, "Revenue"].sum()
    total_sales_low = dataframe.loc[low_cost_mask, "Sales Volume"].sum()
    print("Total Revenue from High-Cost Products:", total_revenue_high)
    print("Total Sales Volume from High-Cost Products:", total_sales_high)
    print("\n")
    print("Total Revenue from Low-Cost Products:", total_revenue_low)
    print("Total Sales Volume from Low-Cost Products:", total_sales_low)

if __name__ == "__main__":
    main()
