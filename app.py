import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Sales Intelligence",
    page_icon="📊",
    layout="wide"
)

# ---------- SAMPLE DATA ----------
@st.cache_data
def load_data():
    data = {
        "Order Date": pd.date_range("2025-01-01", periods=120, freq="3D"),
        "Order ID": [f"ORD-{1001+i}" for i in range(120)],
        "Customer Name": [f"Customer {i+1}" for i in range(120)],
        "City": ["New York", "Los Angeles", "Chicago", "Houston", "Seattle"] * 24,
        "Region": ["East", "West", "Central", "South", "West"] * 24,
        "Product": ["Laptop", "Monitor", "Keyboard", "Mouse", "Tablet"] * 24,
        "Category": ["Technology", "Accessories", "Accessories",
                     "Accessories", "Technology"] * 24,
        "Quantity": [(i % 8) + 1 for i in range(120)],
        "Sales": [((i % 10) + 1) * 125 for i in range(120)],
        "Profit": [((i % 10) + 1) * 25 for i in range(120)]
    }
    return pd.DataFrame(data)

df = load_data()

# ---------- PREMIUM DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #081426, #10243D);
    color: #F1F5F9;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3, p, label {
    color: #F1F5F9 !important;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #173B5E, #125B70);
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #287D91;
    box-shadow: 0 5px 18px rgba(0,0,0,0.25);
}
[data-testid="stMetricLabel"] {
    color: #B8DCE8 !important;
}
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] {
    background: #0B1B30;
    border-right: 1px solid #23415E;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #287D91;
    border-radius: 10px;
}/* Professional white sidebar selection boxes */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #B8C9D9 !important;
    border-radius: 8px !important;
    color: #17365E !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #17365E !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #E6F0F7 !important;
    color: #17365E !important;
    border: 1px solid #C5D8E8 !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
    fill: #17365E !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("# 🌐 GLOBAL SALES INTELLIGENCE")
st.markdown("### International Business Performance | 2025")
st.markdown("---")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.title("⚙️ Dashboard Controls")
st.sidebar.markdown("### Filter Your Data")


cities = st.sidebar.multiselect(
    "Select Cities",
    sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

categories = st.sidebar.multiselect(
    "Select Categories",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Order Date"].min().date(), df["Order Date"].max().date()),
    min_value=df["Order Date"].min().date(),
    max_value=df["Order Date"].max().date()
)

filtered_df = df[
    df["City"].isin(cities) &
    df["Category"].isin(categories)
]
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= date_range[0]) &
        (filtered_df["Order Date"].dt.date <= date_range[1])
    ]


# ---------- KPI CARDS ----------

# ---------- KPI CARDS ----------
st.markdown("## 📌 Business Overview")

revenue = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order ID"].nunique()
units = filtered_df["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"${revenue:,.0f}")
c2.metric("📈 Total Profit", f"${profit:,.0f}")
c3.metric("📦 Total Orders", f"{orders:,}")
c4.metric("🛒 Units Sold", f"{units:,}")

st.markdown("---")

# ---------- CHARTS ----------
st.markdown("## 📊 Sales Performance")

chart_template = "plotly_dark"

monthly = filtered_df.copy()
monthly["Month"] = monthly["Order Date"].dt.strftime("%b %Y")
monthly_sales = monthly.groupby("Month", as_index=False)["Sales"].sum()

fig_month = px.area(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Revenue Trend",
    template=chart_template,
    color_discrete_sequence=["#21D4C2"]
)
fig_month.update_traces(fill="tozeroy")
fig_month.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_month, use_container_width=True)

left, right = st.columns(2)

with left:
    city_sales = filtered_df.groupby("City", as_index=False)["Sales"].sum()
    fig_city = px.bar(
        city_sales,
        x="City",
        y="Sales",
        title="Revenue by City",
        template=chart_template,
        color="City",
        color_discrete_sequence=[
            "#21D4C2", "#4389F5", "#8B72E8", "#F2B84B", "#E879A8"
        ]
    )
    fig_city.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_city, use_container_width=True)

with right:
    category_sales = filtered_df.groupby("Category", as_index=False)["Sales"].sum()
    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.55,
        title="Revenue by Category",
        template=chart_template,
        color_discrete_sequence=["#21D4C2", "#4389F5", "#F2B84B"]
    )
    fig_category.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_category, use_container_width=True)

# ---------- DATA TABLE ----------
st.markdown("---")
st.markdown("### 🏆 Top 5 Products by Revenue")

top_products = (
    filtered_df.groupby("Product", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(5)
)

fig_top_products = px.bar(
    top_products,
    x="Sales",
    y="Product",
    orientation="h",
    text="Sales",
    color="Sales",
    color_continuous_scale=["#21D4C2", "#4389F5"]
)

fig_top_products.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(autorange="reversed"),
    coloraxis_showscale=False
)

st.plotly_chart(fig_top_products, use_container_width=True)
st.markdown("## 📋 Sales Transaction Details")
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Sales Data (CSV)",
    data=csv_data,
    file_name="international_sales_data.csv",
    mime="text/csv"
)
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.markdown(
    "<p style='text-align:center;color:#91A9BF;'>"
    "Global Sales Intelligence Dashboard | Built with Python & Streamlit"
    "</p>",
    unsafe_allow_html=True
)