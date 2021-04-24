import requests


class WeChat:

    def __init__(self):
        self.BASE_URL = 'http://127.0.0.1:52700/wechat-plugin/'
        # [GET] 最近聊天列表，可选参数: [keyword]
        self.USER_URL = self.BASE_URL + 'user'
        # [GET] 根据用户 id 查询指定数量聊天记录，可选参数：[userId, count]
        self.CHAT_LOG_URL = self.BASE_URL + 'chatlog'
        # [POST] 根据用户 id 发送消息，可选参数：[userId, content, srvId]（Content-Type: application/x-www-form-urlencoded）
        self.SEND_MESSAGE_URL = self.BASE_URL + 'send-message'
        # [POST] 打开与指定好友的聊天窗口，参数：[userId]（Content-Type: application/x-www-form-urlencoded）
        self.OPEN_SESSION_URL = self.BASE_URL + 'open-session'

    def _get_user_id_by_name(self, users, name):
        """根据名称获取 userId

        Args:
            users (list): 用户字典列表
            name (str): 待匹配的名称

        Return:
            list: 待匹配名称对应 userId
        """
        return [
            user['userId']
            for user in users
            if name == user['title'].replace('[群聊]', '').split('(')[0]
        ]

    def search_user_by_keyword(self, keyword):
        """根据关键词搜索用户

        Args:
            keyword (str): 关键词

        Returns:
            dict: 用户相关信息列表
        """
        return requests.get(self.USER_URL, params={"keyword": keyword}).json()

    def search_user_by_name(self, name, group=False):
        """根据名称获取 userId

        Args:
            name (str): 待匹配的名称
            group (bool, optional): 是否多选，默认为 False，若 False 在匹配多个情况下默认返回最近的联系人

        Returns:
            list: userId 列表
        """
        r = requests.get(self.USER_URL).json()
        user_ids = self._get_user_id_by_name(r, name)
        if not user_ids:
            return []
        if group:
            return user_ids
        else:
            return [user_ids[0]]

    def get_chat_log_by_name(self, name, count):
        """根据待匹配名称获取聊天记录

        Args:
            name (str): 用户 userId
            count (int): 返回聊天记录条目数

        Raises:
            ValueError: 待匹配名称重复，例如有两个相同的人名

        Returns:
            dict: 聊天记录字典
        """
        user_ids = self.search_user_by_name(name, group=True)
        if len(user_ids) > 1:
            raise ValueError("用户 ID 数量大于 1，请检查是否同名")
        r = requests.get(self.CHAT_LOG_URL, params={
                         "userId": user_ids, "count": count})
        if r:
            return {i['subTitle']: i['copyText'] for i in r.json()[:1:-1]}
        else:
            return {}

    def get_chat_log_by_id(self, user_id, count):
        """根据 userId 获取聊天记录

        Args:
            user_id (int): 用户 userId
            count (int): 返回聊天记录条目数

        Returns:
            dict: 聊天记录字典
        """
        r = requests.get(self.CHAT_LOG_URL, params={
                         "userId": user_id, "count": count})
        if r:
            return {i['subTitle']: i['copyText'] for i in r.json()[:1:-1]}
        else:
            return {}

    def send_message_by_name(self, name, content, srvId=1, group=False):
        """通过待匹配名称发送消息

        Args:
            name (str): 待匹配名称
            content (str): 待发送的消息
            srvId (int, optional): Defaults to 1.
            group (bool, optional): 是否群发，默认 False

        Returns:
            bool: 布尔值
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        user_ids = self.search_user_by_name(name, group=group)
        for user_id in user_ids:
            r = requests.post(self.SEND_MESSAGE_URL, headers=headers, data={
                              "userId": user_id, "content": content, "srvId": srvId})
        return True

    def send_message_by_ids(self, user_ids, content, srvId=1):
        """通过 userId 发送消息

        Args:
            user_ids (list): 需要发送消息的 userId 列表
            content (str): 待发送的消息
            srvId (int, optional): [int]. Defaults to 1.

        Returns:
            bool: 布尔值
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        for user_id in user_ids:
            r = requests.post(self.SEND_MESSAGE_URL, headers=headers, data={
                              "userId": user_id, "content": content, "srvId": srvId})
        return True


if __name__ == '__main__':
    wechat = WeChat()
    print(wechat.search_user_by_keyword('狗狗币')) # 搜索显示名称为狗狗币的联系人/群组（速度较慢）
    print(wechat.search_user_by_name('狗狗币')) # 搜索显示名称为狗狗币的联系人/群组（速度较快）
    print(wechat.get_chat_log_by_name('狗狗币', 5)) # 返回与狗狗币最近的五条聊天记录
    print(wechat.get_chat_log_by_id('DogeCoin', 5)) # 返回与 userId 为 dogecoin 的最近的五条聊天记录
    print(wechat.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊')) # 在显示名称为汪汪汪的联系人/群组发送消息
    print(wechat.send_message_by_ids(['DogeCoin', 'ElonMusk'], 'Everything to the moon!')) # 给 userId 为 DogeCoin 和 ElonMusk 的联系人/群组发送消息
    
