Title: 遍历S3
Date: 2016-07-04 20:20
Modified: 2016-07-04 20:20
Category: Python
Tags: python, aws
Slug: boto-scan-s3
Authors: Martin
Summary: 使用 boto 遍历 s3

首先你需要一个有S3 list权限的key，如果bucket里面的文件很多的话，推荐使用分页来遍历

```python
session = boto3.Session(aws_access_key_id=<s3_aws_key_id>,
                            aws_secret_access_key=<s3_aws_secret_key>,
                            region_name='us-east-1')
    s3 = session.resource('s3')
    client = session.client('s3')
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=<s3_bucket>, Prefix=<s3_path_prefix>:
        for content in result.get('Contents'):
            if content.get('Size') > 0:
                print content.get('Key')
```

分页默认大小是1000，可以修改PageSize，改小可以减少响应时间

```python
paginator = client.get_paginator('list_objects')
page_iterator = paginator.paginate(Bucket='my-bucket',
                                   PaginationConfig={'PageSize': 100})
```


参考资料：
1. https://github.com/boto/boto3
2. https://boto3.readthedocs.io/en/latest/reference/services/s3.html#paginators
3. https://boto3.readthedocs.io/en/latest/guide/paginators.html
