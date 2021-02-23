Title: 数据仓库和指标体系
Status: published
Date: 2021-02-23 10:00
Modified: 2021-02-23 12:00
Category: Data
Tags: data
Slug: data-dw-indicator
Authors: Martin
Summary: 数据仓库和指标体系


## 数据仓库和指标体系

数据仓库建设和研发过程中都有很多名词和概念，但是不要拘泥于这些教科书上的名词，一切应当以实用为最优先。

### 星型模型

下面是比较土的理解方式，如果需要找精确的定义请去网上搜索。

数据仓库建模核心就是维度建模，维度建模大部分情况下采用星型模型就够用了

元数据管理：事实表每列的类型，维度表每列的类型，还有事实表和维度的关联关系

主数据管理：最经用到的，而且是比较标准的维度，比如行政区划，产品类型，抽取出来做规范化就可以叫做主数据管理


### 指标体系

原子指标：简单理解就是一张事实表(如果一张事实表中有多个度量，比如订单金额和订单下上商品数量，可以理解成两个原子指标)

派生指标：派生指标=维度+原子指标+修饰词+聚合方式

修饰词：可以简单理解成过滤条件



参考资料：

[美团点评酒旅数据仓库建设实践](https://tech.meituan.com/2017/05/26/hotel-dw-layer-topic.html)

[美团酒旅起源数据治理平台的建设与实践](https://tech.meituan.com/2018/12/27/onedata-origin.html)

[美团点评运营数据产品化应用与实践](https://tech.meituan.com/2018/02/11/mtdp-travel-yydp-present.html)

[有赞指标库实践](https://tech.youzan.com/you-zan-zhi-biao-ku-shi-jian/)

[网易有数](https://youdata.163.com/index/manual/o/4Analyze_data_and_visualize_it/38aggregation.html)