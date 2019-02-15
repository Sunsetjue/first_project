# 编写自定义过滤器
# 过滤器最多只有两个参数

from django import template
from datetime import datetime
from django.utils.timezone import now,localtime

register = template.Library()

def changes(value, word):
    return value + "是个" + word

# 绑定
register.filter("changes", changes)



'''
time距离现在的时间间隔
1. 如果时间间隔小于1分钟以内，那么就显示“刚刚”
2. 如果是大于1分钟小于1小时，那么就显示“xx分钟前”
3. 如果是大于1小时小于24小时，那么就显示“xx小时前”
4. 如果是大于24小时小于30天以内，那么就显示“xx天前”
5. 否则就是显示具体的时间 2017/10/20 16:15
'''
@register.filter()
def since_time(value):
    if isinstance(value,datetime):
        time_cut = (now() - value).total_seconds() # total_seconds()返回一个时间差的秒数
        if time_cut <= 60 :
            return "刚刚"
        elif time_cut > 60 and time_cut < 60*60:
            return str(int(time_cut/60)) + "分钟前"
        elif time_cut >= 60 and time_cut < 60*60*24:
            return str(int(time_cut/3600)) + "小时前"
        elif time_cut >= 24*60*60 and time_cut <= 24*60*60*30:
            return str(int(time_cut/60/60/24)) + "天前"
        else:
            return value.strftime('%Y-%m-%d %H:%M:%S')

@register.filter()
def time_zh(value):
    if isinstance(value, datetime):
        return localtime(value).strftime('%Y-%m-%d %H:%M:%S')