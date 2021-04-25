import requests


class QQ:

    def __init__(self):
        self.BASE_URL = 'http://127.0.0.1:52777/QQ-plugin/'
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

    def get_chat_log_by_name(self, name, user_type=1):
        """根据待匹配名称获取聊天记录

        Args:
            name (str): 用户 userId
            user_type (int, optional): 用户类型，默认为 1，用户为 1，群聊为 101

        Raises:
            ValueError: 待匹配名称重复，例如有两个相同的人名

        Returns:
            dict: 聊天记录字典
        """
        user_ids = self.search_user_by_name(name, group=True)
        if len(user_ids) > 1:
            raise ValueError("用户 ID 数量大于 1，请检查是否同名")
        r = requests.get(self.CHAT_LOG_URL, params={
                         "userId": user_ids, "type": user_type})
        if r:
            return {i['subTitle']: i['title'] for i in r.json()[:1:-1]}
        else:
            return {}

    def get_chat_log_by_id(self, user_id, user_type=1):
        """根据 userId 获取聊天记录

        Args:
            user_id (int): 用户 userId
            user_type (int, optional): 用户类型，默认为 1，用户为 1，群聊为 101

        Returns:
            dict: 聊天记录字典
        """
        r = requests.get(self.CHAT_LOG_URL, params={
                         "userId": user_id, "type": user_type})
        if r:
            return {i['subTitle']: i['title'] for i in r.json()[:1:-1]}
        else:
            return {}

    def send_message_by_name(self, name, content, user_type=1, group=False):
        """通过待匹配名称发送消息

        Args:
            name ([type]): [description]
            content ([type]): [description]
            user_type (int, optional): 用户类型，默认为 1，用户为 1，群聊为 101
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
                              "userId": user_id, "content": content, "type": user_type})
        return True

    def send_message_by_ids(self, user_ids, content, user_type=1):
        """通过 userId 发送消息

        Args:
            user_ids (list): 需要发送消息的 userId 列表
            content (str): 待发送的消息
            user_type (int, optional): 用户类型，默认为 1，用户为 1，群聊为 101

        Returns:
            bool: 布尔值
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        for user_id in user_ids:
            r = requests.post(self.SEND_MESSAGE_URL, headers=headers, data={
                              "userId": user_id, "content": content, "type": user_type})
        return True


if __name__ == '__main__':
    qq = QQ()
    print(qq.search_user_by_name('狗狗币'))  # 搜索显示名称为狗狗币的联系人/群组
    print(qq.get_chat_log_by_name('狗狗币', 1))  # 返回与狗狗币最近的五条聊天记录
    # 返回与 userId 为 DogeCoin 联系人的最近的五条聊天记录
    print(qq.get_chat_log_by_id('DogeCoin', 1))
    # 返回与 userId 为 DogeCoin 群组的最近的五条聊天记录
    print(qq.get_chat_log_by_id('DogeCoin', 101))
    # 在显示名称为汪汪汪的联系人发送消息
    print(qq.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊'), 1)
    # 在显示名称为汪汪汪的群组发送消息
    print(qq.send_message_by_name('汪汪汪', '哟，这不狗狗币么，几天不见，这么拉了啊'), 101)
    # 给 userId 为 DogeCoin 和 ElonMusk 的联系人发送消息
    print(qq.send_message_by_ids(
        ['DogeCoin', 'ElonMusk'], 'Everything to the moon!'), 1)
    # 给 userId 为 DogeCoin 和 ElonMusk 的群组发送消息
    print(qq.send_message_by_ids(
        ['DogeCoin', 'ElonMusk'], 'Everything to the moon!'), 101)
