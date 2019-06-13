Title: YAML简介
Date: 2015-10-01 20:20
Modified: 2015-10-01 20:20
Category: Django
Tags: django, aws, zinnia
Slug: introduce-to-yaml
Authors: Martin
Summary: YAML简介


YAML(尾音类似camel)是一个可读性高，用来表达数据序列化的语言。 在最初的时候YAML表示Yet Another Markup Language，但是现在YAML Ain’t Markup Language。

官方的定义是这样写的：YAML is a human friendly data serialization standard for all programming languages.

可读性好
--------

YAML格式有很好的可读性，对比JSON格式，增加了换行和缩进，就像Python一样。:

    name: Vorlin Laruknuzum
    sex: Male
    class: Priest
    title: Acolyte
    hp: [32, 71]
    sp: [1, 13]
    gold: 423
    inventory:
    - a Holy Book of Prayers (Words of Wisdom)
    - an Azure Potion of Cure Light Wounds
    - a Silver Wand of Wonder

注释和文档结构
--------------

在yaml格式中注释有两种格式单行注释以 \# 开始， 多行注释跟C语言一样 /\* \*/

yaml 可以在一个string中包含多个document， 每个文档以三个短横线开始，以三个点结束，不过结束标志并不是必须的。

> &gt;&gt;&gt; a = yaml.load\_all(""" ... \# Play by Play Feed ... ---... time: 20:03:20 ... player: Sammy Sosa ... action: strike (miss) ... ... ... ---... time: 20:03:47 ... player: Sammy Sosa ... action: grand slam ... """) &gt;&gt;&gt; for i in a: ... print i ... {'action': 'strike (miss)', 'player': 'Sammy Sosa', 'time': 72200} {'action': 'grand slam', 'player': 'Sammy Sosa', 'time': 72227}

数据结构和数据类型
------------------

在yaml中有三种数据结构Scalar，Sequence，Mapping（标量，序列，字典）

1.  Scalar

Scalar 的格式很灵活，可以不带引号, 单引号(不需要转义)，双引号（需要转义），还可以有多行的形式:

    --- |
    Hello, world!
    Have a line break

    --- >
    Hello, World!
    no line break

更多情况参考 <http://www.yaml.org/spec/1.2/spec.html> 2.3. Scalars

1.  Sequence

Sequence 有两种形式，和JSON一样的使用中括号\[\]， 或者是每个元素以短横线和空格("- ")开始。在最开始的例子中就可以看到两种形式。

1.  Mapping

同样，Mapping也有两种形式，我们直接看例子吧:

    >>> yaml.load("""
    ... main:
    ...     game: hearthstone
    ...     role: {name: Jaina, class: magician}
    ... """)
    {'main': {'game': 'hearthstone', 'role': {'name': 'Jaina', 'class': 'magician'}}}

python 和 yaml
--------------

解析和生成yaml都可以用pyyaml库，用法参考上面的例子，主要使用两个函数 load 和 dump。

在实际的使用过程中，一般用yaml格式做配置文件，因为yaml格式的可读性非常好，人工编辑很方便，而且也方便程序读取。

更多资料
--------

yaml格式官网 <http://www.yaml.org/>

pyyaml <http://pyyaml.org/wiki/PyYAML>

各种编程语言在实现yaml解析的时候可能对应到本语言的数据类型类型可能不一致， 如果需要更严格的指定数据类型需要了解yaml tags

<http://www.yaml.org/spec/1.2/spec.html> 2.4. Tags

<http://yaml.org/type/index.html>
