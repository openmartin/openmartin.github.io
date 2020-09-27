Title: selenium 的用法
Status: published
Date: 2020-09-25 11:00
Modified: 2020-09-25 12:00
Category: Java
Tags: java, selenium
Slug: selenium-java
Authors: Martin
Summary: selenium 的用法，Java API


## selenium

selenium 是一个 web 自动化测试工具，提供了各种API，就像真正的用户在操作一样。而且支持各种浏览器 Chrome、Firfox、Edge、Safari。

这里推荐用 Firefox，如果是用 Chrome 的话，跟随 Chrome 的升级，webdriver 也要频繁更新，但 Firefox 的 webdirver 不用这么频繁更新。

### Java API

selenium 提供很多种语言的 API，Python、Java、C#、Javascript、Ruby

这里介绍一下 Java API

```java
// 打开页面
System.setProperty("webdriver.gecko.driver", "E:\\workspace\\demo\\src\\main\\resources\\geckodriver.exe");
WebDriver driver = new FirefoxDriver();
driver.get("http://www.example.com/login");

// input
((FirefoxDriver) driver).findElementById("username").sendKeys("ABCDEFG");
((FirefoxDriver) driver).findElementById("password").sendKeys("ABCDEFG");

// click
((FirefoxDriver) driver).findElement(By.cssSelector("#login-btn")).click();


// 获取网页源文件
String pageSource = driver.getPageSource();
// 后续可以用 jsoup 处理，获取部分的 html

// findElement 返回 WebElement，如果找不到抛出 NoSuchElementException
// findElements 返回 list，如果找不到 list.size() = 0
element.findElement(By.cssSelector("ul>li>span:nth-child(1)")
element.findElement(By.xpath("ul/li")
element.findElement(By.id("mainContent")
```

可用浏览器的开发者工具获取 dom 节点的 xpath, cssSelector

如果是 ajax 加载的最好 Thread.sleep 几秒，等待 dom 节点加载完毕







