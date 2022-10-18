Title: RestTemplate POST Multipart File
Status: published
Date: 2022-10-18 23:00
Modified: 2022-10-18 23:00
Category: Java
Tags: java, spring
Slug: rest-template-post-multipart-file
Authors: Martin
Summary: RestTemplate POST Multipart File 踩过的坑

## RestTemplate

下面的代码以 Multipart 形式 POST 文件到一个 URL，最重要的是使用 `FileSystemResource`

```java
LinkedMultiValueMap<String, Object> map = new LinkedMultiValueMap<>();
FileSystemResource value = new FileSystemResource(new File("D://test.png"));
map.add("file", value);
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.MULTIPART_FORM_DATA);
HttpEntity<LinkedMultiValueMap<String, Object>> requestEntity = new HttpEntity<>(map, headers);
RestTemplate restTemplate = new RestTemplate();
restTemplate.exchange("http://localhost/api/v1/users/avatar", HttpMethod.POST, requestEntity, String.class);
```

FileSystemResource 必须要有一个本地文件， 我从数据库或者对象存储中读出来的内容是不是必须写一个本地临时文件？

能不能使用其他类型的 Resource 呢，比如 `ByteArrayResource`，答案是不行，[这里有详细解释](https://github.com/spring-projects/spring-framework/issues/18147#issuecomment-453431464)

In order to properly write the multipart request, the FormHttpMessageConverter configured automatically with the RestTemplate will write all parts; if a part inherits from Resource, it calls the Resource.getFilename() method to get a file name, see the getFilename() method. If no file name is found, then this part is written as a "regular" part, not a file, in the content-disposition part of the message.

## MultipartFileResource

为了解决上面的问题，我们可以自定义一个类，包含 filename

```java
public class MultipartFileResource extends ByteArrayResource {

    private String filename;

    public MultipartFileResource(byte[] byteArray, String filename) {
        super(byteArray);
        this.filename = filename;
    }

    @Override
    public String getFilename() {
        return this.filename;
    }
}
```

上面的代码可以修改为，即可实现 RestTemplate POST Multipart 文件类型，并不需要写一个临时文件，只需要文件的内容 byte[]

```java
LinkedMultiValueMap<String, Object> map = new LinkedMultiValueMap<>();
MultipartFileResource value = new MultipartFileResource(byte[] fileContent, "example.txt");
map.add("file", value);
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.MULTIPART_FORM_DATA);
HttpEntity<LinkedMultiValueMap<String, Object>> requestEntity = new HttpEntity<>(map, headers);
RestTemplate restTemplate = new RestTemplate();
restTemplate.exchange("http://localhost/api/v1/users/avatar", HttpMethod.POST, requestEntity, String.class);
```