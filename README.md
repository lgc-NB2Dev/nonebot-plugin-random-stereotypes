<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_random_stereotypes

_✨ NoneBot 发病语录 ✨_


<a href="https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_random_stereotypes?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_random_stereotypes?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_random_stereotypes?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_random_stereotypes.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_random_stereotypes">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_random_stereotypes.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

## 📖 介绍

随机返回一条在互联网上收录一些有趣的发病语录（主要针对VTB）  
如果有需要补充的可以提交issue进行追加，侵删。  

## 💿 安装  

### 1. nb-cli安装（推荐）

在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  

```sh
nb plugin install nonebot_plugin_random_stereotypes
```

### 2. 本地安装

将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_random_stereotypes`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：

```sh
git clone https://github.com/Ikaros-521/nonebot_plugin_random_stereotypes.git
```

也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_random_stereotypes`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_random_stereotypes/__init__.py```  

### 3. pip安装

```sh
pip install nonebot_plugin_random_stereotypes
```  

打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_random_stereotypes')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_random_stereotypes```即可  
pyproject.toml配置例如：  

``` toml
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_random_stereotypes"]
```

### 更新版本

```sh
nb plugin update nonebot_plugin_random_stereotypes
```

## 🔧 配置

不需要喵

## 🎉 功能

随机生成下标获取本地`data.py`中的一条语录，凭借传入的字符串返回结果。

## 👉 命令

### /发病

命令结构：```/发病 [发病对象]```  
例如：```/发病 测试```  
bot返回内容：  
`电梯里遇到了测试，她按了八层，呵真会暗示，她八层有点喜欢我`  

## ⚙ 拓展

自定义发病语录，修改`data.py`文件，在数组中添加语句即可，对象名用 `{target_name}` 代替，注意格式！  

## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布  

### 0.0.2

- 追加发病语录数据  

</details>

## 🔧 开发环境

Nonebot2：2.0.0rc3  
python：3.8.13  
操作系统：Windows10（Linux兼容性问题不大）  
编辑器：VS Code  

## 致谢

- [nonebot-plugin-template](https://github.com/A-kirami/nonebot-plugin-template)

## 项目打包上传至pypi

官网：https://pypi.org，注册账号，在系统用户根目录下创建`.pypirc`，配置

```txt
[distutils] 
index-servers=pypi 
 
[pypi] repository = https://upload.pypi.org/legacy/ 
username = 用户名 
password = 密码
```

### poetry

```sh
# 参考 https://www.freesion.com/article/58051228882/
# poetry config pypi-token.pypi

# 1、安装poetry
pip install poetry

# 2、初始化配置文件（根据提示填写）
poetry init

# 3、微调配置文件pyproject.toml

# 4、运行 poetry install, 可生成 “poetry.lock” 文件（可跳过）
poetry install

# 5、编译，生成dist
poetry build

# 6、发布(poetry config pypi-token.pypi 配置token)
poetry publish
```

### twine

```sh
# 参考 https://www.cnblogs.com/danhuai/p/14915042.html
#创建setup.py文件 填写相关信息

# 1、可以先升级打包工具
pip install --upgrade setuptools wheel twine

# 2、打包
python setup.py sdist bdist_wheel

# 3、可以先检查一下包
twine check dist/*

# 4、上传包到pypi（需输入用户名、密码）
twine upload dist/*
```
