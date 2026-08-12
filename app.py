import streamlit as st
import requests
import math
import pandas as pd


# =====================================
# 页面设置
# =====================================

st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="wide"
)


st.title("AMHUNKUS-ETSY")

st.caption(
    "Etsy 壁纸成本计算系统 V2.9.2"
)



# =====================================
# 汇率获取
# =====================================

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



# =====================================
# 材料数据库
# =====================================

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



# =====================================
# 默认尺寸
# =====================================

default_sizes = [

    (
        "72W × 96H",
        72,
        96
    ),


    (
        "96W × 96H",
        96,
        96
    ),


    (
        "120W × 96H",
        120,
        96
    ),


    (
        "144W × 96H",
        144,
        96
    )

]



# =====================================
# 获取计算尺寸
# =====================================

def get_sizes(width,height):


    if width > 0 and height > 0:


        return [

            (
                f"{int(width)}W × {int(height)}H",
                width,
                height
            )

        ]


    else:

        return default_sizes




# =====================================
# 根据纸筒数量匹配纸箱
# =====================================

def get_box_size(tube_count):


    if tube_count <= 2:

        return 55,20,10


    elif tube_count <=4:

        return 55,20,20


    elif tube_count <=6:

        return 55,30,20


    elif tube_count <=9:

        return 55,30,30


    elif tube_count <=12:

        return 55,40,30


    else:

        return 55,40,40




# =====================================
# 向上保留两位小数
# =====================================

def ceil_two(value):

    return math.ceil(
        value * 100
    ) / 100




# =====================================
# 页面布局
# =====================================

left,right = st.columns(
    [1,2]
)




# =====================================
# 左侧输入
# =====================================

with left:


    st.subheader(
        "参数设置"
    )



    width = st.number_input(

        "壁纸宽度（inch）",

        min_value=0.0,

        value=0.0,

        step=1.0

    )



    height = st.number_input(

        "壁纸高度（inch）",

        min_value=0.0,

        value=0.0,

        step=1.0

    )



    profit_ratio = st.number_input(

        "利润倍率",

        min_value=0.01,

        max_value=0.69,

        value=0.25,

        step=0.05

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





# =====================================
# 右侧结果
# =====================================

with right:


    st.subheader(
        "计算结果"
    )



    if calculate:


        sizes = get_sizes(
            width,
            height
        )



        package_info = []

        material_results = {}



        for size_name,w,h in sizes:



            # =============================
            # 英寸转米
            # =============================


            width_m = ceil_two(

                w * 0.0254

            )


            height_m = ceil_two(

                h * 0.0254

            )



            area = (

                width_m *
                height_m

            )


            billing_area = math.ceil(
                area
            )



            # =============================
            # 纸筒数量
            # =============================


            tube_count = math.ceil(

                w / 20

            )



            # =============================
            # 箱子尺寸
            # =============================


            box_l,box_w,box_h = get_box_size(

                tube_count

            )



            # =============================
            # 包装重量
            # =============================


            package_weight = ceil_two(

                tube_count *
                0.45
                +
                0.8

            )



            # =============================
            # 材积重量
            # =============================


            volume_weight = ceil_two(

                box_l *
                box_w *
                box_h
                /
                8000

            )

            # =============================
            # 遍历材料计算
            # =============================

            for material,data in materials.items():


                material_price = data["price"]

                material_weight = data["weight"]



                # -----------------------------
                # 商品重量
                # 商品重量 = 计费面积 × 材料克重
                # -----------------------------

                product_weight = ceil_two(

                    billing_area *
                    material_weight

                )



                # -----------------------------
                # 实际重量
                # 实际重量 = 商品重量 + 包装重量
                # -----------------------------

                actual_weight = ceil_two(

                    product_weight +
                    package_weight

                )



                # -----------------------------
                # 最终计费重量
                # 实际重量 VS 材积重量
                # -----------------------------

                billing_weight = ceil_two(

                    max(

                        actual_weight,

                        volume_weight

                    )

                )



                # =============================
                # 尺寸包装信息
                # =============================

                package_info.append({

                    "材料":

                    material,


                    "尺寸":

                    size_name,


                    "转换尺寸(m)":

                    f"{width_m} × {height_m}",


                    "计费面积㎡":

                    billing_area,


                    "纸筒数量":

                    tube_count,


                    "纸箱尺寸(cm)":

                    f"{box_l} × {box_w} × {box_h}",


                    "商品重量KG":

                    f"{product_weight:.2f}",


                    "包装重量KG":

                    f"{package_weight:.2f}",


                    "实际重量KG":

                    f"{actual_weight:.2f}",


                    "材积重量KG":

                    f"{volume_weight:.2f}",


                    "计费重量KG":

                    f"{billing_weight:.2f}"

                })



                # =============================
                # 采购价格
                # =============================


                purchase_price_cny = ceil_two(

                    billing_area *

                    material_price *

                    exchange_rate

                )



                # =============================
                # 快递费用
                # =============================


                shipping_price_cny = ceil_two(

                    billing_weight *

                    120

                    +

                    50

                )



                # =============================
                # 成本售价
                # =============================


                cost_price_cny = ceil_two(

                    purchase_price_cny

                    +

                    shipping_price_cny

                )



                # =============================
                # 建议售价 USD
                #
                # 成本售价/(0.7-利润倍率)
                # 再转换美元
                # =============================


                recommend_price_usd = ceil_two(

                    cost_price_cny

                    /

                    (0.7-profit_ratio)

                    /

                    exchange_rate

                )



                if material not in material_results:


                    material_results[material] = []



                material_results[material].append({

                    "尺寸":

                    size_name,


                    "计费面积㎡":

                    billing_area,


                    "商品重量KG":

                    f"{product_weight:.2f}",


                    "包装重量KG":

                    f"{package_weight:.2f}",


                    "实际重量KG":

                    f"{actual_weight:.2f}",


                    "计费重量KG":

                    f"{billing_weight:.2f}",


                    "采购价格(RMB)":

                    purchase_price_cny,


                    "快递价格(RMB)":

                    shipping_price_cny,


                    "成本售价(RMB)":

                    cost_price_cny,


                    "建议售价(USD)":

                    recommend_price_usd

                })




        # =====================================
        # 输出尺寸包装信息
        # =====================================


        st.divider()


        st.subheader(
            "尺寸与包装信息"
        )



        package_df = pd.DataFrame(

            package_info

        )



        st.dataframe(

            package_df,

            use_container_width=True,

            hide_index=True

        )



        # =====================================
        # 输出材料报价
        # =====================================


        st.divider()


        st.subheader(

            "材料报价"

        )



        for material,result in material_results.items():


            st.markdown(

                f"## {material}"

            )



            df = pd.DataFrame(

                result

            )



            st.dataframe(

                df,

                use_container_width=True,

                hide_index=True

            )
