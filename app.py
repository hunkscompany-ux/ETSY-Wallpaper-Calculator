import streamlit as st
import requests
import math
import pandas as pd


# ==================================================
# 页面设置
# ==================================================

st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="wide"
)


st.title("AMHUNKUS-ETSY")

st.caption(
    "Etsy 壁纸成本计算系统 V2.9.4"
)



# ==================================================
# 获取实时汇率
# ==================================================

def get_exchange_rate():

    try:

        url = "https://api.exchangerate-api.com/v4/latest/USD"

        result = requests.get(
            url,
            timeout=10
        ).json()

        return result["rates"]["CNY"]


    except:

        return 7.2



exchange_rate = get_exchange_rate()



# ==================================================
# 材料数据库
# ==================================================

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




# ==================================================
# 默认尺寸
# ==================================================

default_sizes = [

    {
        "name":"72W × 96H",
        "width":72,
        "height":96
    },


    {
        "name":"96W × 96H",
        "width":96,
        "height":96
    },


    {
        "name":"120W × 96H",
        "width":120,
        "height":96
    },


    {
        "name":"144W × 96H",
        "width":144,
        "height":96
    }

]




# ==================================================
# 向上保留2位小数
# ==================================================

def ceil_two(value):

    return math.ceil(
        value * 100
    ) / 100




# ==================================================
# 获取计算尺寸
# ==================================================

def get_sizes(width,height):


    if width > 0 and height > 0:


        return [

            {
                "name":
                f"{int(width)}W × {int(height)}H",

                "width":
                width,

                "height":
                height
            }

        ]


    return default_sizes





# ==================================================
# 最新纸筒数量计算 V2.9.4
#
# 宽度：
# 每卷50cm
#
# 高度：
# 每卷最大700cm
#
# ==================================================

def calculate_tube_count(width_cm,height_cm):


    # 宽度裁切数量

    width_parts = math.ceil(

        width_cm / 50

    )



    # 高度切割

    height_parts = []


    remain = height_cm



    while remain > 0:


        if remain >= 700:


            height_parts.append(700)

            remain -= 700


        else:


            height_parts.append(remain)

            remain = 0




    total_tubes = 0



    # 每段高度分别计算

    for h in height_parts:


        roll_count = width_parts



        # 一个纸筒可装多少卷

        capacity = math.floor(

            700 / h

        )


        if capacity < 1:

            capacity = 1



        tubes = math.ceil(

            roll_count /

            capacity

        )


        total_tubes += tubes



    return total_tubes




# ==================================================
# 根据纸筒数量匹配纸箱
# ==================================================

def get_box_size(tube_count):


    if tube_count <=2:


        return (
            55,
            20,
            10
        )


    elif tube_count <=4:


        return (
            55,
            20,
            20
        )


    elif tube_count <=6:


        return (
            55,
            30,
            20
        )


    elif tube_count <=9:


        return (
            55,
            30,
            30
        )


    elif tube_count <=12:


        return (
            55,
            40,
            30
        )


    else:


        return (
            55,
            40,
            40
        )





# ==================================================
# 页面布局
# ==================================================

left,right = st.columns(
    [1,2]
)





# ==================================================
# 左侧参数
# ==================================================

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



    start = st.button(

        "开始计算",

        use_container_width=True

    )



# ==================================================
# 右侧结果
# ==================================================

with right:


    st.subheader(
        "计算结果"
    )

# ==================================================
# 开始计算
# ==================================================

