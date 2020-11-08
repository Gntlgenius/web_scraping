from http.cookies import SimpleCookie


def cookie_parser():
    cookie_string = 'session-id=261-0165281-5042641; i18n-prefs=GBP; ubid-acbuk=258-2030534-2886328; lc-acbuk=en_GB; session-token=P2LjXVYYJCt0x9YOMkVCfLTvbl6sDad8Va8C0ZZZXMPqYQEya2fqtrSqbPioWD1fn1VfByzrHb8cKTeU5h9z120wwxxJqL1IPgjEQBnNoDYKH0tLf0e8ecE1fz/LOFZq6M/NiLRKHm5/8eJBGtcTwUIjKJ1kcjVB/PTzGdQrg9jLWLZuCfonuIZmbhP9GjF8; csm-hit=tb:YSBJTY3SBP5P6WA241T1+s-8WMYAGGHT9WC40TKQ2G3|1603432043951&t:1603432043951&adb:adblk_no; session-id-time=2082758401l'
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies_dict = {}

    for key, morsel in cookie.items():
        cookies_dict[key] = morsel.value


    return cookies_dict
