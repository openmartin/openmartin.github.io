Title: python small tips
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Python
Tags: python
Slug: python-small-tips
Authors: Martin
Summary: 一些Python小技巧

最近的工作中遇到一些问题，记录了下来，希望后来的人不要再踩坑了。

all()
-----

all()是python的一个内置函数，官方文档里面说如果所有的元素都为True，all()才返回True。:

    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True

有一些情况需要注意，当list为空时，返回True；空字符串，None，0 的结果都是False。:

    >>> all([])
    True
    >>> all(['a', 'b', 'c'])
    True
    >>> all(['a', 'b', ''])
    False
    >>> all(['a', 'b', None])
    False
    >>> all(['a', 'b', 0])
    False

注册表中有中文的问题
--------------------

在windows上安装python package，有时候会碰到： UnicodeDecodeError错误:

    mimetypes.init() # try to read system mime.types
    File "C:\Python27\lib\mimetypes.py", line 358, in init
    db.read_windows_registry()
    File "C:\Python27\lib\mimetypes.py", line 258, in read_windows_registry
    for subkeyname in enum_types(hkcr):
    File "C:\Python27\lib\mimetypes.py", line 249, in enum_types
    ctype = ctype.encode(default_encoding) # omit in 3.x!
    UnicodeDecodeError: 'ascii' codec can't decode byte 0x88 in position 1: ordinal not in range(128)

这是因为python从注册表中HKEY\_CLASSES\_ROOT读取mimetype时，有包含中文的文件名后缀，一般都是阿里旺旺的。:

    HKEY_CLASSES_ROOT\.阿里旺旺接收的可疑文件

删除这项就不会再出现UnicodeDecodeError错误。

我的版本是Python 2.7.6，会出现这个问题，Python 2.7.7及以后的版本修复了这个问题。

python setup.py develop
-----------------------

develop模式并不会真正的install这个包，而是在site-packages文件夹中建立一个.egg-link文件，类似于操作系统的软链接。 这样你就可以随意编辑你的代码，并不需要每次测试的时候都reinstall一遍。当然你的程序要以python包的形似来组织才行。

更多信息考参考文档 <http://pythonhosted.org//setuptools/setuptools.html#development-mode>

json 格式中单引号是不合法的
---------------------------

在json格式中单引号是不合法的字符，可以用replace(''', '"')替换掉。:

    >>> json.loads("['a', 'b', 'c']")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "D:\Python27\lib\json\__init__.py", line 338, in loads
        return _default_decoder.decode(s)
      File "D:\Python27\lib\json\decoder.py", line 365, in decode
        obj, end = self.raw_decode(s, idx=_w(s, 0).end())
      File "D:\Python27\lib\json\decoder.py", line 383, in raw_decode
        raise ValueError("No JSON object could be decoded")
     ValueError: No JSON object could be decoded

redis.Redis 和 redis.StrictRedis zadd的参数顺序不一样的
-------------------------------------------------------

redis.Redis.zadd(name, *args,*\*kwargs) value在前，分数在后

*args, 如: name1, score1, name2, score2, ... 或者是*\*kwargs, 如: name1=score1, name2=score2

redis.StrictRedis.zadd(name, *args,*\*kwargs) 分数在前，value在后

*args, 如: score1, name1, score2, name2, ... 或者是*\*kwargs, 如: name1=score1, name2=score2,