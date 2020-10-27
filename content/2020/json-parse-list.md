Title: json 反序列化数组
Status: published
Date: 2020-10-14 11:00
Modified: 2020-10-14 12:00
Category: Java
Tags: java, json
Slug: json-parse-list
Authors: Martin
Summary: json 反序列化数组

## json 反序列化

泛型的序列化比较简单，和一般对象的序列化没有区别，但是反序列化有一些不同。

### jackson

```java
import com.fasterxml.jackson.databind.ObjectMapper;
ObjectMapper mapper = new ObjectMapper();

List<MyClass> myObjectList = mapper.readValue(jsonInput, new TypeReference<List<MyClass>>(){});
```

### gson

```java
import com.google.gson.Gson;
Gson gson = new Gson();

List<MyClass> myObjectList = gson.fromJson(researchIdStr, new TypeToken<List<MyClass>>(){}.getType());
```

### fastjson

```java
import com.alibaba.fastjson.JSON;

List<MyClass> myObjectList = JSON.parseObject(researchIdStr, new TypeReference<List<MyClass>>(){});
```

### List 的元素还是个泛型

如果 List 的元素还是一个泛型，需要指定具体的子类，见下面

```java
import com.google.gson.Gson;
Gson gson = new Gson();

List<Pair<String, Boolean>> pairList = gson.fromJson(researchIdStr, new TypeToken<List<ImmutablePair<String, Boolean>>>(){}.getType());
```



