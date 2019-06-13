Title: reStructuredText to Markdown
Date: 2016-04-20 20:20
Modified: 2016-04-25 20:20
Category: Doc
Tags: pandoc
Slug: pandoc-trans-rst-markdown
Authors: Martin
Summary: pandoc 是一个haskell语言开发的文档格式转换工具，支持非常丰富的格式，覆盖了常见的所有格式。使用起来非常方便。

## pandoc

pandoc 是一个haskell语言开发的文档格式转换工具，支持非常丰富的格式，覆盖了常见的所有格式。使用起来非常方便。

### 安装
```shell
# mac osx
brew install pandoc
# ubuntu
sudo apt-get install pandoc
```

### 格式转换
reStructuredText to markdown

```shell
pandoc -f rst --toc small_tip.rst -t markdown_github -o small_tip.md
```

更多例子
[pandoc demo](http://pandoc.org/demos.html)

