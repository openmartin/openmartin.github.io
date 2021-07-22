---
Title: hugo hosting on netlify
Status: published
Date: 2021-07-20 10:00
Modified: 2021-07-20 12:00
Category: Doc
Slug: hugo-hosting-on-netlify
Authors: Martin
---

虽然本站是使用 pelican + github pages 发布的，不过现在出现了很多最新的工具，比如 hugo + netlify 。

pelican + github pages 需要在本地生成静态网页然后 push 到 github 上， github pages 会展示 repo 的一个分支。

hugo + netlify 通过CI/CD 自动生成静态网页的，生成静态网页的这一步都自动化了，只需要写好 markdown 文件就行。

具体做法可以直接看[官方文档文档](https://gohugo.io/hosting-and-deployment/hosting-on-netlify/)

配置文件 `netlify.toml`，配置好之后，推送到 github 之后会自动触发 netlify 生成和部署静态网页的动作

