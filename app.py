import streamlit as st
import requests
import math


# ==============================
# 页面设置
# ==============================

st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="wide"
)


st.title("AMHUNKUS-ETSY")
st.caption("Etsy壁纸成本计算系统")


# ==============================
# 获取实时汇率
# ==============================

def get_exchange_rate():

    try:

        url = "https://api.exchangerate-api.com/v4/latest/USD"

        response = requests.get(url, timeout=10)

        data = response.json()

        return data["rates"]["CNY"]

    except:

        # 获取失败备用汇率

        return 7.2



exchange_rate = get_exchange_rate()



# ==============================
# 材料数据库
# 单位:
# price USD / ㎡
# weight KG / ㎡
# ==============================

materials = {


    "Peel & Stick Vinyl":
    {
        "price":5.5,
        "weight":0.23
    },


    "Non-Woven":
    {
        "price":3,
        "weight":0.25
    },


    "Canvas":
    {
        "price":5,
        "weight":0.30
    },


    "Velvet Texture":
    {
        "price":3.5,
        "weight":0.31
    },


    "3D Embossed Texture":
    {
        "price":12,
        "weight":0.39
    }

}



# ==============================
# 左右布局
# ==============================

left,right = st.columns(
    [1,1.6]
)



# ==============================
# 左侧 输入区域
# ==============================


with left:


    st.subheader("参数设置")


    material = st.selectbox(
        "选择壁纸材料",
        materials.keys()
    )


    width = st.number_input(
        "壁纸宽度（inch）",
        min_value=1.0,
        max_value=1000.0,
        value=120.0,
        step=1.0
    )


    height = st.number_input(
        "壁纸高度（inch）",
        min_value=1.0,
        max_value=1000.0,
        value=96.0,
        step=1.0
    )


    profit_ratio = st.number_input(
        "壁纸利润倍率",
        min_value=0.1,
        max_value=10.0,
        value=1.2,
        step=0.1
    )


    st.info(
        f"当前汇率：1 USD = {exchange_rate:.2f} CNY"
    )



    calculate = st.button(
        "开始计算",
        use_container_width=True
    )



# ==============================
# 右侧 结果区域
# ==============================


with right:


    st.subheader("计算结果")


    if calculate:


        material_info = materials[material]


        material_price = material_info["price"]

        material_weight = material_info["weight"]



        # ----------------------
        # 面积计算
        # ----------------------

        width_m = width * 0.0254

        height_m = height * 0.0254


        area = width_m * height_m


        # 平米数向上取整

        billing_area = math.ceil(area)



        # ----------------------
        # 采购价格
        # ----------------------

        purchase_cny = (

            billing_area

            *

            material_price

            *

            exchange_rate

        )


        purchase_usd = (

            purchase_cny

            /

            exchange_rate

        )



        # ----------------------
        # 壁纸重量
        # ----------------------

        wallpaper_weight = round(

            billing_area

            *

            material_weight,

            1

        )



        # ----------------------
        # 包装重量
        # ----------------------

        package_count = math.ceil(

            billing_area / 3.5

        )


        package_weight = round(

            package_count * 0.4 + 0.7,

            1

        )



        # ----------------------
        # 总重量
        # ----------------------

        total_weight = round(

            wallpaper_weight

            +

            package_weight,

            1

        )



        # ----------------------
        # 快递费用
        # ----------------------

        shipping_cny = (

            total_weight

            *

            120

            +

            50

        )


        shipping_usd = (

            shipping_cny

            /

            exchange_rate

        )



        # ----------------------
        # 成本售价
        # ----------------------

        cost_price_cny = (

            purchase_cny

            +

            shipping_cny

            +

            100

        ) / 0.6



        cost_price_usd = (

            cost_price_cny

            /

            exchange_rate

        )



        # ----------------------
        # 建议售价
        # ----------------------

        selling_price_cny = (

            cost_price_cny

            *

            profit_ratio

        )


        selling_price_usd = (

            selling_price_cny

            /

            exchange_rate

        )



        # ======================
        # 显示结果
        # ======================


        st.divider()


        # 基础信息

        st.subheader("壁纸信息")


        info1,info2,info3,info4 = st.columns(4)


        info1.metric(
            "实际面积",
            f"{area:.2f}㎡"
        )


        info2.metric(
            "计费面积",
            f"{billing_area}㎡"
        )


        info3.metric(
            "壁纸重量",
            f"{wallpaper_weight}KG"
        )


        info4.metric(
            "总重量",
            f"{total_weight}KG"
        )



        st.divider()



        # 成本区域

        st.subheader("成本分析")


        col1,col2 = st.columns(2)



        with col1:


            st.write("### 采购价格")


            st.success(
                f"""
人民币：

¥{purchase_cny:,.2f}


美元：

${purchase_usd:,.2f}
"""
            )



            st.write("### 快递价格")


            st.warning(
                f"""
人民币：

¥{shipping_cny:,.2f}


美元：

${shipping_usd:,.2f}
"""
            )



        with col2:


            st.write("### 成本售价")


            st.info(
                f"""
人民币：

¥{cost_price_cny:,.2f}


美元：

${cost_price_usd:,.2f}
"""
            )



            st.write("### 建议售价")


            st.success(
                f"""
人民币：

¥{selling_price_cny:,.2f}


美元：

${selling_price_usd:,.2f}
"""
            )
