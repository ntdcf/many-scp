# many-scp
简单的批量上传文件脚本

* conf 目录用来配置上传项目相关配置，可以一次性上传多个配置的内容
* host 模块 固定配置，要上传的服务器信息
* 之后的每个模块都有模块名称，和如下三个配置
``cfg
local_file = /home/user/example
remote_file_path = /usr/local/example/
file_name = exampleapp
```
* 运行程序的时候程序参数带模块名，可带多个模块名，如：
```
python scp.py test
```
* 本程序运行在python3环境下，需要 paramiko 模块依赖