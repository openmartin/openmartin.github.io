Title: 计算文本相似度
Status: published
Date: 2020-06-15 14:00
Modified: 2020-05-15 14:00
Category: NLP
Tags: nlp
Slug: text-similarity-nlp
Authors: Martin
Summary: 如何计算文本相似度

## 词的相似度

作为一个NLP的门外汉， word2vec 算法只能看懂个大概，个人的理解就是假定一个词跟它周围的词是相关的，通过大量的数据可以训练出一个模型。

使用的话只用调用模型得出结果就行，训练模型的问题就交给大神去做了，而且目前有一些开源的。

目前使用的是 hanlp 开源的 https://github.com/hankcs/HanLP/wiki/word2vec


https://www.hankcs.com/nlp/word2vec.html

## 句子的相似度

句子的相似度可以把所有的词向量加起来再计算，目前也是使用 hanlp 开源的

https://zhuanlan.zhihu.com/p/37104535

https://github.com/shibing624/text2vec


## 文章的相似度

Google 提出的 samehash 算法，可以去搜索一下，对长文本的效果不错，对短文本的效果反而不太好。
