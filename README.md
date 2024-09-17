<!-- markdownlint-disable MD024 MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-Random-Stereotypes

_✨ 发病语录 ✨_

<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4778875-45a4-4688-8e1b-b8c844440abb">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4778875-45a4-4688-8e1b-b8c844440abb.svg" alt="wakatime">
</a>

<br />

<a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/pyd-v1-or-v2.json" alt="Pydantic Version 1 Or 2" >
</a>
<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-random-stereotypes.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-random-stereotypes">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-random-stereotypes.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-random-stereotypes">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-random-stereotypes" alt="pypi download">
</a>

<br />

<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-random-stereotypes:nonebot_plugin_random_stereotypes">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot-plugin-random-stereotypes" alt="NoneBot Registry">
</a>
<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-random-stereotypes:nonebot_plugin_random_stereotypes">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin-adapters%2Fnonebot-plugin-random-stereotypes" alt="Supported Adapters">
</a>

</div>

## 📖 介绍

随机返回一条在互联网上收录一些有趣的发病语录（主要针对 VTB）  
如果有需要补充的可以提交 issue 进行追加，侵删。

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-random-stereotypes
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-random-stereotypes
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-random-stereotypes
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-random-stereotypes
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-random-stereotypes
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_random_stereotypes"
]
```

</details>

## ⚙️ 配置

在 nonebot2 项目的 `.env` 文件中添加下表中的必填配置

|                配置项                | 必填 |                 默认值                 |                                       说明                                       |
| :----------------------------------: | :--: | :------------------------------------: | :------------------------------------------------------------------------------: |
|             **全局配置**             |      |                                        |                                                                                  |
|             `SUPERUSERS`             |  否  |                  `[]`                  |                  超级用户 ID 列表，本插件中超级用户无视冷却限制                  |
|             **冷却配置**             |      |                                        |                                                                                  |
|           `STEREOTYPES_CD`           |  否  |                 `1800`                 |                            触发冷却后的冷却时间（秒）                            |
|         `STEREOTYPES_COUNT`          |  否  |                  `3`                   | 在 `STEREOTYPES_COUNT_TIME`（单位秒）中触发超过 `STEREOTYPES_COUNT` 次则触发冷却 |
|       `STEREOTYPES_COUNT_TIME`       |  否  |                 `1800`                 |                                       如上                                       |
|      `STEREOTYPES_PUNISH_COUNT`      |  否  |                  `5`                   |                 当在冷却中继续触发指令超过此次数将会重置冷却时间                 |
|      `STEREOTYPES_CD_KEY_TYPE`       |  否  |                 `user`                 |    冷却时间标识符，可选 `user`（只分用户冷却）或 `session`（分群与用户冷却）     |
|             **消息配置**             |      |                                        |                                                                                  |
| `STEREOTYPES_SHOW_TRIGGER_USER_NAME` |  否  |                 `True`                 |                          是否在消息中展示触发的用户昵称                          |
|      **Meme 配置**（详见下方）       |      |                                        |                                                                                  |
|      `STEREOTYPES_ENABLE_MEME`       |  否  |                 `True`                 |         是否启用 Meme 功能，启用后将会在有 At 对象时附带生成一张表情包图         |
|      `STEREOTYPES_MEME_SOURCE`       |  否  |                 `auto`                 |               Meme 数据源，可选 `auto`（自动选择）、`embed`、`api`               |
|         `STEREOTYPES_MEMES`          |  否  | `["kiss","bite","rub","little_angel"]` |                                    表情包列表                                    |
|             **指令配置**             |      |                                        |                                                                                  |
|        `STEREOTYPES_ALIASES`         |  否  |           `["发电", "发癫"]`           |                                   附加指令前缀                                   |
|        `STEREOTYPES_PRIORITY`        |  否  |                 `100`                  |                                  Matcher 优先级                                  |
|         `STEREOTYPES_BLOCK`          |  否  |                `False`                 |                       是否阻止事件向低优先级 Matcher 传递                        |

### Meme 配置相关

Meme 功能默认启用，但是当没有可用数据源或初始化时遇到问题将会自动禁用  
当指令参数为 At 对象时才会触发此功能

#### `embed` 数据源配置

安装 [`meme-generator`](https://github.com/MeetWq/meme-generator)（或 [`nonebot-plugin-memes`](https://github.com/noneplugin/nonebot-plugin-memes)）即可使用

#### `api` 数据源配置

先安装 [`nonebot-plugin-memes-api`](https://github.com/noneplugin/nonebot-plugin-memes-api)  
安装后请按照其配置文档配置好 [`MEME_GENERATOR_BASE_URL`](https://github.com/noneplugin/nonebot-plugin-memes-api#meme_generator_base_url) 后即可使用

#### 表情包列表配置（`STEREOTYPES_MEMES`）

本配置项为一个字符串或 `MemeConfig` 列表，当元素为字符串时会自动转换为有默认配置的 `MemeConfig`

`MemeConfig` 包含以下字段：

- `name`（必填）: 表情名
- `target_first`（默认 `False`）：当需传入两张图片时，是否调换图片顺序使被 At 的用户在前
- `additional_images`（默认 `[]`）：额外的图片路径列表，会附加在传入图片后
- `additional_texts`（默认 `[]`）：额外传入的文字列表
- `additional_args`（默认 `{}`）：额外传入的参数字典

示例：

```properties
STEREOTYPES_MEMES='
[
  "little_angel",
  {
    "name": "call_110",
    "target_first": true
  },
  {
    "name": "addiction",
    "additional_texts": ["阿巴阿巴阿巴阿巴"]
  },
  {
    "name": "petpet",
    "additional_args": {
      "circle": true
    }
  }
]
'
```

## 🎉 使用

![Example](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/random-stereotypes/QQ20240826-190322.png)

## 📞 联系

### Ikaros

QQ: 327209194
邮箱：<327209194@qq.com>

### student_2333

QQ：3076823485
Telegram：[@lgc2333](https://t.me/lgc2333)
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)
邮箱：<lgc2333@126.com>

<!--
## 💡 鸣谢

如果有要鸣谢的人的话
-->

## 💰 赞助

### student_2333

**[赞助我](https://blog.lgc2333.top/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！

## 📝 更新日志

### 0.4.0

- 加入 meme 功能

### 0.3.0

- 重构

### 0.2.1

- 支持获取 At 对象的昵称作为发病对象

### 0.2.0

- 添加命令冷却
- 追加发病语录数据

### 0.1.0

- 重构

### 0.0.2 ~ 0.0.3

- 追加发病语录数据
