Title: java xss 防护
Status: published
Date: 2020-08-25 18:00
Modified: 2020-08-25 22:00
Category: Java
Tags: java, xss
Slug: java-xxs-protection
Authors: Martin
Summary: java xss 防护

## XSS 的类型

### 存储型 XSS

数据库中存有的存在XSS攻击的数据，返回给客户端。若数据未经过任何转义，被浏览器渲染，就可能导致XSS攻击。

### 反射型 XSS

将用户输入的存在XSS攻击的数据，发送给后台，后台并未对数据进行存储，也未经过任何过滤，直接返回给客户端。被浏览器渲染，就可能导致XSS攻击。


## 防护

### 输入过滤

https://github.com/OWASP/java-html-sanitizer

```xml
<dependency>
    <groupId>com.googlecode.owasp-java-html-sanitizer</groupId>
    <artifactId>owasp-java-html-sanitizer</artifactId>
    <version>20200713.1</version>
</dependency>
```

```java
PolicyFactory policy = Sanitizers.FORMATTING.and(Sanitizers.LINKS);
String safeHTML = policy.sanitize(untrustedHTML);
```

### 输出过滤

```xml
<dependency>
    <groupId>org.owasp.encoder</groupId>
    <artifactId>encoder</artifactId>
    <version>1.2.2</version>
</dependency>
```

```html
<%@ taglib prefix="e" uri="https://www.owasp.org/index.php/OWASP_Java_Encoder_Project" %>
<p>Exception: ${e:forHtml(exception.toString())}</p>
```

## 实践

在 spring 的 controller 中添加 String 的转换，在这个过程中过滤非法数据，所有继承 BaseController 的都会拥有过滤能力。(PS.如果子类已经有 @InitBinder, 需要调用 Super.initBinder(dataBinder))

```java
public class BaseController {
	  
		// xss protection
    @InitBinder
    protected void initBinder(WebDataBinder dataBinder) {
        dataBinder.registerCustomEditor(String.class, new StringAntiXssConverter());
    }

}
```

```java
public class StringAntiXssConverter extends PropertyEditorSupport {

    private static final PolicyFactory policy = Sanitizers.BLOCKS.and(Sanitizers.FORMATTING).and(Sanitizers.STYLES)
            .and(Sanitizers.LINKS)
            .and(new HtmlPolicyBuilder().allowElements("p").allowAttributes("class").onElements("p").toFactory())
            .and(new HtmlPolicyBuilder().allowElements("span").allowAttributes("lang").onElements("span").toFactory());


    @Override
    public String getAsText() {
        Object value = getValue();
        return (value != null ? value.toString() : "");
    }

    @Override
    public void setAsText(String text) {
        if (text == null) {
            setValue(null);
        } else {
            if (JsonUtils.isJsonValid(text)){ // 先判断是不是json字符串
                setValue(text);
            } else if (StringUtils.isHtml(text)){ // 然后 html sanitizer
                String value = policy.sanitize(text);
                setValue(value);
            } else {
                setValue(text);
            }
        }
    }
}
```

```java
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonToken;
import com.google.gson.stream.MalformedJsonException;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;

public class JsonUtils {

    public static boolean isJsonValid(final String json) {
        try {
            return isJsonValid(new StringReader(json));
        } catch (IOException e) {
            return false;
        }
    }

    public static boolean isJsonValid(final Reader reader)
            throws IOException {
        return isJsonValid(new JsonReader(reader));
    }

    public static boolean isJsonValid(final JsonReader jsonReader)
            throws IOException {
        try {
            JsonToken token;
            loop:
            while ((token = jsonReader.peek()) != JsonToken.END_DOCUMENT && token != null) {
                switch (token) {
                    case BEGIN_ARRAY:
                        jsonReader.beginArray();
                        break;
                    case END_ARRAY:
                        jsonReader.endArray();
                        break;
                    case BEGIN_OBJECT:
                        jsonReader.beginObject();
                        break;
                    case END_OBJECT:
                        jsonReader.endObject();
                        break;
                    case NAME:
                        jsonReader.nextName();
                        break;
                    case STRING:
                    case NUMBER:
                    case BOOLEAN:
                    case NULL:
                        jsonReader.skipValue();
                        break;
                    case END_DOCUMENT:
                        break loop;
                    default:
                        throw new AssertionError(token);
                }
            }
            return true;
        } catch (final MalformedJsonException ignored) {
            return false;
        }
    }
}
```

```java
import org.springframework.web.util.HtmlUtils;
public class StringUtils {
	  
		public static boolean isHtml(String str) {
        boolean isHtml = false;
        if (str != null) {
            if (!str.equals(HtmlUtils.htmlEscape(str))) {
                isHtml = true;
            }
        }
        return isHtml;
    }
}
```