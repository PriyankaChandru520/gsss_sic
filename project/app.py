from flask import Flask, render_template, send_file
import subprocess
import pandas as pd

app = Flask(__name__)

@app.route('/')
def show_csvs():
    # 1️ Run mcode.py
    try:
        subprocess.run(["python", "mcode.py"], check=True)
    except subprocess.CalledProcessError as e:
        return f"<pre>Error running script:\n{e}</pre>"

    # 2️ Load CSVs
    try:
        category_summary = pd.read_csv("category_summary.csv")
        top_customers = pd.read_csv("top_customers.csv")
        summary_stats = pd.read_csv("summary_stats.csv")
    except FileNotFoundError:
        return "<h3>CSV file not found. Did mcode.py run successfully?</h3>"

    # 3️ Format numbers (2 decimal places where applicable)
    def format_numbers(df):
        return df.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)

    category_summary = format_numbers(category_summary)
    top_customers = format_numbers(top_customers)
    summary_stats = format_numbers(summary_stats)

    # 4️ Convert to HTML tables with Bootstrap styling
    table_classes = "table table-striped table-hover align-middle text-center"
    category_table = category_summary.to_html(classes=table_classes, index=False, border=0)
    top_customers_table = top_customers.to_html(classes=table_classes, index=False, border=0)
    summary_stats_table = summary_stats.to_html(classes=table_classes, index=False, border=0)

    return render_template("index.html",
                           category_table=category_table,
                           top_customers_table=top_customers_table,
                           summary_stats_table=summary_stats_table)

# Download routes
@app.route('/download/category')
def download_category():
    return send_file("category_summary.csv", as_attachment=True)

@app.route('/download/customers')
def download_customers():
    return send_file("top_customers.csv", as_attachment=True)

@app.route('/download/stats')
def download_stats():
    return send_file("summary_stats.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
