```
上海市
shanghaishi
JtDtu1gi


奉贤区
fengxianqu  
ZEo2iitt  


institution user
david
Btn0T7kz
```



### 修改后台

```sql
# 机构数据修改
SELECT  id,license_num,institution_name,way FROM  institution_import_data  WHERE license_num = 'Y0181403300'
SELECT  id,COMMIT  FROM  institution_other_new  WHERE  id = 2765
# way 字段修改为t

# 药店修改数据
SELECT  *  FROM "Shdistrict_in"  WHERE licence_num = 'YD832512826'
SELECT  licence_num,way FROM  "YD_show"  WHERE  licence_num  = 'YD832512826'
# way 字段修改为现场检查

```



### inspectdb

```python
# --database default 用于修改数据库
python manage.py --database default tablename1,tablename2  > aoppname/models.py
```



### Listen failure: Couldn't listen on xxxx

```shell
$ lsof -i:8107
COMMAND     PID       USER   FD   TYPE    DEVICE SIZE/OFF NODE NAME
python3.7 17797 MidspDbDev   11u  IPv4 390457552      0t0  TCP localhost.localdomain:8107 (LISTEN)
$ kill -9 17797
```



### nginx

```shell
# 重启服务
service nginx restart
```



### postgresql

#### 查询最大id

```sql
select max(id) from gis_sys_yaodian_all_190814;
```



### update

```sql
UPDATE institution_other_new 
SET sq1420 = ( SELECT sq1420 FROM institution_self_new WHERE institution_self_new.ID = institution_other_new.ID )
```



#### id自增

```sql
select setval('all_user_id_seq', (SELECT max(id) FROM all_user));


select setval('all_user_id_seq', 10000);

```



#### UPDATE

```sql
SELECT * FROM gis_sys_yaodian_all_190814 WHERE ydm like  '上海复美安鑫%';

Update
gis_sys_yaodian_all_190814
set address = 'xxxxx',
lng_wgs = 'xxx',lat_wgs='xxx',
geom = st_geomfromtext('point(xxx xxx)',4326) 
where gid = xxx and id = xxx;
```



#### 插入

字段名称不需要添加引号，插入值添加单引号

```sql
INSERT INto
all_user
SELECT id,password, last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined FROM "users_user" WHERE username like '%qu' or  username = 'shanghaishi'
```



#### join

* 内连接

```sql
SELECT 
gis_sys_yaodian_all_190814.*,"Shdistrict_in".*
FROM "gis_sys_yaodian_all_190814"  
INNER JOIN "Shdistrict_in" 
ON gis_sys_yaodian_all_190814.gsp = "Shdistrict_in".licence_num  
where 
"Shdistrict_in"."zone" = '奉贤区';
```



### Django restframe

#### 前后端分离

* 交互形式
    * 前端通过不同的请求方式，向后端发送请求，
    * 后端只相应对应的json或者xml类型数据
* 代码组织方式
* 开发模式
* 数据接口规范流程

#### Json

```python
for item in queryset:
	data.append(model_to_dict(item))
    
data = json.dumps((list(data.values())))
```



#### ViewSet中实现的方法

* list # get请求，返回全部查询
* create # post请求，处理表单提交的数据
* retrieve # get请求，通过pk查询单个信息
* update # patch请求，通过pk修改数据
* destroy # delete请求，通过pk删除数据



#### 注册

```python
# 注册序列化器
class RegisterUserSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(label='确认密码', write_only=True)

    class Meta:
        model = InstitutionUser
        exclude = ['last_login', 'first_name', 'last_name', 'is_staff', "groups", "user_permissions"]

        # 修改字段选项，以及自定义校验错误信息
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 32,
                # 'error_message': {
                #     'min_length': '用户名的长度不能小于5位字符',
                #     'max_length': '用户名的长度不能大于32位长度',
                # }
            },
            # 只做序列化输出
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 32,
            },
        }

    # def validate_mobile(self, value):
    #     if not re.match(r'1[3-9]\d{9}$', value):
    #         raise serializers.ValidationError('手机号格式有误')
    #     return value
    #
    # def validate_allow(self, value):
    #     if value != 'true':
    #         raise serializers.ValidationError('请同意用户协议')
    #     return value

    def validate(self, attrs):
        """ 密码是否一致 """
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs

    def create(self, validated_data):
        del validated_data['password_2']
        password = validated_data.pop('password')
        user = InstitutionUser()
        user.set_password(password)
        return user
```



#### jwt

https://pythonav.com/

##### 应用场景

* 前后端分离项目


##### 原理

* 用户提交用户名和密码给服务端，若果登录成功，使用jwt创建一个token，并返回给用户


```
eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjA4NTYyMDU3fQ.jAoQvBbjWUGZqrgRIx8T4fch_gc-tJbcIc29PrpK6VM
```

注意：jwt生成的 token 是由三段字符串组成，并使用 . 连接起来	

* 第一段字符串，HEADER，内部包含加密算法和 token 类型

    json转换为字符串，然后做 base64 url 加密

    ```json
    {
    	'alg':'HS256',
    	'typ':'JWT'
    }
    ```

