import re
import os
import logging
from io import StringIO
from html.parser import HTMLParser
from pathlib import Path

if os.getenv('ENVIRONMENT') == 'k8s':
    MASTO_USERNAME = '@' + Path('/etc/watcher-config-vol/masto.username').read_text()
    SERVER = '@' + Path('/etc/watcher-config-vol/masto.domain').read_text()
else:
    MASTO_USERNAME = '@' + os.getenv('EV_MASTO_USERNAME') 
    SERVER = '@' + os.getenv('EV_MASTO_DOMAIN')

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def cleanup(content, start, end):
    return strip_tags(content).replace(MASTO_USERNAME, '').replace(SERVER, '').replace(start, '').replace(end, '').replace(r'\\', '').strip()


def get_content(msg):
    # Sometimes the data in the SSE msg is truncated so we can't assume it's well-formed json for parsing (e.g. when coming from Firefish account).
    start = r'"content":"'
    end = r'","filtered"'
    content_re = r'"content":".+","filtered"'
    mention_re = r'"type":"mention"'

    found = re.search(mention_re, msg)
    if found:
        # It's a mention.
        found = re.search(content_re, msg)
        return cleanup(found.group(), start, end)
    else:
        logging.debug("NOT a mention")
        return None

def get_status_id(msg):
    # Sometimes the data in the SSE msg is truncated so we can't assume it's well-formed json for parsing (e.g. when coming from Firefish account).
    start = r'"status":{"id":"'
    end = r'","created_at"'
    status_re = r'"status":{"id":"[0-9]+","created_at"'

    found = re.search(status_re, msg)
    return cleanup(found.group(), start, end)

def get_account(msg):
    # Sometimes the data in the SSE msg is truncated so we can't assume it's well-formed json for parsing (e.g. when coming from Firefish account).
    
    # The "acct - display_name" section appears more than once so to avoid grabbing everything in between
    # we first trim the message down so it only contains one occurrence
    start = r'"acct":"'
    end = r'"status"'
    account_re = r'"acct":".+"status"'

    found = re.search(account_re, msg)
    msg = found.group()
    end = end = r'","display_name"'
    account_re = r'"acct":".+","display_name"'

    found = re.search(account_re, msg)

    return '@' + cleanup(found.group(), start, end)