if start:


    sizes = get_sizes(
        width,
        height
    )


    package_results = []

    material_results = {}



    # ==============================================
    # 循环尺寸
    # ==============================================

    for size in sizes:


        size_name = size["name"]

        width_inch = size["width"]

        height_inch = size["height"]



        # ==========================================
        # inch 转 cm
        # ==========================================

        width_cm = ceil_two(

            width_inch *

            2.54

        )


        height_cm = ceil_two(

            height_inch *

            2.54

        )



        # ==========================================
        # inch 转米
        # ==========================================

        width_m = ceil_two(

            width_inch *

            0.0254

        )


        height_m = ceil_two(

            height_inch *

            0.0254

        )



        # ==========================================
        # 计费面积
        # ==========================================

        area = (

            width_m *

            height_m

        )


        billing_area = math.ceil(

            area

        )



        # ==========================================
        # 纸筒数量
        # ==========================================

        tube_count = calculate_tube_count(

            width_cm,

            height_cm

        )



        # ==========================================
        # 箱子尺寸
        # ==========================================

        box_l,box_w,box_h = get_box_size(

            tube_count

        )



        # ==========================================
        # 包装重量
        #
        # 纸筒重量0.45KG
        # 箱子重量0.8KG
        #
        # ==========================================

        package_weight = ceil_two(

            tube_count *

            0.45

            +

            0.8

        )



        # ==========================================
        # 材积重量
        #
        # 长×宽×高÷8000
        #
        # ==========================================

        volume_weight = ceil_two(

            box_l *

            box_w *

            box_h

            /

            8000

        )




        # ==========================================
        # 不同材料计算
        # ==========================================


        for material,info in materials.items():


            material_price = info["price"]

            material_weight = info["weight"]



            # ======================================
            # 商品重量
            #
            # 面积 × 克重
            #
            # ======================================

            product_weight = ceil_two(

                billing_area *

                material_weight

            )



            # ======================================
            # 实际重量
            #
            # 商品重量+包装重量
            #
            # ======================================

            actual_weight = ceil_two(

                product_weight

                +

                package_weight

            )



            # ======================================
            # 最终计费重量
            #
            # 实际重量 VS 材积重量
            #
            # ======================================

            billing_weight = ceil_two(

                max(

                    actual_weight,

                    volume_weight

                )

            )



            # ======================================
            # 采购价格
            # ======================================

            purchase_price = ceil_two(

                billing_area

                *

                material_price

                *

                exchange_rate

            )



            # ======================================
            # 快递价格
            # ======================================

            shipping_price = ceil_two(

                billing_weight

                *

                120

                +

                50

            )



            # ======================================
            # 成本售价
            # ======================================

            cost_price = ceil_two(

                purchase_price

                +

                shipping_price

            )



            # ======================================
            # 建议售价 USD
            # ======================================

            recommend_price = ceil_two(

                cost_price

                /

                (

                    0.7

                    -

                    profit_ratio

                )

                /

                exchange_rate

            )



            # ======================================
            # 包装信息
            # ======================================

            package_results.append({


                "材料":

                material,


                "尺寸":

                size_name,


                "转换尺寸(cm)":

                f"{width_cm} × {height_cm}",



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




            # ======================================
            # 材料报价
            # ======================================


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

                purchase_price,



                "快递价格(RMB)":

                shipping_price,



                "成本售价(RMB)":

                cost_price,



                "建议售价(USD)":

                recommend_price

            })
                    # ==========================================
        # 尺寸与包装信息展示
        # ==========================================

        st.divider()


        st.subheader(
            "尺寸与包装信息"
        )


        package_df = pd.DataFrame(

            package_results

        )


        st.dataframe(

            package_df,

            use_container_width=True,

            hide_index=True

        )



        # ==========================================
        # 材料报价展示
        # ==========================================

        st.divider()


        st.subheader(
            "材料报价"
        )



        for material,result in material_results.items():


            st.markdown(

                f"### {material}"

            )



            material_df = pd.DataFrame(

                result

            )



            st.dataframe(

                material_df,

                use_container_width=True,

                hide_index=True

            )



        # ==========================================
        # 计算说明
        # ==========================================

        st.divider()


        st.info(
            """
计算规则：

1. 商品重量
= 计费面积㎡ × 材料克重


2. 包装重量
= 纸筒数量 × 0.45KG + 0.8KG


3. 实际重量
= 商品重量 + 包装重量


4. 材积重量
= 纸箱长 × 宽 × 高 ÷ 8000


5. 最终计费重量
= 实际重量 与 材积重量取最大值


6. 快递费用
= 最终计费重量 ×120 +50


7. 建议售价USD
= 成本售价 ÷ (0.7-利润倍率) ÷ 汇率
"""
        )
