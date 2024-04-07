Title: 如何组装台式机
Status: published
Date: 2023-06-13 07:00
Modified: 2023-06-13 07:00
Category: Hardware
Tags: pc, hardware
Slug: how-to-assemble-your-pc
Authors: Martin
Summary: 如何组装台式机

## 硬件

组装台式机需要一定的硬件，最关键的是主板，主板是连接所有设备的核心部件。

- CPU
- 主板
- 电源
- CPU 散热器
- 显卡(集显可以不用买独立显卡)
- 机箱

## 最重要的：主板说明书

所有的设备都需要连接在主板上，主板说明书是最重要的操作指南，如果找不到原装的纸制说明书，可以去主板官网下载对应的电子版

AMD 和 Intel 的 CPU 插槽是不一样的，而且每一代的的CPU插槽不一样，在采购的时候需要仔细确认，板U套餐一起买一般比较便宜，而且肯定是配套的。

## 涂硅脂

某些型号的 CPU 会带原装风扇，第一次安装的时候可以不准备硅脂，因为原装风扇上是有硅脂的。但是拆下来再安装的时候一定要准备硅脂，网上买也很便宜，买那种 2g 装的大概可以用三次。

## 散热器选择

散热器一般分水冷和风冷两种大类，推荐用风冷，水冷的效果其实不是很好，水冷的风扇转速比风冷高，导致不一定比风冷安静。

## 安装步骤

1. 先把 CPU 安装在主板上，把散热器背板和固定卡扣之类的也一并安装在主板上
2. 把主板固定在机箱上。因为机箱也是金属的，会导电，所以主板跟机箱不是直接接触的，是安装在金属柱上的。如果少了金属柱，可以自己在机箱上加上，根据 ATX/MATX/ITX 版型，金属柱的位置是不一样的，大部分情况需要自己添加和减少金属柱。在安装主板的时候，主板输出接口后侧板记得要装
3. 然后在 CPU 上涂抹硅脂，安装散热器，一般都是卡扣型，硅脂要涂抹均匀，卡扣固定紧密，这样散热效果才会好
4. 如果有独立显卡，安装独立显卡
5. 电源安装到机箱上，一般需要三根线，主板供电，CPU 供电，显卡供电 
6. 其他主板连接线，CPU 散热器供电，机箱开机线，机箱前置 USB 线，机箱前置耳机线，机箱风扇供电

## Linux

推荐的 Linux 发行版是 Debian 12，桌面环境是 KDE，安装过程中直接选简体中文，安装好之后中文支持就很好，不用再特殊配置，从 KDE 5 之后可以支持高分屏，支持放大倍数，4K 屏可以支持，不过在某些应用仍有问题。

而且从 Debian 12 开始，ISO 中带上了 non-free 的 firmware，比较旧的硬件可以直接驱动，解决了大部分驱动问题。买了一个二手的 ThinkPad X230，安装过后直接能驱动所有硬件，非常 nice。

但是台式机的无线网卡驱动不了，不过 AMD 的显卡可以驱动。


