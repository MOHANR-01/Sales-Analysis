import pandas as pd
import streamlit as st
import plotly.express as px
import openpyxl as ex

st.set_page_config(page_title = "Sales Dashboard",
                   page_icon=":bar_chart:" , 
                   layout = 'wide')

df = pd.read_excel(
    io = 'sales.xlsx',
    engine='openpyxl' ,
    # sheet_name='sales' ,
    # skiprows=3,
    # usecols='B:R',
    nrows=1000
    )



# -----------SIDEBAR

st.sidebar.header("Please Filter Here : ")
category = st.sidebar.multiselect(
    "Select the Category:" ,
    options = df["CATEGORY"].unique() ,
    default=df["CATEGORY"].unique()
)

product = st.sidebar.multiselect(
    "Select the Product:" ,
    options = df["PRODUCT"].unique() ,
    default=df["PRODUCT"].unique()
)

price = st.sidebar.multiselect(
    "Select the Price:" ,
    options = df["PRICE"].unique() ,
    default=df["PRICE"].unique()
)

df_selection = df.query(
    "CATEGORY == @category & PRODUCT == @product & PRICE == @price"
)


# ----------   MAINPAGE

st.title( ":bar_chart: Sales Dashboard" )
st.markdown("##")


# TOP PRODUCTS
total_sales = int(df_selection["PROFIT"].sum())
avg_rating = round(df_selection["AVG_RATING"].mean(), 1)
star_rating = ":star:" * int(round(avg_rating, 0))
avg_sales = round(df_selection["PROFIT"].mean(),2)

left_col, middle_col, right_col = st.columns(3)
with left_col:
    st.subheader("Total Sales :")
    st.subheader(f"US $ {total_sales:,}")

with middle_col:
    st.subheader("Average Rating :")
    st.subheader(f"{avg_rating} {star_rating}")

with right_col:
    st.subheader("Average Sales :")
    st.subheader(f"US $ {avg_sales}")

st.markdown("---")


# ------------  BAR CHART

sales_by_product = (
    df_selection.groupby(by=["PRODUCT"]).sum()[["PRICE"]].sort_values(by="PRICE")
)

fig_product_sales = px.bar(
    sales_by_product,
    x = "PRICE" ,
    y = sales_by_product.index ,
    orientation = "h" ,
    title = "<b>Sales by Product</b>" ,
    color_discrete_sequence = ["#008388"] * len(sales_by_product) ,
    template = "plotly_white"
)

# st.plotly_chart(fig_product_sales)


sales_by_category = (
    df_selection.groupby(by=["CATEGORY"]).sum()[["PROFIT"]]
)

fig_category_sales = px.pie(
    sales_by_category,
    names=sales_by_category.index,
    values="PROFIT",
    title="Profit % By Category",
    hole=.3,
    color=sales_by_category.index,
    color_discrete_sequence=px.colors.sequential.RdBu_r
)

# st.plotly_chart(fig_category_sales)



left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_category_sales, use_container_width=True)
right_col.plotly_chart(fig_product_sales, use_container_width=True)


hide_st_style = """
                <style>
                #MainMenu{visibility:hidden;}
                footer{visibility:hidden;}
                header{visibility:hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)


# st.dataframe(df)