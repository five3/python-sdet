import logging


class Plugins:
    def fire(self, context):
        for p in self.events:
            if p['source'] == context['source'] and p['target'] == context['target']:
                logging.info(f"匹配成功：{p}")
                exec(p['content'])

    def register(self, p):
        self.events.append(p)

    def clear(self):
        self.events = []


class PRE_PROXY(Plugins):
    def __init__(self):
        self.events = []


class POST_PROXY(Plugins):
    def __init__(self):
        self.events = []


pre_proxy = PRE_PROXY()
post_proxy = POST_PROXY()

