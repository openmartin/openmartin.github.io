Title: echarts 初级教程
Status: published
Date: 2020-05-25 14:00
Modified: 2020-05-25 14:00
Category: Javascript
Tags: echarts, javascript
Slug: echarts-preliminary-guide
Authors: Martin
Summary: echarts 基本概念，初级教程

## echarts 初级教程

柱状图的例子

```javascript
option = {
    title: {
        text: 'ECharts 入门示例'
    },
    tooltip: {},
    legend: {
        data:['销量']
    },
    xAxis: {
        data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
    },
    yAxis: {},
    series: [{
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
    }]
};

// 设置 echarts option
var myChart = echarts.init(document.getElementById('echartsContainer'));
myChart.setOption(option);
```

## 核心概念

xAxis.type

```
'value' 数值轴，适用于连续数据。
'category' 类目轴，适用于离散的类目数据。为该类型时类目数据可自动从 series.data 或 dataset.source 中取，或者可通过 xAxis.data 设置类目数据。
'time' 时间轴，适用于连续的时序数据，与数值轴相比时间轴带有时间的格式化，在刻度计算上也有所不同，例如会根据跨度的范围来决定使用月，星期，日还是小时范围的刻度。
'log' 对数轴。适用于对数数据。
```

yAxis.type

```
'value' 数值轴，适用于连续数据。
'category' 类目轴，适用于离散的类目数据。为该类型时类目数据可自动从 series.data 或 dataset.source 中取，或者可通过 xAxis.data 设置类目数据。
'time' 时间轴，适用于连续的时序数据，与数值轴相比时间轴带有时间的格式化，在刻度计算上也有所不同，例如会根据跨度的范围来决定使用月，星期，日还是小时范围的刻度。
'log' 对数轴。适用于对数数据。
```

series.type

```
'line' 折线图
'bar' 柱状图
'pie'  饼图
'scatter' 散点（气泡）图
'effectScatter' 带有涟漪特效动画的散点（气泡）图
'radar' 雷达图
'tree' 树图
'treemap'
'sunburst' 旭日图
'boxplot'  中文可以称为『箱形图』、『盒须图』、『盒式图』、『盒状图』、『箱线图』
'candlestick' K线图
'heatmap' 热力图主要通过颜色去表现数值的大小
'map' 地图
'parallel' 平行坐标系
'lines' 用于带有起点和终点信息的线数据的绘制，主要用于地图上的航线，路线的可视化。
'graph' 关系图 用于展现节点以及节点之间的关系数据。
'sankey' 桑基图 是一种特殊的流图（可以看作是有向无环图）。 它主要用来表示原材料、能量等如何从最初形式经过中间过程的加工或转化达到最终状态。
'funnel' 漏斗图
'gauge' 仪表盘
'pictorialBar' 象形柱图 象形柱图是可以设置各种具象图形元素（如图片、SVG PathData 等）的柱状图。往往用在信息图中。用于有至少一个类目轴或时间轴的直角坐标系上。
'themeRiver' 主题河流 是一种特殊的流图, 它主要用来表示事件或主题等在一段时间内的变化。
'custom' 自定义系列
```

## 如何学习

echarts 有非常多的 option，建议先找一个最接近的官方实例，然后在此上修改，比自己去看 API 更快更方便。
