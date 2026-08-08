import streamlit as st
import requests
import math


st.set_page_config(
    page_title="AMHUNKUS-ETSY",
    layout="centered"
)


st.title("AMHUNKUS-ETSY")


st.write(
    "Etsy壁纸成本计算系统"
)


# ======================
# 获取实时汇率
# ======================

def get_exchange_rate():

    try:

        url="https://api.exchangerate-api.com/v4/latest/USD"

        data=requests.get(url).json()

        return data["rates"]["CNY"]

    except:

        return 7.2



rate=get_exchange_rate()



# ======================
# 材料
# ======================

materials={

"Peel & Stick Vinyl":
(5.5,0.23),

"Non-Woven":
(3,0.25),

"Canvas":
(5,0.30),

"Velvet Texture":
(3.5,0.31),

"3D Embossed Texture":
(12,0.39)

}



material=st.selectbox(
"选择壁纸材料",
materials.keys()
)



width = st.number_input(
    "壁纸宽度(inch)",
    min_value=1.0,
    value=120.0
)


height = st.number_input(
    "壁纸高度(inch)",
    min_value=1.0,
    value=96.0
)



profit=st.number_input(
"壁纸利润倍率",
1.2
)



st.info(
f"当前美元汇率：1 USD = {rate:.2f} CNY"
)



if st.button("开始计算"):


    price,weight=materials[material]


    # 面积

    area=(
        width*0.0254
        *
        height*0.0254
    )


    #采购

    purchase_cny=(
        area*
        price*
        rate
    )


    #壁纸重量
    #壁纸面积向上取整数
    calculate_area = math.ceil(area)
    
    # 壁纸重量
    wallpaper_weight = (
        calculate_area * weight
    )
    
    # 保留1位小数
    wallpaper_weight = round(
        wallpaper_weight,
        1
    )

    #包装重量
    package_num=math.ceil(
        area/3.5
    )


    package_weight=(
        package_num*0.4+0.7
    )


    total_weight=(
        wallpaper_weight+
        package_weight
    )


    #物流

    shipping_cny=(
        total_weight*120+50
    )


    #成本售价

    cost_price=(

        purchase_cny
        +
        shipping_cny
        +
        100

    )/0.6



    #建议售价

    selling_price=(
        cost_price*
        profit
    )


    st.divider()


    st.subheader("壁纸信息")


    st.write(
        f"面积：{area:.2f} ㎡"
    )

    st.write(
        f"壁纸重量：{wallpaper_weight} KG"
    )

    st.write(
        f"包装重量：{package_weight:.1f} KG"
    )

    st.write(
        f"总重量：{total_weight:.1f} KG"
    )


    st.divider()


    def show_price(name,cny):

        st.subheader(name)

        st.write(
            f"人民币：¥{cny:.2f}"
        )

        st.write(
            f"美元：${cny/rate:.2f}"
        )



    show_price(
        "采购价格",
        purchase_cny
    )


    show_price(
        "快递价格",
        shipping_cny
    )


    show_price(
        "成本售价",
        cost_price
    )


    show_price(
        "建议售价",
        selling_price
    )
