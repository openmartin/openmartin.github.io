Title: 使用 GitHub Actions 自动部署 pelican 生成的 GitHub Pages
Status: published
Date: 2022-10-08 01:00
Modified: 2022-10-08 01:00
Category: Python
Tags: pelican, github
Slug: pelican-github-actions
Authors: Martin
Summary: GitHub Actions 非常方便，自动化的 CI/CD 工具

## GitHub Actions

GitHub Actions 作为自动化的 CI/CD 工具，结合 GitHub 使用起来非常方便。

下面是 `.github/workflows/main.yaml` 文件的写法

```yaml
name: Pelican site generator

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Git clone pelican-plugins
        run: |
          git clone --recursive https://github.com/getpelican/pelican-plugins
      - name: Generate html output
        run: make html
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./output
          cname: xingzuoshe.cn
```

有些注意事项:

1. GitHub 会从`默认分支`下找`.github/workflows/*.yml`文件, 所以只能放在默认分支上, repo 的 settings 里可以修改默认分支。
2. 其他人写的 GitHub Actions 不一定能拿来用，还是需要了解里面具体写的是什么命令，有的是直接下载一个 docker，但是里面的环境不一定和你的项目需要的环境一致。