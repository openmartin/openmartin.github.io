Title: 如何从命令行运行 TestCase
Status: published
Date: 2020-11-24 11:00
Modified: 2020-11-24 12:00
Category: Java
Tags: junit, test, testcase
Slug: junit-cmd
Authors: Martin
Summary: 如何从命令行运行 TestCase

## 如何从命令行运行 TestCase

### junit

把依赖 和 junit 放到 lib 目录下， 下面是 JUnit 4.x 的例子

```bat
set JAVA_HOME="C:\Program Files\Java\jdk1.8.0_171"
%JAVA_HOME%\bin\java -classpath "lib/*;.\classes;.\test-classes" org.junit.runner.JUnitCore com.example.util.TestJSON
```

注意：junit 依赖 hamcrest-core，也一并放到 lib 目录下


参考：https://stackoverflow.com/questions/2235276/how-to-run-junit-test-cases-from-the-command-line


### maven

也可以使用 maven 运行 TestCase

```
mvn clean test
mvn clean test -Dtest=your.package.TestClassName
mvn clean test -Dtest=your.package.TestClassName#particularMethod
```

### gradle

```
gradle test
gradle test --tests your.package.TestClassName
gradle test --tests your.package.TestClassName.particularMethod
```