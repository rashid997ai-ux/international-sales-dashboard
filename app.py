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
    import numpy as np
    rng = np.random.default_rng(42)
    n = 600
    dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")

    catalog = {
        "Laptop":     ("Technology", 950, 0.18),
        "Monitor":    ("Technology", 320, 0.22),
        "Tablet":     ("Technology", 480, 0.20),
        "Headphones": ("Accessories", 120, 0.35),
        "Keyboard":   ("Accessories", 75, 0.38),
        "Mouse":      ("Accessories", 45, 0.40),
        "Webcam":     ("Accessories", 90, 0.30),
        "Desk Chair": ("Furniture", 260, 0.25),
        "Standing Desk": ("Furniture", 540, 0.21),
    }
    cities = {
        "New York": "East", "Boston": "East", "Chicago": "Central",
        "Dallas": "South", "Houston": "South", "Seattle": "West",
        "Los Angeles": "West", "Denver": "Central",
    }

    products = rng.choice(list(catalog), n, p=[.14, .12, .10, .13, .12, .14, .08, .09, .08])
    city_names = rng.choice(list(cities), n, p=[.20, .08, .15, .10, .10, .12, .17, .08])
    qty = rng.integers(1, 9, n)
    price = np.array([catalog[p][1] for p in products])
    margin = np.array([catalog[p][2] for p in products]) + rng.normal(0, 0.03, n)
    season = 1 + 0.25 * np.isin(dates.month, [11, 12]) - 0.10 * np.isin(dates.month, [2, 8])
    sales = (price * qty * season * rng.uniform(0.9, 1.1, n)).round(2)

    df = pd.DataFrame({
        "Order Date": dates,
        "Order ID": [f"ORD-{1001 + i}" for i in range(n)],
        "Customer Name": [f"Customer {rng.integers(1, 260)}" for _ in range(n)],
        "City": city_names,
        "Region": [cities[c] for c in city_names],
        "Product": products,
        "Category": [catalog[p][0] for p in products],
        "Quantity": qty,
        "Sales": sales,
        "Profit": (sales * margin).round(2),
    })
    return df.sort_values("Order Date").reset_index(drop=True)

df = load_data()

# ---------- PREMIUM DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0B1020, #1B1440);
    color: #F1F5F9;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}
h1, h2, h3, p, label {
    color: #F1F5F9 !important;
}
h1 { font-size: clamp(1.5rem, 4vw, 2.4rem) !important; line-height: 1.2 !important; }
h2 { font-size: clamp(1.2rem, 3vw, 1.7rem) !important; }
h3 { font-size: clamp(1rem, 2.5vw, 1.3rem) !important; }

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #2A1F6B, #3A2D9C);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #5B4BDB;
    box-shadow: 0 6px 20px rgba(0,0,0,0.30);
}
[data-testid="stMetricLabel"] { color: #CFC9F7 !important; }
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: clamp(1.3rem, 2.6vw, 2rem) !important;
}
section[data-testid="stSidebar"] {
    background: #0F0B2E;
    border-right: 1px solid #2A2468;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #5B4BDB;
    border-radius: 10px;
    overflow-x: auto;
}
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
    background-color: #E9E5FF !important;
    color: #2A1F6B !important;
    border: 1px solid #C9C0FF !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
    fill: #2A1F6B !important;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }
    [data-testid="stMetric"] { padding: 12px; }
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
palette = ["#8B5CF6", "#22D3EE", "#F59E0B", "#EC4899", "#34D399"]
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
    color_discrete_sequence=["#8B5CF6"]
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
            "#8B5CF6", "#22D3EE", "#F59E0B", "#EC4899", "#34D399", "#6366F1", "#F97316", "#14B8A6"
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
        color_discrete_sequence=["#8B5CF6", "#22D3EE", "#F59E0B"]
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
    color_continuous_scale=["#6366F1", "#EC4899"]
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