* 第二段字符串 payload  自定义返回给前端的值

    json转换为字符串，然后做 base64 url 加密

    ```python
    {
    	'id':'11111',
    	'username':'xxxxx',
    	'exp':1213123123123123,# 过期时间
    }
    ```

* 第三段字符串

    ```
    第一步：将第1、2部分的密文字符串拼接起来
    
    第二步：对前两部分的密文进行hs256加密 + 加盐
    
    第三步：对HS256加密后的密文在做 base64 url 加密
    ```

* 以后用户再来访问的时候，需要携带token，后端需要对token进行检验

    * 获取token

    * 第一步：对token进行切割

    * 第二步：对第二段进行 base64 url 解密，并获取 payload 信息，检测 token 是否过期

    * 第三步：把第1、2段拼接起来，再次执行 HS256 加密

        ```
        第一步：第1、2部分密文拼接起来
        
        第二步：对前2部分密文进行HS256 加密 + 加盐
        
        如果加密后的密文与第三部分一致，则认证成功
        ```

##### 应用

```python
pip install pyjwt
```

* 在 app 模块下创建 token 校验机制 authentication.py 文件

* 在 app 模块内的 urls 路由内

    ```python
    # 此种注册方式，只可以使用默认的认证机制，只能返回token
    url(r'^api-token-auth/', obtain_jwt_token),# 获取登录后的token
    url(r'^api-refresh-token/', refresh_jwt_token),# 更新
    url(r'^api-token-verify/', verify_jwt_token),
    ```

* settings 文件

    ```python
    JWT_AUTH = {
        # 可以重写 JWT_RESPONSE_PAYLOAD_HANDLER，即可使用自定义的 token 返回数据类型
        # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
        # how long the original token is valid for
        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
    
        # allow refreshing of tokens
        'JWT_ALLOW_REFRESH': True,
    
        # this is the maximum time AFTER the token was issued that
        # it can be refreshed.  exprired tokens can't be refreshed.
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    }
    ```

    ```python
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            # 全局配置，默认全部接口生效
            'InstitutionUser.authentication.JwtQueryParamsAuthentication',
        ],
    }
    ```

* views集使用

    settings配置的时候，使用的是全局配置，因此默认每个视图接受认证【局部认证的权限高于全局的认证】

####  跨域

##### 原因

浏览器遵守同源策略，只有浏览器才能存在跨域问题

##### 同源策略

协议:ip/域名:端口完全一致

#####  解决方案

* 浏览器检测 response 中是否存在 **Access-Control-Allow-Orign**，若存在可以解决跨域方案。CORS

    * 安装第三方插件

        ```shell
        pip install django-cors-headers
        ```

    * settings.py

        ```python
        INSTALLED_APPS = [
            'corsheaders',  # 跨域配置
        ]
        
        MIDDLEWARE = [ 
            # 注意优先级顺序
            'corsheaders.middleware.CorsMiddleware', 
        ]
        
        # 白名单
        CORS_ALLOW_CREDENTIALS = True
        # 允许携带 cookie
        CORS_ORIGIN_ALLOW_ALL = True
        CORS_ORIGIN_WHITELIST = (
            '*',
        	'127.0.0.1:8080',
        )
        
        ```

* 使用代理



#### celery 异步框架

```
celery -A celery_tasks.main worker -l info
```







### Git

```shell
# 生成的公钥在 Administrator/.ssh/id_rsa.pub
ssh-kengen -t rsa -C 'github email address'

# 将生成的公钥放在github account settings SSH & GPG KEY
```



```shell
# 配置初始化信息
git config --global user.name 'guopeiqing'

git config --global user.email 'guopeiqing@git.com'
```



```shell
# 创建一个新的仓库，当前路径
git init

# 添加文件，将文件交给git管理,
git add .

# 提交 简单概要
git commit -m 'xxxx提交操作的内容'

# 提交到github,后面地址为github仓库中的ssh地址
git remote add origin git@github.com:xxxxx/runoob-git-test.git

# 上传
git push -u origin branch
```



```shell
# 解决远端存在的文件，本地不存在问题
#  ! [rejected]        master -> master (fetch first)
# error: failed to push some refs to 'git@github.com:Zswdhy/MedicalCatalogue.git'
git pull --rebase origin master

#  ! [rejected]        master -> master (non-fast-forward)
# error: failed to push some refs to 'git@github.com:Zswdhy/MedicalCatalogue.git'
git pull origin master --allow-unrelated-histories


# 克隆远端文件，默认为当前目录
git pull remote-url branch
```



```shell
# 克隆项目
$ git clone git@github.com:mazhenkai/MedicalCatalogue.git

# 创建同分支
$ git checkout Guo_dev

$ cd MedicalCatalogue/McBackEnd/BackApis/
# 添加文件
$ git add urls.py  views.py
# 注释
$ git commit -m ' 返回当前树节点 '
# 提交
$ git push origin Guo_dev
```

