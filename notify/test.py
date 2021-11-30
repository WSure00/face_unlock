#! /usr/bin/env python
import os

def notify(title,message):
    os.environ.setdefault('DISPLAY', ':0.0')
    os.system('notify-send -i "notification-message-IM" "'+title+'" "'+message+'"')

notify("alipay","支付宝到账, 1000万元")