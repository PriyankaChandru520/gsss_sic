import pandas as pd

# Load CSV
df = pd.read_csv("orders.csv")


df.columns = df.columns.str.strip()


df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

print("\n--- Initial Info ---")
print(df.info())
print("\nMissing Values:\n", df.isnull().sum())
print("\nSample Data:\n", df.head())


df['CustomerID'].fillna("Unknown", inplace=True)

df['ProductCategory'].fillna("Unknown Category", inplace=True)


df['Price'] = df.groupby('ProductCategory')['Price'].transform(
    lambda x: x.fillna(x.mean())
)


df.drop_duplicates(inplace=True)


df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')


df['TotalAmount'] = df['Quantity'] * df['Price']


category_summary = df.groupby('ProductCategory').agg(
    TotalRevenue=('TotalAmount', 'sum'),
    AverageOrderValue=('TotalAmount', 'mean'),
    OrderCount=('OrderID', 'count')
).reset_index()


top_customers = (
    df.groupby('CustomerID')['TotalAmount']
    .sum()
    .reset_index()
    .sort_values(by='TotalAmount', ascending=False)
    .head(5)
)


summary_stats = pd.DataFrame({
    'Metric': ['TotalOrders', 'TotalRevenue', 'AverageOrderValue', 'UniqueCustomers'],
    'Value': [
        len(df),
        df['TotalAmount'].sum(),
        df['TotalAmount'].mean(),
        df['CustomerID'].nunique()
    ]
})


df.to_csv("cleaned_orders.csv", index=False)
category_summary.to_csv("category_summary.csv", index=False)
top_customers.to_csv("top_customers.csv", index=False)
summary_stats.to_csv("summary_stats.csv", index=False)

print("\n Cleaning & Analysis Complete!")
print("\n--- Category Summary ---\n", category_summary)
print("\n--- Top 5 Customers ---\n", top_customers)
print("\n--- Summary Stats ---\n", summary_stats)
