import streamlit as st
import requests
import math
import pandas as pd


# ==================================================
# 页面配置
# ==================================================

st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="wide"
)


# ==================================================
# 标题
# ==================================================

st.markdown(
    """
    <h1 style="text-align:center;">
    AMHUNKUS-ETSY
    </h1>
    """,
    unsafe_allow_html=True
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
# 工具函数
# ==================================================

def ceil_two(value):

    """
    向上取整，保留两位小数
    """

    return math.ceil(
        value * 100
    ) / 100




def get_sizes(width,height):

    """
    有输入：
    使用输入尺寸

    无输入：
    使用默认尺寸
    """


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
# 纸筒数量计算
#
# 规则：
# 1、壁纸宽度裁剪为50cm一份
# 2、高度最大700cm
# 3、每个纸筒最多装入700cm长度
#
# ==================================================

def calculate_tube_count(width_cm, height_cm):


    # 宽度裁剪数量

    width_count = math.ceil(

        width_cm / 50

    )


    tube_count = 0


    remain_height = height_cm



    while remain_height > 0:


        current_height = min(

            remain_height,

            700

        )


        # 当前高度下，一个纸筒可装数量

        tube_capacity = math.floor(

            700 / current_height

        )


        if tube_capacity < 1:

            tube_capacity = 1



        tube_count += math.ceil(

            width_count /

            tube_capacity

        )


        remain_height -= current_height



    return tube_count





# ==================================================
# 自动匹配纸箱尺寸
# ==================================================

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





# ==================================================
# 页面布局
# ==================================================

left,right = st.columns(

    [1,1]

)



# ==================================================
# 左侧参数设置
# ==================================================

with left:


    st.subheader(

        "参数设置"

    )


    wallpaper_width = st.number_input(

        "壁纸宽度（inch）",

        min_value=0.0,

        value=0.0,

        step=1.0

    )



    wallpaper_height = st.number_input(

        "壁纸高度（inch）",

        min_value=0.0,

        value=0.0,

        step=1.0

    )



    st.divider()



    st.write(

        "包装尺寸（可选）"

    )



    package_length = st.number_input(

        "包装长度（cm）",

        min_value=0.0,

        value=0.0,

        step=1.0

    )



    package_width = st.number_input(

        "包装宽度（cm）",

        min_value=0.0,

        value=0.0,

        step=1.0

    )



    package_height = st.number_input(

        "包装高度（cm）",

        min_value=0.0,

        value=0.0,

        step=1.0

    )



    st.divider()



    profit_ratio = st.number_input(

        "利润倍率",

        min_value=0.01,

        max_value=0.69,

        value=0.25,

        step=0.05

    )



    st.info(

        f"""

当前汇率：

1 USD = {exchange_rate:.2f} CNY

"""

    )



    calculate_button = st.button(

        "开始计算",

        use_container_width=True

    )





# ==================================================
# 右侧计算规则（折叠）
# ==================================================

with right:


    with st.expander(

        "查看计算规则"

    ):


        st.markdown(

"""

### 尺寸计算

inch × 0.0254 = 米


计费面积：

宽 × 高

结果向上取整数



---

### 裁切规则


宽度：

50cm / 卷


高度：

700cm / 段



---

### 重量规则


商品重量：

计费面积 × 材料克重


包装重量：

纸筒数量 × 0.45 + 0.8


实际重量：

商品重量 + 包装重量


材积重量：

包装长 × 宽 × 高 ÷ 8000


最终计费重量：

实际重量和材积重量取最大值



---

### 价格规则


采购价格：

计费面积 × 材料价格 × 汇率


快递：

计费重量 ×120 +50


成本：

采购价格 + 快递价格


建议售价：

成本 ÷ (0.7-利润倍率) ÷ 汇率


"""

        )
        
# ==================================================
# 开始计算
# ==================================================

if calculate_button:


    sizes = get_sizes(

        wallpaper_width,

        wallpaper_height

    )


    # 尺寸与包装信息

    package_results = []


    # 材料报价

    material_results = {}



    for material in materials:


        material_results[material] = []




    # ==================================================
    # 循环尺寸
    # ==================================================

    for size in sizes:



        size_name = size["name"]


        width_inch = size["width"]


        height_inch = size["height"]




        # ----------------------------------------------
        # inch 转换
        # ----------------------------------------------

        width_cm = ceil_two(

            width_inch * 2.54

        )


        height_cm = ceil_two(

            height_inch * 2.54

        )



        width_m = ceil_two(

            width_inch * 0.0254

        )


        height_m = ceil_two(

            height_inch * 0.0254

        )




        # ----------------------------------------------
        # 计费面积
        # ----------------------------------------------

        area = (

            width_m *

            height_m

        )


        billing_area = math.ceil(

            area

        )





        # ----------------------------------------------
        # 纸筒数量
        # ----------------------------------------------

        tube_count = calculate_tube_count(

            width_cm,

            height_cm

        )




        # ----------------------------------------------
        # 包装尺寸
        # ----------------------------------------------

        if (

            package_length > 0

            and

            package_width > 0

            and

            package_height > 0

        ):


            box_length = package_length

            box_width = package_width

            box_height = package_height



        else:


            box_length,box_width,box_height = get_box_size(

                tube_count

            )





        # ----------------------------------------------
        # 包装重量
        # ----------------------------------------------

        package_weight = ceil_two(

            tube_count *

            0.45

            +

            0.8

        )




        # ----------------------------------------------
        # 材积重量
        # ----------------------------------------------

        volume_weight = ceil_two(

            box_length *

            box_width *

            box_height

            /

            8000

        )





        # ==================================================
        # 按材料计算
        # ==================================================

        for material,data in materials.items():



            # 商品重量

            product_weight = ceil_two(

                billing_area *

                data["weight"]

            )




            # 实际重量

            actual_weight = ceil_two(

                product_weight

                +

                package_weight

            )




            # 最终计费重量

            billing_weight = ceil_two(

                max(

                    actual_weight,

                    volume_weight

                )

            )




            # ----------------------------------------------
            # 采购价格
            # ----------------------------------------------

            purchase_price = ceil_two(

                billing_area *

                data["price"]

                *

                exchange_rate

            )





            # ----------------------------------------------
            # 快递费用
            # ----------------------------------------------

            shipping_price = ceil_two(

                billing_weight *

                120

                +

                50

            )





            # ----------------------------------------------
            # 成本
            # ----------------------------------------------

            cost_price = ceil_two(

                purchase_price

                +

                shipping_price

            )





            # ----------------------------------------------
            # 建议售价 USD
            # ----------------------------------------------

            selling_price_usd = ceil_two(

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





            # ==================================================
            # 尺寸包装信息
            # ==================================================

            package_results.append(

                {


                "尺寸":

                size_name,


                "计费面积㎡":

                billing_area,


                "纸筒数量":

                tube_count,


                "纸箱尺寸":

                f"{box_length}×{box_width}×{box_height}",


                "商品重量KG":

                product_weight,


                "实际重量KG":

                actual_weight,


                "材积重量KG":

                volume_weight,


                "计费重量KG":

                billing_weight


                }

            )





            # ==================================================
            # 材料报价集中保存
            # ==================================================

            material_results[material].append(

                {


                "尺寸":

                size_name,


                "计费面积㎡":

                billing_area,


                "商品重量KG":

                product_weight,


                "实际重量KG":

                actual_weight,


                "计费重量KG":

                billing_weight,


                "采购价格(RMB)":

                purchase_price,


                "快递价格(RMB)":

                shipping_price,


                "成本售价(RMB)":

                cost_price,


                "建议售价(USD)":

                selling_price_usd


                }

            )

# ==================================================
# 结果展示
# ==================================================

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



# ==================================================
# 材料报价展示
#
# 一个材料 = 一个完整表格
#
# ==================================================

st.divider()


st.subheader(

    "材料报价"

)



for material, rows in material_results.items():


    # Canvas默认展开

    expand_status = False


    if "Canvas" in material:

        expand_status = True



    with st.expander(

        material,

        expanded=expand_status

    ):


        material_df = pd.DataFrame(

            rows

        )


        st.dataframe(

            material_df,

            use_container_width=True,

            hide_index=True

        )
