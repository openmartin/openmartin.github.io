Title: django data migration
Date: 2016-05-13 20:20
Modified: 2016-06-13 20:20
Category: Django
Tags: django
Slug: djang-data-migration
Authors: Martin
Summary: django data migration 常见问题及应对

在使用django框架开发的过程中，我们不可避免的遇到models层的变更，就涉及到数据库表的变动，django给我提供了一个migration的工具来做这些数据库表的变更。

## djang migration

如果不加appname，那么就是指所有包含migrations 目录的app

```shell
# 基于当前的model 检测修改，创建迁移策略文件
python manage.py makemigrations <appname>
# 执行迁移动作
python manage.py migrate
```

### migrations失败

有时候如果models改动比较大，migrations会失败，这个时候有两种选择，手工去修改migrations文件，第二种是清除所有migrations，重新migrate

#### 手工修改migrations文件

通过报错信息加上SQL语句找到找到问题，然后具体问题具体分析，是修改数据库里面的数据，还是修改migrations生成的脚本。


```shell
python manage.py migrate

python manage.py sqlmigrate <appname> 0001
```

当处理模型修改的时候：

- 如果模型包含一个未曾在数据库里建立的字段，Django会报出错信息。 当你第一次用Django的数据库API请求表中不存在的字段时会导致错误。

- Django不关心数据库表中是否存在未在模型中定义的列。

- Django不关心数据库中是否存在未被模型表示的table。


在使用SQLite3数据库时, 因为SQLite3 不支持删除列操作，只有有限地 ALTER TABLE 支持，
所以修改数据库列的操作被新建表然后select into newtable 代替，所以会存在更多问题

参考

http://www.tuicool.com/articles/yM3IVr

##### NULL to NOT NULL

```shell
python manage.py makemigrations
You are trying to add a non-nullable field 'college' to majorproperty without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now()
>>> 1
```

在migrate的时候提示你需要指定一个默认值，用以处理NULL的情况

#### 清除migrations

清除所有app目录/migrations/下除__init__.py 文件之外的py文件

```shell
find . -path "*migrations*" -name "*.py" -not -path "*__init__*" -exec rm {} \;
```


#### squashmigrations

当migrations越来越多的时候执行 makemigrations 和 migrate 就会越来越慢，可以考虑对其瘦身（减少migrations文件的数量）

```shell
python manage.py squashmigrations schools 0002
```

## 数据导入导出

### 数据导出
django 项目提供了一个导出的方法 python manage.py dumpdata, 不指定 appname 时默认为导出所有的app

```shell
python manage.py dumpdata [appname] > appname_data.json
```

### 数据导入

数据导入,不需要指定 appname

```
python manage.py loaddata appname_data.json
```

优点：可以兼容各种支持的数据库，也就是说，以前用的是 SQLite3，可以导出后，用这种方法导入到 MySQL, PostgreSQL等数据库，反过来也可以。

缺点：数据量大的时候，速度相对较慢，表的关系比较复杂的时候可以导入不成功。

### 常见数据导入导出

一般情况下，我们导入导出的时候需要排除一些app，contenttypes(新环境migrate的时候会重新生成，而且包含数据)，sessions(用户session相关数据),  admin(admin log)

auth 包含用户，可视情况决定是否导出

```
python manage.py dumpdata --all --indent=4 --exclude=auth --exclude=contenttypes --exclude=sessions --exclude=admin > all.json
python manage.py loaddata all.json
```

