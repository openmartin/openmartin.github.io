Title: 大模型开发中常用的正则表达式
Status: published
Date: 2025-08-20 20:00
Modified: 2025-08-20 20:00
Category: Python
Tags: python
Slug: most-used-regex-in-llm-development
Authors: Martin
Summary: 大模型开发中常用的正则表达式

## 提取 JSON

```
match = re.search(r'```json\s*([\s\S]*?)\s*```', text, re.MULTILINE)
if match:
    json_code = match.group(0)
```

提取出来还要去掉开头的 &#96;&#96;&#96;json 和 结尾的 &#96;&#96;&#96;

## 提取 XML

```python
match = re.search(r'```xml\s*([\s\S]*?)\s*```', text, re.MULTILINE)
if match:
    xml_code = match.group(0)
```

提取出来还要去掉开头的 &#96;&#96;&#96;xml 和 结尾的 &#96;&#96;&#96;

## 去掉 think 标签

```python
cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
```

