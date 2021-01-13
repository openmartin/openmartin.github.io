Title: CSS Grid Layout
Status: published
Date: 2020-12-30 10:00
Modified: 2020-12-30 12:00
Category: Web
Tags: css
Slug: css-grid-layout
Authors: Martin
Summary: CSS Grid Layout

## Grid 布局

Grid 布局是比 Flex 布局更强大的布局

教程：

[CSS Grid 网格布局教程](https://www.ruanyifeng.com/blog/2019/03/grid-layout-tutorial.html)

[MDN CSS 网格布局](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Grid_Layout)


## 常见用法


单元格的大小是固定的，但是容器的大小不确定。如果希望每一行（或每一列）容纳尽可能多的单元格，这时可以使用auto-fill关键字表示自动填充。

```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fill, 100px);
}
```

行和列的间距

```css
grid-row-gap: 20px;
grid-column-gap: 20px;
grid-gap: 20px;
```


## CSS trick

紧挨着的下一个邻节点, 加号表示

```css
a.thumbnail:focus +div, a.thumbnail:hover +div {
    color: #ff7c08;
}
```
