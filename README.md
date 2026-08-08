# ETSY-Wallpaper-Calculator
AMHUNKUS-ETSY Wallpaper Calculator

帮我设计一个程序

背景：
我是一名etsy卖家，我的店铺经营壁纸相关商品
材料一共五种,分别为Peel & Stick Vinyl、Non-Woven、Canvas、Velvet Texture、3D Embossed Texture；
每种材料价格为Peel & Stick Vinyl  $5.5/平米、Non-Woven  $3/平米、Canvas  $5/平米、Velvet Texture  $3.5/平米、3D Embossed Texture  $12/平米；
每种材料的克重为：Peel & Stick Vinyl 0.23KG/平米、Non-Woven 0.25KG/平米、Canvas 0.3KGg/平米、Velvet Texture 0.31KG/平米、3D Embossed Texture 0.39KG/平米；
总重量为（KG）：壁纸平米数/3.5*0.4+0.7
快递费用计算公示为(CNY)：总重量（KG）*120+50

需求：
当我选择壁纸材料，输入壁纸尺寸的宽高（单位英寸，计算时需要单位转换为米）后
输出采购价格（对应壁纸材料价格*平米数），单位为人民币，自动转换为美元，两个币种都显示
输出快递价格（总重量（KG）*120+50），单位为人民币，自动转换为美元，两个币种都显示
输出成本售价（采购价格+快递价格+100）/0.6，单位为人民币，自动转换为美元，两个币种都显示
当我输入壁纸利润比时，例如1.2
输出建议售价（成本售价*壁纸利润比），单位为人民币，自动转换为美元，两个币种都显示

发布模式为：github上传程序源码，streamlit发布访问
---------------------------V2.0--------------------------------------------------
帮我设计一个程序

背景：
我是一名etsy卖家，我的店铺经营壁纸相关商品
材料一共五种,分别为Peel & Stick Vinyl、Non-Woven、Canvas、Velvet Texture、3D Embossed Texture；
每种材料价格为Peel & Stick Vinyl  $5.5/平米、Non-Woven  $3/平米、Canvas  $5/平米、Velvet Texture  $3.5/平米、3D Embossed Texture  $12/平米；
每种材料的克重为：Peel & Stick Vinyl 0.23KG/平米、Non-Woven 0.25KG/平米、Canvas 0.3KGg/平米、Velvet Texture 0.31KG/平米、3D Embossed Texture 0.39KG/平米；
壁纸重量为（KG）：壁纸平米数*对应壁纸材料重量，结果向上取整数
包装重量为（KG）：壁纸平米数/3.5，计算结果向上取整数，然后计算结果*0.4+0.7
总重量为（KG）：壁纸重量+包装重量
快递费用计算公示为(CNY)：总重量（KG）*120+50

需求：
当我选择壁纸材料，输入壁纸尺寸的宽高（单位英寸，计算时需要单位转换为米）后
输出采购价格（对应壁纸材料价格*平米数），单位为人民币，自动转换为美元，两个币种都显示
输出快递价格（总重量（KG）*120+50），单位为人民币，自动转换为美元，两个币种都显示
输出成本售价（采购价格+快递价格+100）/0.6，单位为人民币，自动转换为美元，两个币种都显示
当我输入壁纸利润比时，例如1.2
输出建议售价（成本售价*壁纸利润比），单位为人民币，自动转换为美元，两个币种都显示

注：
1、发布模式为：github上传程序源码，streamlit发布访问
2、人民币与美元兑换回来自动获取最新汇率
3、页面除了标题，其它都用中文显示
