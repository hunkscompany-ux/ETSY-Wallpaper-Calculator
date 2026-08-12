import streamlit as st
import requests
import math
import pandas as pd


# ===============================
# 页面设置
# ===============================

st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="wide"
)

st.title("AMHUNKUS-ETSY")
st.caption("Etsy 壁纸成本计算系统 V2.7")



# ===============================
# 汇率
# ===============================

def get_exchange_rate():

    try:

        url = "https://api.exchangerate-api.com/v4/latest/USD"

        data = requests.get(
            url,
            timeout=10
        ).json()

        return data["rates"]["CNY"]

    except:

        return 7.2



exchange_rate = get_exchange_rate()



# ===============================
# 材料
# ===============================

materials = {

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
        "weight":0.40
    }

}



# ===============================
# 默认尺寸
# ===============================

default_sizes = [

    ("72W × 96H",72,96),

    ("96W × 96H",96,96),

    ("120W × 96H",120,96),

    ("144W × 96H",144,96)

]



# ===============================
# 获取尺寸
# ===============================

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




# ===============================
# 纸箱尺寸
# ===============================

def get_box_size(tube_count):


    if tube_count <= 2:

        return 55,20,10


    elif tube_count <= 4:

        return 55,20,20


    elif tube_count <= 6:

        return 55,30,20


    elif tube_count <= 9:

        return 55,30,30


    elif tube_count <= 12:

        return 55,40,30


    else:

        return 55,40,40




# ===============================
# 左右布局
# ===============================

left,right = st.columns(
    [1,2]
)



# ===============================
# 输入区域
# ===============================

with left:


    st.subheader("参数设置")


    width = st.number_input(

        "壁纸宽度（inch）",

        min_value=0.0,

        value=None,

        placeholder="留空自动计算默认尺寸"

    )


    height = st.number_input(

        "壁纸高度（inch）",

        min_value=0.0,

        value=None,

        placeholder="留空自动计算默认尺寸"

    )


    profit_ratio = st.number_input(

        "利润倍率",

        min_value=0.1,

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




# ===============================
# 结果
# ===============================

with right:


    st.subheader("计算结果")


    if calculate:


        sizes = get_sizes(
            width,
            height
        )


        package_info=[]


        material_result={}



        for size_name,w,h in sizes:



            # -----------------------
            # 米转换
            # -----------------------

            width_m = math.ceil(

                w*0.0254*10

            )/10



            height_m = math.ceil(

                h*0.0254*10

            )/10



            # 面积

            area = width_m * height_m


            billing_area = math.ceil(area)



            # -----------------------
            # 纸筒数量
            # -----------------------

            tube_count = math.ceil(

                w/20

            )



            # -----------------------
            # 商品重量
            # -----------------------

            # 材料不同，这里循环计算



            # -----------------------
            # 包装
            # -----------------------

            box_l,box_w,box_h = get_box_size(

                tube_count

            )



            package_weight = round(

                tube_count*0.45+0.8,

                1

            )



            volume_weight = round(

                box_l*
                box_w*
                box_h
                /
                8000,

                1

            )



            package_info.append({

                "尺寸":size_name,

                "转换尺寸(m)":

                f"{width_m}×{height_m}",

                "计费面积㎡":

                billing_area,

                "纸筒数量":

                tube_count,

                "纸箱尺寸(cm)":

                f"{box_l}×{box_w}×{box_h}",

                "包装重量KG":

                package_weight,

                "材积重量KG":

                volume_weight

            })



            # ======================
            # 材料计算
            # ======================


            for material,data in materials.items():



                material_weight=data["weight"]


                material_price=data["price"]



                product_weight = round(

                    billing_area*

                    material_weight

                    +

                    0.45,

                    1

                )



                final_weight=max(

                    product_weight,

                    package_weight,

                    volume_weight

                )



                purchase_cny=(

                    billing_area

                    *

                    material_price

                    *

                    exchange_rate

                )



                shipping_cny=(

                    final_weight

                    *

                    120

                    +

                    50

                )



                cost_price=(

                    purchase_cny

                    +

                    shipping_cny

                    +

                    100

                )/0.6



                sale_price=(

                    cost_price

                    *

                    profit_ratio

                )



                if material not in material_result:

                    material_result[material]=[]



                material_result[material].append({

                    "尺寸":

                    size_name,


                    "计费面积㎡":

                    billing_area,


                    "商品重量KG":

                    product_weight,


                    "最终重量KG":

                    final_weight,


                    "采购价格(RMB)":

                    round(purchase_cny,2),


                    "快递价格(RMB)":

                    round(shipping_cny,2),


                    "成本售价(RMB)":

                    round(cost_price,2),


                    "建议售价(RMB)":

                    round(sale_price,2),


                    "建议售价(USD)":

                    round(

                        sale_price/exchange_rate,

                        2

                    )

                })



        # ===============================
        # 包装信息
        # ===============================

        st.divider()

        st.subheader("尺寸与包装信息")


        st.dataframe(

            pd.DataFrame(package_info),

            use_container_width=True,

            hide_index=True

        )



        # ===============================
        # 材料报价
        # ===============================

        st.divider()

        st.subheader("材料报价")



        for material,data in material_result.items():


            st.markdown(

                f"## {material}"

            )


            st.dataframe(

                pd.DataFrame(data),

                use_container_width=True,

                hide_index=True

            )
