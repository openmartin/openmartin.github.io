Title: Python 中 class 的 JSON 序列化
Date: 2015-08-17 20:20
Modified: 2015-08-17 20:20
Category: Python
Tags: json
Slug: python-obj-to-json
Authors: Martin
Summary: Python 中 class 的 JSON 序列化

在Java中如果定义一个class，是十分方便JSON序列化的，比如说使用 jackson lib。

但是在Python中如果使用json.dumps(a)，a如果不是一个简单类型的就会报错:

    TypeError: <__main__.A instance at 0x109d553b0> is not JSON serializable

其实Python的class也十分方便JSON序列化,需要一小段代码就可以:

    import json
    from json import JSONEncoder

    def obj2dict(obj):
        memberlist = [m for m in dir(obj)]
        _dict = {}
        for m in memberlist:
            if m[0] != "_" and not callable(m):
                _dict[m] = getattr(obj, m)

        return _dic

    class ClsEncoder(JSONEncoder):
        def default(self, o):
            return obj2dict(o)


    json.dumps(a, cls=ClsEncoder)

在使用json.dumps的时候指定ClsEncoder就能够达到目的