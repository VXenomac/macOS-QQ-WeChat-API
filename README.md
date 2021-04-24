# macOS-WeChat-API

## 什么是 macOS-WeChat-API？

macOS-WeChat-API 是基于 [WeChatPlugin-MacOS](https://github.com/TKkk-iOSer/WeChatPlugin-MacOS) 的使用封装，WeChatPlugin-MacOS 使用`GCDWebServer`在本地`127.0.0.1`监听`52700`端口作为 Web 服务器，用于获取用户好友、获取聊天记录、打开与指定好友的聊天窗口、对指定好友发送任意消息。

## 使用场景

Telegram、Slack、Discord、飞书等应用中的机器人扩展了工具的边界，提升了效率，但微信官方始终不支持微信机器人。为此，本工具基于 TK 大佬几年前开发的插件上进行使用封装，可在包括但不局限于以下场景中使用：

1. 给指定的人在指定的时间发送指定的消息
2. 给群组推送加密货币最新价格
3. 群发消息
4. ……

## 使用限制

1. macOS
2. 安装[Alfred](https://www.alfredapp.com)
3. 安装[WeChatExtension-ForMac](https://github.com/MustangYM/WeChatExtension-ForMac)
4. 安装https://github.com/TKkk-iOSer/wechat-alfred-workflow
5. 在微信插件中打开`小助手`->`开启 Alfred 功能`

## 使用方法

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

6. 在显示名称为汪汪汪的联系人/群组发送消息

```python
wechat.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊')
```

7. 给 userId 为 DogeCoin 和 ElonMusk 的联系人/群组发送消息

```python
wechat.send_message_by_ids(['DogeCoin', 'ElonMusk'], 'Everything to the moon!')
```

