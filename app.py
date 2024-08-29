import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# Set up the page config
st.set_page_config(page_title="TechCorp", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        body {background-color: #1E1E1E;}
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
            color: white;
        }
        .kpi-box {
            background-color: #4A4A4A;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            color: #FFFFFF;
            font-size: 16px;
            margin-bottom: 15px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            position: relative; /* To contain pseudo-elements */
        }
        .kpi-box h3 {
            font-size: 18px;
            margin-bottom: 2px; /* Reduce space between title and value */
            color: #EEEEEE;
            text-align: center; /* Centering the heading text */
        }
        .kpi-box p {
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
            text-align: center; /* Centering the main value text */
            margin: 0; /* Removing margin to reduce space */
        }
        .kpi-box span {
            font-size: 16px;
            text-align: center; /* Centering the arrow and percentage change */
            display: block; /* Ensures it behaves correctly when centered */
            margin: 0; /* Removing margin to avoid alignment issues */
        }
        .kpi-box a {
            display: none; /* Hides any links that might be inadvertently displayed */
        }
        .arrow-up {
            color: #00CC44; /* Green for positive change */
            font-weight: bold;
        }
        .arrow-down {
            color: #CC0000; /* Red for negative change */
            font-weight: bold;
        }
        .stPlotlyChart {
            margin-left: auto;
            margin-right: auto;
        }
        .stTable {
            margin-left: auto;
            margin-right: auto;
        }
        .centered {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)



# Fake company name
st.title("Data Analysis Dashboard")
st.write("Welcome to the data analysis dashboard of TechCorp Solutions. Upload your data, visualize it, and perform various analyses.")

# Set default data if no file is uploaded
uploaded_file = None
df = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'Sales': np.random.randint(20000, 50000, size=12),
    'Expenses': np.random.randint(15000, 30000, size=12)
})

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# Allow users to download their data as an Excel file
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer._save()
    processed_data = output.getvalue()
    return processed_data

df_xlsx = to_excel(df)

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")
st.sidebar.selectbox("Time Granularity", ["Monthly", "Quarterly", "Yearly"], index=0)
if st.sidebar.button('Run Analysis'):
    st.write("Analysis launched!")
if st.sidebar.button('Generate Report'):
    st.write("Report generated!")
if st.sidebar.button('Reset Configuration'):
    st.write("Configuration reset!")

st.sidebar.header("Advanced Configuration")
data_retention_period = st.sidebar.slider("Data Retention Period (months)", 1, 12, 6)
report_frequency = st.sidebar.slider("Report Frequency (days)", 1, 30, 7)
notification_preference = st.sidebar.selectbox("Notification Preference", ["Email", "SMS", "None"])

# File uploader at the bottom of the sidebar
st.sidebar.header("")
st.sidebar.header("📀 Upload Data")
uploaded_file = st.sidebar.file_uploader("", type="csv", key="uploader1")

# Layout: Graph on top left, KPIs on top right, and table at the bottom
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Sales and Expenses Trend")
    
    months = df['Month']
    sales = df['Sales']
    expenses = df['Expenses']
    
    fig = px.line(title="")
    fig.add_scatter(x=months, y=sales, mode='lines+markers', name='Sales', line=dict(color='#636EFA'))
    fig.add_scatter(x=months, y=expenses, mode='lines+markers', name='Expenses', line=dict(color='#EF553B'))
    st.plotly_chart(fig)

# Calculate KPIs
total_sales = sales.sum()
total_expenses = expenses.sum()
profit = total_sales - total_expenses

# Assuming we have data from the previous year for comparison
previous_sales = total_sales * np.random.uniform(0.8, 1.2)
previous_expenses = total_expenses * np.random.uniform(0.8, 1.2)
previous_profit = previous_sales - previous_expenses

sales_change = ((total_sales - previous_sales) / previous_sales) * 100
expenses_change = ((total_expenses - previous_expenses) / previous_expenses) * 100
profit_change = ((profit - previous_profit) / previous_profit) * 100

# Add colorful arrows based on performance
sales_arrow = "▲" if sales_change > 0 else "▼"
expenses_arrow = "▲" if expenses_change > 0 else "▼"
profit_arrow = "▲" if profit_change > 0 else "▼"

sales_color = "arrow-up" if sales_change > 0 else "arrow-down"
expenses_color = "arrow-up" if expenses_change > 0 else "arrow-down"
profit_color = "arrow-up" if profit_change > 0 else "arrow-down"

with col2:
    st.subheader("")
    st.markdown(f"""
        <div class="kpi-box">
            <h2>Total Sales</h2>
            <p>${total_sales:,}</p>
            <span class="{sales_color}">{sales_arrow} {sales_change:.2f}%</span>
        </div>
        <div class="kpi-box">
            <h2>Total Expenses</h2>
            <p>${total_expenses:,}</p>
            <span class="{expenses_color}">{expenses_arrow} {expenses_change:.2f}%</span>
        </div>
        <div class="kpi-box">
            <h2>Profit</h2>
            <p>${profit:,}</p>
            <span class="{profit_color}">{profit_arrow} {profit_change:.2f}%</span>
        </div>
    """, unsafe_allow_html=True)

st.subheader("Sales and Expenses Data")
st.table(df)

# Fake button to send report
if st.button('Send report to stakeholders'):
    st.write("Report sent to stakeholder successfully!")

st.markdown("<div style='text-align: center; margin-top: 50px;'>© 2024 Made by Yoluko Solutions - Alexandre Kocev</div>", unsafe_allow_html=True)




