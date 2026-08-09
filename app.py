import streamlit as st
import requests
import math
import pandas as pd


# =================================
# 页面设置
# =================================

st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="wide"
)


st.title("AMHUNKUS-ETSY")
st.caption("Etsy壁纸成本计算系统 V2.4")



# =================================
# 获取实时汇率
# =================================

def get_exchange_rate():

    try:

        url = "https://api.exchangerate-api.com/v4/latest/USD"

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        return data["rates"]["CNY"]

    except:

        return 7.2



exchange_rate = get_exchange_rate()



# =================================
# 壁纸材料数据库
# price USD /㎡
# weight KG /㎡
# =================================

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



# =================================
# 自动匹配包装尺寸
# =================================

def get_package_size(package_number):


    if package_number == 1:

        return 50,15,15


    elif package_number == 2:

        return 50,30,15


    elif package_number in [3,4]:

        return 50,30,30


    else:

        return 50,45,30




# =================================
# 左右布局
# =================================

left,right = st.columns(
    [1,1.8]
)



# =================================
# 左侧输入
# =================================

with left:


    st.subheader("参数设置")


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



    st.divider()


    st.info(

        f"当前汇率：1 USD = {exchange_rate:.2f} CNY"

    )



    calculate = st.button(

        "开始计算",

        use_container_width=True

    )



# =================================
# 右侧结果
# =================================

with right:


    st.subheader("计算结果")



    if calculate:


        # -----------------------------
        # 面积计算
        # -----------------------------


        width_m = width * 0.0254

        height_m = height * 0.0254


        area = width_m * height_m


        # 计费面积

        billing_area = math.ceil(area)



        # -----------------------------
        # 包装数量
        # -----------------------------


        package_number = math.ceil(

            billing_area / 3.5

        )



        # 自动包装尺寸


        package_length,package_width,package_height = get_package_size(

            package_number

        )



        # -----------------------------
        # 包装重量
        # -----------------------------


        package_weight = round(

            package_number * 0.4 + 0.7,

            1

        )



        # -----------------------------
        # 材积重量
        # -----------------------------


        volume_weight = round(

            package_length

            *

            package_width

            *

            package_height

            /

            8000,

            1

        )



        st.divider()


        st.subheader("基础信息")



        a,b,c,d = st.columns(4)


        a.metric(

            "实际面积",

            f"{area:.2f}㎡"

        )


        b.metric(

            "计费面积",

            f"{billing_area}㎡"

        )


        c.metric(

            "包装数量",

            f"{package_number}卷"

        )


        d.metric(

            "包装尺寸",

            f"{package_length}×{package_width}×{package_height}cm"

        )



        st.divider()



        st.subheader("重量分析")



        w1,w2,w3 = st.columns(3)


        w1.metric(

            "包装重量",

            f"{package_weight} KG"

        )


        w2.metric(

            "材积重量",

            f"{volume_weight} KG"

        )



        st.divider()



        # ============================
        # 五种材料计算
        # ============================


        results=[]



        for name,data in materials.items():


            material_price = data["price"]

            material_weight = data["weight"]



            # 采购价格

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



            # 壁纸重量

            wallpaper_weight = round(

                billing_area

                *

                material_weight,

                1

            )



            # 实际重量

            actual_weight = round(

                wallpaper_weight

                +

                package_weight,

                1

            )



            # 最终计费重量

            charge_weight=max(

                actual_weight,

                volume_weight

            )



            # 快递费用

            shipping_cny=(

                charge_weight

                *

                120

                +

                50

            )


            shipping_usd=(

                shipping_cny

                /

                exchange_rate

            )



            # 成本售价

            cost_price_cny=(

                purchase_cny

                +

                shipping_cny

                +

                100

            ) / 0.6



            cost_price_usd=(

                cost_price_cny

                /

                exchange_rate

            )



            # 建议售价

            selling_price_cny=(

                cost_price_cny

                *

                profit_ratio

            )



            selling_price_usd=(

                selling_price_cny

                /

                exchange_rate

            )



            results.append({

                "材料":name,

                "采购价格(RMB)":round(purchase_cny,2),

                "采购价格(USD)":round(purchase_usd,2),

                "快递价格(RMB)":round(shipping_cny,2),

                "成本售价(RMB)":round(cost_price_cny,2),

                "成本售价(USD)":round(cost_price_usd,2),

                "建议售价(RMB)":round(selling_price_cny,2),

                "建议售价(USD)":round(selling_price_usd,2)

            })



        # ============================
        # 展示表格
        # ============================


        st.divider()


        st.subheader("五种材料报价")


        df = pd.DataFrame(results)



        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )
