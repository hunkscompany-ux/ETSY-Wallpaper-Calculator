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
    <h1 style='text-align:center;'>
    AMHUNKUS-ETSY
    </h1>
    """,
    unsafe_allow_html=True
)



# ==================================================
# 汇率获取
# ==================================================

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
    向上取整，保留2位小数
    """

    return math.ceil(
        value * 100
    ) / 100






def get_sizes(width,height):


    """
    如果输入尺寸：

    使用输入尺寸

    如果为空：

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
# 纸筒数量计算 V3.0
#
# 宽度：
# 每卷50cm
#
# 高度：
# 最大700cm
#
# ==================================================

def calculate_tube_count(
    width_cm,
    height_cm
):


    # 宽度方向裁切数量

    width_parts = math.ceil(

        width_cm / 50

    )



    # 高度拆分

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



    for h in height_parts:


        # 当前高度卷数量

        roll_count = width_parts



        # 一个纸筒可装数量

        capacity = math.floor(

            700 / h

        )


        if capacity < 1:

            capacity = 1



        total_tubes += math.ceil(

            roll_count /

            capacity

        )



    return total_tubes
    # ==================================================
# 自动纸箱尺寸
# ==================================================

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





# ==================================================
# 页面顶部布局
# ==================================================

left,right = st.columns(
    [1,1]
)




# ==================================================
# 左侧 参数设置
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
# 右侧 计算规则
# ==================================================

with right:


    st.subheader(

        "计算规则"

    )


    st.markdown(

"""
### 尺寸计算

inch × 2.54 = cm

inch × 0.0254 = m


计费面积：

宽(m) × 高(m)

结果向上取整数



---


### 壁纸裁切规则


宽度：

50cm / 卷


高度：

700cm / 段



---


### 纸筒数量


根据裁切后的壁纸卷数量计算。


单个纸筒最大：

700cm长度



---


### 重量计算


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


### 价格计算


采购价格：

面积 × 材料价格 × 汇率


快递：

计费重量 ×120 +50


成本售价：

采购价格 + 快递价格


建议售价：

成本售价 ÷(0.7-利润倍率)÷汇率


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


    package_info = []


    material_price_info = {}



    for size in sizes:


        size_name = size["name"]


        width_inch = size["width"]


        height_inch = size["height"]


        # inch转cm

        width_cm = ceil_two(

            width_inch *

            2.54

        )


        height_cm = ceil_two(

            height_inch *

            2.54

        )



        # inch转m


        width_m = ceil_two(

            width_inch *

            0.0254

        )


        height_m = ceil_two(

            height_inch *

            0.0254

        )



        # 面积


        area = (

            width_m *

            height_m

        )


        billing_area = math.ceil(

            area

        )



        # 纸筒数量


        tube_count = calculate_tube_count(

            width_cm,

            height_cm

        )
                # ==================================================
        # 纸箱尺寸
        #
        # 如果用户填写包装尺寸
        # 优先使用用户输入
        #
        # 否则自动匹配
        # ==================================================


        if (

            package_length > 0

            and

            package_width > 0

            and

            package_height > 0

        ):


            box_l = package_length

            box_w = package_width

            box_h = package_height


        else:


            box_l,box_w,box_h = get_box_size(

                tube_count

            )




        # ==================================================
        # 包装重量
        #
        # 纸筒：
        # 0.45KG/个
        #
        # 箱子：
        # 0.8KG
        #
        # ==================================================


        package_weight = ceil_two(

            tube_count *

            0.45

            +

            0.8

        )




        # ==================================================
        # 材积重量
        # ==================================================


        volume_weight = ceil_two(

            box_l *

            box_w *

            box_h

            /

            8000

        )




        # ==================================================
        # 遍历材料
        # ==================================================


        for material,data in materials.items():


            material_price = data["price"]


            material_weight = data["weight"]




            # ==================================================
            # 商品重量
            #
            # 面积 × 克重
            # ==================================================


            product_weight = ceil_two(

                billing_area *

                material_weight

            )



            # ==================================================
            # 实际重量
            # ==================================================


            actual_weight = ceil_two(

                product_weight

                +

                package_weight

            )



            # ==================================================
            # 最终计费重量
            # ==================================================


            billing_weight = ceil_two(

                max(

                    actual_weight,

                    volume_weight

                )

            )




            # ==================================================
            # 采购价格
            # ==================================================


            purchase_price_rmb = ceil_two(

                billing_area *

                material_price *

                exchange_rate

            )




            # ==================================================
            # 快递费用
            # ==================================================


            shipping_price_rmb = ceil_two(

                billing_weight *

                120

                +

                50

            )




            # ==================================================
            # 成本售价
            # ==================================================


            cost_price_rmb = ceil_two(

                purchase_price_rmb

                +

                shipping_price_rmb

            )




            # ==================================================
            # 建议售价 USD
            # ==================================================


            recommend_price_usd = ceil_two(

                cost_price_rmb

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


            package_info.append({


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





            # ==================================================
            # 材料报价集中保存
            # ==================================================


            if material not in material_price_info:


                material_price_info[material] = []




            material_price_info[material].append({


                "尺寸":

                size_name,



                "计费面积㎡":

                billing_area,



                "商品重量KG":

                f"{product_weight:.2f}",



                "实际重量KG":

                f"{actual_weight:.2f}",



                "计费重量KG":

                f"{billing_weight:.2f}",



                "采购价格(RMB)":

                purchase_price_rmb,



                "快递价格(RMB)":

                shipping_price_rmb,



                "成本售价(RMB)":

                cost_price_rmb,



                "建议售价(USD)":

                recommend_price_usd

            })

        # ==================================================
        # 结果展示
        # ==================================================

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




        # ==================================================
        # 材料报价
        # ==================================================

        st.divider()



        st.subheader(

            "材料报价"

        )



        for material, rows in material_price_info.items():


            # Canvas默认展开

            expanded = False


            if "Canvas" in material:

                expanded = True



            with st.expander(

                material,

                expanded=expanded

            ):


                df = pd.DataFrame(

                    rows

                )



                st.dataframe(

                    df,

                    use_container_width=True,

                    hide_index=True

                )





        # ==================================================
        # 计算说明
        # ==================================================

        st.divider()



        st.info(

"""
AMHUNKUS-ETSY V3.0 计算说明


【尺寸】

英寸转换：

inch × 2.54 = cm

inch × 0.0254 = m


计费面积：

宽(m) × 高(m)

向上取整数



【壁纸裁切】

宽度：

每卷50cm


高度：

每段最大700cm



【纸筒】

根据裁切后的壁纸卷数量计算。


单个纸筒最大长度700cm。



【重量】

商品重量：

计费面积㎡ × 材料克重


包装重量：

纸筒数量×0.45 + 0.8


实际重量：

商品重量+包装重量


材积重量：

包装尺寸(cm) 长×宽×高÷8000


最终计费重量：

实际重量和材积重量取最大值



【价格】

采购价格：

计费面积×材料价格×汇率


快递：

计费重量×120+50


成本：

采购价格+快递


建议售价：

成本÷(0.7-利润倍率)÷汇率

"""

        )
