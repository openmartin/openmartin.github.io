Title: ryzentosh 从零开始的黑苹果
Status: published
Date: 2020-08-08 22:00
Modified: 2020-08-08 22:00
Category: Hardware
Tags: mac, hackintosh, ryzentosh
Slug: ryzentosh
Authors: Martin
Summary: AMD, Yes! 从零开始组装一台 AMD 黑苹果

## 硬件的选择

理论上其实 Intel 平台的黑苹果更接近白苹果，后续的一些问题会更容易解决，不过既然是 AMD, Yes! 那么我们就来挑战一下 ryzentosh，也有很多成功的案例，难度在逐渐降低。

因为最新的 opencore 不支持 AMD B550 平台，而且后续也比较难支持，所有目前还是选择 B450。PCIe 5.0 的标准明年(2021)就出了，以后 PCIe 5.0 + DDR 5 估计是标配了，所以选择为了 PCIe 4.0 选择 B550 或者 X570，意义不大，只是一个短时的过渡。

| 部件     | 品牌和型号                                      | 价格         |
|----------|-------------------------------------------------|--------------|
| 主板     | 微星 MSI B450M MORTAR MAX                        | 板U套装 2499 |
| CPU      | AMD 3700X                                      |              |
| 显卡     | 蓝宝石 Sapphire RX580 8G 白金版 OC              | 800          |
| 内存     | 阿斯加特 Asgard 16GB 3000频率 DDR4 台式机内存条   | 299X2        |
| 固态硬盘 | 金士顿 Kingston A2000 1TB NVMe协议              | 759          |
| 无线网卡 | 奋威 FV-T919 bcm94360cd 黑苹果免驱动              | 258          |
| 电源     | 二手 安钛克 Antec NeoECO II 550                 | 152          |
| 机箱     | 银欣 SilverStone PS15B   M-ATX 小机箱           | 200          |
| 总计     |                                                | 5266         |


同类的 EFI 配置参考

[B450M-MORTAR-MAX-Hackintosh](https://github.com/techysy/B450M-MORTAR-Hackintosh)

[B450M-MORTAR-Hackintosh](https://github.com/heyxiaobai/MSI-B450m-MORTAR-Hackintosh)

## macOS 下安装U盘的制作

由于已经有了一台 MacBook Pro，所以跟其他教程不一样，我们在 macOS 下制作安装U盘

### 简单的方法

直接去下载黑果小兵做好的镜像文件，写入U盘，然后直接复制同类的 EFI 文件，参考 [macOS安装教程兼小米Pro安装过程记录](https://blog.daliansky.net/MacOS-installation-tutorial-XiaoMi-Pro-installation-process-records.html)

这样如果没有问题，那很方便，但是如果有什么地方有问题就不知道怎么办了，黑苹果很考验动手能力，还是建议用复杂的办法，一步一步来，理解原理。

### 复杂的方法

按照 AMD Vallina 的安装方法一步一步，参考 [保姆级黑苹果教程：让你的Ryzen+A卡用上最新版本的MacOS](https://juejin.im/post/6844904135368654856)

或者按照小学生的视频教程 [小学生玩转macOS](https://www.bilibili.com/video/av328135482/) 跪了，真的是小学生

这个教程也不错 [黑苹果开荒记系统篇:超详细纯净MacOS安装流程](http://zhongce.sina.com.cn/article/view/53765/)

### 配置 OpenCore

假设已经做好了安装U盘，最重要的工作是 OpenCore 的配置，和寻找合适的驱动

- [OpenCorePkg](https://github.com/acidanthera/OpenCorePkg/releases)
- [ProperTree](https://github.com/corpnewt/ProperTree.git)
- [gibMacOS](https://github.com/corpnewt/gibMacOS.git)
- [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS.git)
- [SSDTTime](https://github.com/corpnewt/SSDTTime.git)
- [USBMap](https://github.com/corpnewt/USBMap.git)
- [AMD Vanilla](https://github.com/AMD-OSX/AMD_Vanilla/tree/opencore)

上面的工具不一定都用得到，不过可以先下载下来。

黑苹果的原理就是让 macOS 以为它运行在苹果的硬件上，在以前的时代没有太大的可能，但是在计算机硬件行业推广使用 UEFI 和苹果采用 Intel CPU 之后，操作系统和硬件之间增加了一层，我们就在这一层仿冒和加载驱动。关于 UEFI 可以关注 [UEFI和BIOS探秘](https://zhuanlan.zhihu.com/UEFIBlog) 作者的水平很高，应该是在 Intel 工作写 UEFI 的人。

用到的文件

```

```






