import calendar
from datetime import datetime


class Module(object):
    def __init__(self, sc):
        self.sc = sc


class System(Module):
    def init(self):
        r = self.sc._request("system", "init")

        token = r.get("token")

        if token:
            if self.sc._token:
                self.sc.auth.logout()

            self.sc._token = token

        return r


class Auth(Module):
    def login(self, username, password):
        if self.sc._token:
            self.logout()

        r = self.sc._request("auth", "login", {
            "username": username,
            "password": password
        })

        self.sc._token = r["token"]

        return r

    def logout(self):
        r = self.sc._request("auth", "logout")

        self.sc._token = None
        self.sc._session.cookies.clear()

        return r

    def save_fingerprint(self):
        return self.sc._request("auth", "saveFingerprint")


class Plugin(Module):
    def _get_page(self, action, size, offset, type, sort_field, sort_direction, filter_field, filter_string, since):
        if isinstance(since, datetime):
            since = calendar.timegm(since.utctimetuple())

        return self.sc._request("plugin", action, {
            "size": size,
            "offset": offset,
            "type": type,
            "sortField": sort_field,
            "sortDirection": sort_direction,
            "filterField": filter_field,
            "filterString": filter_string,
            "since": since
        })

    def init(self, size=None, offset=None, type=None, sort_field=None, sort_direction=None, filter_field=None, filter_string=None, since=None):
        return self._get_page("init", size, offset, since, type, sort_field, sort_direction, filter_field, filter_string)

    def get_page(self, size=None, offset=None, since=None, type=None, sort_field=None, sort_direction=None, filter_field=None, filter_string=None):
        return self._get_page("getPage", size, offset, since, type, sort_field, sort_direction, filter_field, filter_string)

    def get_details(self, plugin_id):
        return self.sc._request("plugin", "getDetails", {"pluginID": plugin_id})

    def get_source(self, plugin_id):
        return self.sc._request("plugin", "getSource", {"pluginID": plugin_id})