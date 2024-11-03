Title: vscode 新文件模板
Status: published
Date: 2024-11-04 22:00
Modified: 2024-11-04 22:00
Category: Java
Tags: vscode
Slug: vscode-snippets
Authors: Martin
Summary: 怎么设置一个项目里的代码片段


设置 vscode snippets

官方文档 [https://code.visualstudio.com/docs/editor/userdefinedsnippets](https://code.visualstudio.com/docs/editor/userdefinedsnippets)

有三种 scope 的 代码片段

1. Global 
2. Language "文件"(File) -> "首选项"(Preferences) -> "用户代码片段"(User Snippets)
3. Project

在项目中的配置比较合适，在项目根目录下新建 `.vscode/xxx.code-snippets`, xxx 可以命名为一种语言，下面是一个 markdown.code-snippets 的例子。

写 markdown blog 需要一些 meta 信息，每次从以前的文件中复制出来比较费劲，定义一个 snippets，然后敲 prefix 的提示词就可以自动带出来，可以节省下复制粘帖的动作。

```json
{
  "Markdown Blog Header":{
		"prefix": "header",
		"body": [
			"Title: $TM_FILENAME_BASE",
			"Status: published",
			"Date: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE",
			"Modified: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE",
			"Category: Linux",
			"Tags: vscode",
			"Slug: $TM_FILENAME_BASE",
			"Authors: Martin",
			"Summary: ",
			"",
			"$0"
		],
		"description": "markdown blog header",
		"isFileTemplate": true
	}
}
```