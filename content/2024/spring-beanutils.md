Title: Spring BeanUtils 的用法
Status: published
Date: 2024-04-07 18:00
Modified: 2024-04-07 18:00
Category: Java
Tags: java, spring
Slug: spring-beanutils
Authors: Martin
Summary: BeanUtils

## Spring BeanUtils

使用 Spring 的 BeanUtils # CopyProperties 方法去拷贝对象属性时，需要对应的属性有 getter 和 setter 方法（内部实现时，使用反射拿到 set 和 get 方法，再去获取/设置属性值）；

Spring 下的 BeanUtils # copyProperties 方法实现比较简单，就是对两个对象中相同名字的属性进行简单的 get/set，仅检查属性的可访问性，因此具有较好的性能，优于 Apache 的 copyProperties。具体实现如下。


## 性能

![beanutils-performance](../images/beanutils-performance.png)

CglibBeanCopier 但是 cglib 已经不维护了，不支持 JDK 17+，一般情况使用 Spring BeanUtils 就行了，但是大量使用得时候也是存在性能问题的，直接set get 是更快的，如果存在性能问题，建议改成最简单的 set get 方法。

参考：
1. [https://juejin.cn/post/6974303935972507656](https://juejin.cn/post/6974303935972507656)