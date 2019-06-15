Title: 使用 Python 操作亚马逊 S3
Date: 2015-08-17 20:20
Modified: 2015-08-17 20:20
Category: Python
Tags: s3, aws
Slug: python-operate-s3
Authors: Martin
Summary: 使用 Python 操作亚马逊 S3


亚马逊S3(Amazon Simple Storage Service) 为开发人员和IT团队提供安全、耐久且扩展性高的对象存储。 可以理解为一个在线的网盘，而且这个网盘可以通过程序上传，下载，获取外链。亚马逊按照存储空间和请求次数收费。

对小公司来说是一个稳定的在线存储,可以减少维护成本。

boto3 Python SDK
----------------

目前官方推荐的Python SDK 是boto3 <https://github.com/boto/boto3>

接下来进入正题,直接看代码把。:

    from boto3.session import Session

    session = Session(aws_access_key_id='<key>', \
        aws_secret_access_key='<key>', \
        region_name='us-east-1')

    s3 = session.resource('s3')
    client = session.client('s3')

    #上传
    data = open('~/beakup.gif', 'rb')
    file_obj = s3.Bucket('mybucket').put_object(Key='breakup.gif', Body=data)

    #获取URL
    presigned_url = client.generate_presigned_url(
        'get_object', Params={'Bucket': file_obj.bucket_name, 'Key': file_obj.key},
        ExpiresIn= 3600*30*12
    )

简单说明一下代码，S3

1.  create() 创建Bucket
2.  delete() 删除Bucket
3.  put\_object() 上传文件,Key是文件名,Body是文件内容
4.  delete\_object() 删除文件,Key是文件名

如何创建文件夹
--------------

对于对象存储而言，没有文件夹的概念，所有的文件以及文件夹都看成是一个object，但是object前面可以有字符“/”来表示文件夹意义的标示符， 因而本身s3是没有提供直接建文件夹的API的，但是利用前面的概念可以建一个结尾带有“/”的key，这个key的content为空，来象征性的标示文件夹， 后续所谓的往这个文件夹里面继续存放东西就是在所有需要上传文件的文件名前面加上这个文件夹的key作为文件的key将文件上传，就是先所谓的文件夹的概念。

其他
----

如果需要使用客户端操作s3，推荐小黄鸭cyberduck。