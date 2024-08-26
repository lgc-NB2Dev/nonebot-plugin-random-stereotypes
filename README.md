<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

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
  <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_random_stereotypes.svg" alt="license">
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

|                配置项                | 必填 |       默认值       |                                       说明                                       |
| :----------------------------------: | :--: | :----------------: | :------------------------------------------------------------------------------: |
|             **全局配置**             |      |                    |                                                                                  |
|             `SUPERUSERS`             |  否  |        `[]`        |                  超级用户 ID 列表，本插件中超级用户无视冷却限制                  |
|             **冷却配置**             |      |                    |                                                                                  |
|           `STEREOTYPES_CD`           |  否  |       `1800`       |                            触发冷却后的冷却时间（秒）                            |
|         `STEREOTYPES_COUNT`          |  否  |        `3`         | 在 `STEREOTYPES_COUNT_TIME`（单位秒）中触发超过 `STEREOTYPES_COUNT` 次则触发冷却 |
|       `STEREOTYPES_COUNT_TIME`       |  否  |       `1800`       |                                       如上                                       |
|      `STEREOTYPES_PUNISH_COUNT`      |  否  |        `5`         |                 当在冷却中继续触发指令超过此次数将会重置冷却时间                 |
|      `STEREOTYPES_CD_KEY_TYPE`       |  否  |       `user`       |    冷却时间标识符，可选 `user`（只分用户冷却）或 `session`（分群与用户冷却）     |
|             **消息配置**             |      |                    |                                                                                  |
| `STEREOTYPES_SHOW_TRIGGER_USER_NAME` |  否  |       `True`       |                          是否在消息中展示触发的用户昵称                          |
|             **指令配置**             |      |                    |                                                                                  |
|        `STEREOTYPES_ALIASES`         |  否  | `["发电", "发癫"]` |                                   附加指令前缀                                   |
|        `STEREOTYPES_PRIORITY`        |  否  |       `100`        |                                  Matcher 优先级                                  |
|         `STEREOTYPES_BLOCK`          |  否  |      `False`       |                       是否阻止事件向低优先级 Matcher 传递                        |

## 🎉 使用

![Example](https://raw.githubusercontent.com/Ikaros-521/nonebot_plugin_random_stereotypes/master/assets/QQ20240826-190322.png)

<!--
## 📞 联系

QQ：3076823485
Telegram：[@lgc2333](https://t.me/lgc2333)
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)
邮箱：<lgc2333@126.com>
-->

<!--
## 💡 鸣谢

如果有要鸣谢的人的话
-->

<!--
## 💰 赞助

**[赞助我](https://blog.lgc2333.top/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！
-->

## 📝 更新日志

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
