import streamlit as st
import requests
import math
import pandas as pd


# ==============================
# 页面设置
# ==============================

st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="wide"
)

st.title("AMHUNKUS-ETSY")
st.caption("Etsy壁纸成本计算系统 V2.6")


# ==============================
# 汇率
# ==============================

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



# ==============================
# 材料
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

    "Canvas ⭐推荐":
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
# 默认尺寸
# ==============================

default_sizes = [
    ("72W × 96H",72,96),
    ("96W × 96H",96,96),
    ("120W × 96H",120,96),
    ("144W × 96H",144,96)
]



# ==============================
# 尺寸判断
# ==============================

def get_sizes(width,height):

    if width and height:

        return [

            (
                f"{int(width)}W × {int(height)}H",
                width,
                height
            )

        ]

    return default_sizes



# ==============================
# 包装尺寸
# ==============================

def get_package_size(package_number):


    if package_number == 1:

        return 50,15,15


    elif package_number == 2:

        return 50,30,15


    elif package_number in [3,4]:

        return 50,30,30


    else:

        return 50,45,30




# ==============================
# 页面布局
# ==============================

left,right = st.columns(
    [1,2]
)



# ==============================
# 输入
# ==============================

with left:


    st.subheader("参数设置")


    width = st.number_input(

        "壁纸宽度（inch）",

        min_value=0.0,

        value=None,

        placeholder="留空自动计算"

    )


    height = st.number_input(

        "壁纸高度（inch）",

        min_value=0.0,

        value=None,

        placeholder="留空自动计算"

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
        f"""
当前汇率：

1 USD = {exchange_rate:.2f} CNY
"""
    )


    calculate = st.button(
        "开始计算",
        use_container_width=True
    )





# ==============================
# 计算结果
# ==============================

with right:


    st.subheader("计算结果")


    if calculate:


        sizes = get_sizes(
            width,
            height
        )


        package_table=[]


        material_results={}



        # ==================================
        # 循环尺寸
        # ==================================

        for size_name,w,h in sizes:



            width_m = w * 0.0254

            height_m = h * 0.0254


            area = width_m * height_m


            billing_area = math.ceil(area)



            package_number = math.ceil(

                billing_area / 3.5

            )



            package_length,package_width,package_height = get_package_size(

                package_number

            )



            package_weight = round(

                package_number * 0.4 + 0.7,

                1

            )



            volume_weight = round(

                package_length *

                package_width *

                package_height /

                8000,

                1

            )



            package_table.append({

                "尺寸":size_name,

                "计费面积㎡":billing_area,

                "包装数量":package_number,

                "包装尺寸(cm)":

                f"{package_length}×{package_width}×{package_height}",

                "包装重量KG":

                package_weight,

                "材积重量KG":

                volume_weight

            })



            # ==================================
            # 五种材料
            # ==================================

            for material,data in materials.items():


                material_price=data["price"]

                material_weight=data["weight"]



                wallpaper_weight = round(

                    billing_area *

                    material_weight,

                    1

                )


                actual_weight = round(

                    wallpaper_weight +

                    package_weight,

                    1

                )


                charge_weight=max(

                    actual_weight,

                    volume_weight

                )



                purchase_cny=(

                    billing_area *

                    material_price *

                    exchange_rate

                )



                shipping_cny=(

                    charge_weight *

                    120 +

                    50

                )



                cost_cny=(

                    purchase_cny +

                    shipping_cny +

                    100

                ) / 0.6



                sale_cny=(

                    cost_cny *

                    profit_ratio

                )



                if material not in material_results:

                    material_results[material]=[]



                material_results[material].append({

                    "尺寸":size_name,

                    "计费面积㎡":billing_area,

                    "壁纸重量KG":wallpaper_weight,

                    "实际重量KG":actual_weight,

                    "最终计费重量KG":charge_weight,

                    "采购价格(RMB)":round(purchase_cny,2),

                    "快递价格(RMB)":round(shipping_cny,2),

                    "成本售价(RMB)":round(cost_cny,2),

                    "建议售价(RMB)":round(sale_cny,2),

                    "建议售价(USD)":round(

                        sale_cny/exchange_rate,

                        2

                    )

                })



        # ==============================
        # 显示包装信息
        # ==============================

        st.divider()

        st.subheader("尺寸与包装信息")


        package_df=pd.DataFrame(
            package_table
        )


        st.dataframe(

            package_df,

            use_container_width=True,

            hide_index=True

        )



        # ==============================
        # 材料分组显示
        # ==============================

        st.divider()

        st.subheader("各材料报价")



        for material,data in material_results.items():


            st.markdown(
                f"## {material}"
            )


            df=pd.DataFrame(data)


            st.dataframe(

                df,

                use_container_width=True,

                hide_index=True

            )
