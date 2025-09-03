from flask import Flask, render_template
import pandas as pd
import plotly
import plotly.express as px
import json

app = Flask(__name__)

# ---------------------------
# Load and clean the data
# ---------------------------
df = pd.read_csv("orders.csv")

# Strip whitespace from columns and string values
df.columns = df.columns.str.strip()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Fill missing CustomerID and ProductCategory
df['CustomerID'] = df['CustomerID'].fillna("Unknown")
df['ProductCategory'] = df['ProductCategory'].fillna("Unknown Category")

# Fill missing Price per ProductCategory
df['Price'] = df.groupby('ProductCategory')['Price'].transform(lambda x: x.fillna(x.mean()))

# Drop duplicates
df = df.drop_duplicates()

# Convert OrderDate to datetime
df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

# Calculate TotalAmount
df['TotalAmount'] = df['Quantity'] * df['Price']

# ---------------------------
# Create summaries
# ---------------------------
# Filter out "Unknown Category" before generating the summary
df_filtered = df[df['ProductCategory'] != 'Unknown Category']
category_summary = (
    df_filtered.groupby('ProductCategory')
    .agg(
        TotalRevenue=('TotalAmount', 'sum'),
        AverageOrderValue=('TotalAmount', 'mean'),
        OrderCount=('OrderID', 'count')
    )
    .reset_index()
)

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

# ---------------------------
# Create Plotly chart
# ---------------------------
fig_category = px.bar(
    category_summary,
    x='ProductCategory',
    y='TotalRevenue',
    title='Total Revenue by Product Category',
    text='TotalRevenue'
)
fig_category.update_traces(texttemplate='%{text:.2f}', textposition='outside')
graphJSON = json.dumps(fig_category, cls=plotly.utils.PlotlyJSONEncoder)

# ---------------------------
# Flask route
# ---------------------------
@app.route('/')
def index():
    return render_template(
        'dashboard.html',
        tables={
            'Summary Stats': summary_stats.to_html(classes='table table-bordered', index=False),
            'Category Summary': category_summary.to_html(classes='table table-bordered', index=False),
            'Top Customers': top_customers.to_html(classes='table table-bordered', index=False)
        },
        graphJSON=graphJSON
    )

if __name__ == '__main__':
    app.run(debug=True)