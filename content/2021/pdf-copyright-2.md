Title: PDF 版权保护(续)
Status: published
Date: 2021-08-10 11:00
Modified: 2021-08-10 12:00
Category: Java
Tags: pdf
Slug: pdf-copyright-next
Authors: Martin
Summary: PDF 版权保护的思路(续)


[去年(2020)写过一篇PDF版权保护的文章](../2020/pdf-copyright.md)，现在来更新一下内容

## 常规的方法

口令加密，打水印(文字和图片)，数字签名 

这些方法都可以写代码实现和写代码去掉，不管是 Java 和 C# 都可以实现

Java 推荐开源的 pdfbox，实现起来都很方便

## 非常规的方法

非常规的方法，在文档的某些部分写入隐藏和不可见的信息

[盲水印和图片隐写术](https://segmentfault.com/a/1190000038976964)

[在PDF中隐藏信息的两种方式](http://blog.wochengrenwonaocanle.com/2016/2/)

如果文档中有图片，可以在图片中写入隐藏信息，肉眼不可见，但是可以通过工具提取出来。

PDF文件结构中也可以隐藏信息，不过需要对PDF文件结构很了解才行。

