Title: 计算周数
Status: published
Date: 2020-07-01 14:00
Modified: 2020-07-01 14:00
Category: Java
Tags: java
Slug: calculate_week_of_year
Authors: Martin
Summary: 如何知道一年中的第几周从哪天开始哪天结束

## 问题

计算每年的周数有两个个很明显的问题，就是第一周从什么时候开始？还有每周的第一天按星期一算还是星期天算？

## 国际标准

ISO 8601 或者 GB/T 7408-2005《数据元和交换格式信息交换日期和时间表示法》 中有一个计算每年第一周的国际标准，一般都会采用这个标准

```
即一年中的第一个日历星期包括该年的第一个星期四，并且日历年的最后一个日历星期就是在下一个日历年的第一个日历星期之前的那个星期，日历星期数是其在该年中的顺序。

确定第1个日历星期的规则与规则“第一个日历星期是包含1月4日的星期”是等同的。
```

## Java 代码

jdk 8 包含的 java.time 包含很多日期和时间的功能

```java
// 2020 年第一周的开始时间和结束时间
int year = 2020;
int week = 1;
WeekFields weekFields = WeekFields.ISO; // 或者 SUNDAY_START 一周从星期天开始

LocalDate start = LocalDate.now()
		.withYear(year)
  	.with(weekFields.weekOfYear(), week)
  	.with(weekFields.dayOfWeek(), 1L);

LocalDate end = LocalDate.now()
		.withYear(year)
		.with(weekFields.weekOfYear(), week)
		.with(weekFields.dayOfWeek(), 7L);

System.out.println(start);  // 2019-12-29
System.out.println(end);    // 2020-01-04
```

```java
// 当前时间是今年的第几周
LocalDate today = LocalDate.now();
int week = today.get(IsoFields.WEEK_OF_WEEK_BASED_YEAR);
int weekYear = today.get(IsoFields.WEEK_BASED_YEAR);

System.out.printf("now: %s is %d week of weekYear %d", today, week, weekYear);
```