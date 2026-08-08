import streamlit as st


# =========================
# AMHUNKUS-ETSY
# Wallpaper Calculator
# =========================


st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="centered"
)


st.title("AMHUNKUS-ETSY")
st.subheader("Etsy Wallpaper Cost Calculator")


# 材料数据库

materials = {

    "Peel & Stick Vinyl":{
        "price":5.5,
        "weight":0.23
    },

    "Non-Woven":{
        "price":3,
        "weight":0.25
    },

    "Canvas":{
        "price":5,
        "weight":0.30
    },

    "Velvet Texture":{
        "price":3.5,
        "weight":0.31
    },

    "3D Embossed Texture":{
        "price":12,
        "weight":0.39
    }

}



material = st.selectbox(
    "Select Wallpaper Material",
    list(materials.keys())
)



width = st.number_input(
    "Wallpaper Width (inch)",
    min_value=1.0,
    value=120.0
)


height = st.number_input(
    "Wallpaper Height (inch)",
    min_value=1.0,
    value=96.0
)



exchange_rate = st.number_input(
    "USD to CNY Exchange Rate",
    value=7.2
)



profit_ratio = st.number_input(
    "Profit Ratio",
    value=1.2
)



if st.button("Calculate"):


    # inch -> meter

    width_m = width*0.0254

    height_m = height*0.0254


    area = width_m*height_m



    material_price = materials[material]["price"]


    #采购成本

    purchase_cost = (
        area *
        material_price *
        exchange_rate
    )



    #重量

    weight = (
        area/3.5*0.4
        +0.7
    )


    #物流

    shipping_cost = (
        weight*120+50
    )



    #成本售价

    cost_price = (
        purchase_cost
        +
        shipping_cost
        +
        100
    )/0.6



    #建议售价

    recommended_price = (
        cost_price
        *
        profit_ratio
    )



    st.divider()


    st.write(
        f"Wallpaper Area: **{area:.2f}㎡**"
    )


    st.write(
        f"Total Weight: **{weight:.2f} KG**"
    )


    st.divider()


    st.subheader("Purchase Cost")

    st.write(
        f"¥{purchase_cost:.2f}"
    )

    st.write(
        f"${purchase_cost/exchange_rate:.2f}"
    )



    st.subheader("Shipping Cost")

    st.write(
        f"¥{shipping_cost:.2f}"
    )

    st.write(
        f"${shipping_cost/exchange_rate:.2f}"
    )



    st.subheader("Cost Selling Price")

    st.write(
        f"¥{cost_price:.2f}"
    )

    st.write(
        f"${cost_price/exchange_rate:.2f}"
    )



    st.subheader("Recommended Etsy Price")

    st.success(
        f"¥{recommended_price:.2f}"
    )


    st.success(
        f"${recommended_price/exchange_rate:.2f}"
    )
