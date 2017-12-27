import re
from wechatpy.messages import TextMessage
from wechatpy import create_reply
from qqwry import QQwry


class CommandHandler:
    command = ''

    def check_match(self, message):
        if not isinstance(message, TextMessage):
            return False

        if not message.content.strip().lower().startswith(self.command):
            return False
        return True


class IpLocationHandler(CommandHandler):
    command = 'ip'

    def __init__(self):
        self.qqwry = QQwry()
        self.qqwry.load_file('qqwry.dats')
        self.msg = ''

    def handler(self, message):
        if not self.check_match(message):
            return

        ip = message.content.strip()
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

        if not re.match(pattern, ip):
            self.msg = 'IP地址无效'
        
        res = self.qqwry.lookup(ip)

        if res is None:
            self.msg = '未找到'
        else:
            self.msg = res[0]
        return create_reply(self.msg, message)

