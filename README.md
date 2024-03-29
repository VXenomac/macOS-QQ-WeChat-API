# macOS-QQ-WeChat-API

## 什么是 macOS-QQ-WeChat-API？

本项目由两部分组成：macOS-QQ-API 以及 macOS-WeChat-API。

macOS-QQ-API 是基于 [QQPlugin-macOS ](https://github.com/TKkk-iOSer/QQPlugin-macOS)的使用封装，QQPlugin-macOS 使用`GCDWebServer`在本地`127.0.0.1`监听`52777`端口作为 Web 服务器，用于获取用户好友、获取聊天记录、打开与指定好友的聊天窗口、对指定好友发送任意消息。

macOS-WeChat-API 是基于 [WeChatPlugin-MacOS](https://github.com/TKkk-iOSer/WeChatPlugin-MacOS) 的使用封装，WeChatPlugin-MacOS 使用`GCDWebServer`在本地`127.0.0.1`监听`52700`端口作为 Web 服务器，用于获取用户好友、获取聊天记录、打开与指定好友的聊天窗口、对指定好友发送任意消息。

## 使用场景

Telegram、Slack、Discord、飞书等应用中的机器人扩展了工具的边界，提升了效率，但QQ、微信官方始终不支持微信机器人。QQ、微信已经成为日常通讯信息最重要的入口，直接发送通知消息至 QQ、微信将会降低工具切换之间带来的消息延迟。为此，本工具基于 TK 大佬几年前开发的插件进行使用封装，可在包括但不局限于以下场景中使用：

1. 给指定的人在指定的时间发送指定的消息
2. 给群组推送加密货币最新价格、价格变动情况
3. 群发消息
4. ……

## 通用使用限制

1. macOS
2. 需要安装 [Alfred](https://www.alfredapp.com)

## macOS-QQ-API 使用限制

1. 需要安装 [QQPlugin-macOS ](https://github.com/TKkk-iOSer/QQPlugin-macOS)
2. 需要安装 [QQ-alfred-workflow](https://github.com/TKkk-iOSer/QQPlugin-macOS/blob/master/Other/QQ%20Plugin.alfredworkflow)
3. 在 QQ 插件中打开`开启 alfred`

## macOS-WeChat-API 使用限制

1. 需要安装[WeChatExtension-ForMac](https://github.com/MustangYM/WeChatExtension-ForMac)
2. 需要安装[wechat-alfred-workflow](https://github.com/TKkk-iOSer/wechat-alfred-workflow)
3. 在微信插件中打开`小助手`->`开启 Alfred 功能`



## macOS-QQ-API 使用方法

1. 初始化 QQ

```python
from qq import QQ


qq = QQ()
```

2. 搜索显示名称为狗狗币的联系人/群组

```python
qq.search_user_by_name('狗狗币')
```

3. 返回与狗狗币最近的五条聊天记录

```python
qq.get_chat_log_by_name('狗狗币', 1)
```

4. 返回与 userId 为 DogeCoin 联系人的最近的五条聊天记录

```python
qq.get_chat_log_by_id('DogeCoin', 1)
```

5. 返回与 userId 为 DogeCoin 群组的最近的五条聊天记录

```python
qq.get_chat_log_by_id('DogeCoin', 101)
```

6. 给显示名称为汪汪汪的联系人发送消息

```python
qq.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊', 1)
```

7. 给显示名称为汪汪汪的群组发送消息

```python
qq.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊', 101)
```

8. 给 userId 为 DogeCoin 和 ElonMusk 的联系人发送消息

```python
qq.send_message_by_ids(
        ['DogeCoin', 'ElonMusk'], 'Everything to the moon!', 1)
```

9. 给显示名称为汪汪汪的群组发送消息

```python
qq.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊', 101)
```

## macOS-WeChat-API 使用方法

1. 初始化 WeChat

```python
from wechat import WeChat


wechat = WeChat()
```

2. 搜索显示名称为狗狗币的联系人/群组（速度较慢）

```python
wechat.search_user_by_keyword('狗狗币')
```

3. 搜索显示名称为狗狗币的联系人/群组（速度较快）

```python
wechat.search_user_by_name('狗狗币')
```

4. 返回与狗狗币最近的五条聊天记录

```python
wechat.get_chat_log_by_name('狗狗币', 5)
```

5. 返回与 userId 为 dogecoin 的最近的五条聊天记录

```python
wechat.get_chat_log_by_id('DogeCoin', 5)
```

6. 给显示名称为汪汪汪的联系人/群组发送消息

```python
wechat.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊')
```

7. 给 userId 为 DogeCoin 和 ElonMusk 的联系人/群组发送消息

```python
wechat.send_message_by_ids(['DogeCoin', 'ElonMusk'], 'Everything to the moon!')
```

