import requests

def sms_captcha_sender(telephone, captcha):
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": telephone,
        "tpl_id": "133779",
        "tpl_value": '#code#=' + captcha,
        "key": 'e98a278260b7961797aabf1abf9515f6'
    }
    response = requests.get(url, params=params)

    result = (response.json())
    if result["error_code"] == 0:
        return True
    else:
        return False