import aiohttp
import urllib.parse


class SeeOnlineAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def _fetch_json(self, method: str, url: str, data: dict = None) -> dict:
        """
        Вспомогательный метод, выполняющий запрос и возвращающий JSON-ответ.
        Если ответ не в диапазоне 2xx, поднимает ValueError.
        """
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(url) as response:
                    return await self._handle_response(response)
            elif method.upper() == "POST":
                async with session.post(url, json=data) as response:
                    return await self._handle_response(response)
            elif method.upper() == "PATCH":
                async with session.patch(url, json=data) as response:
                    return await self._handle_response(response)
            elif method.upper() == "DELETE":
                async with session.delete(url) as response:
                    # DELETE обычно возвращает пустой ответ, но проверим статус
                    await self._handle_response(response)
                    return None
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

    async def _handle_response(self, response: aiohttp.ClientResponse) -> dict:
        """
        Обработка ответа: если статус-код 2xx, возвращаем JSON (или пустой словарь),
        иначе генерируем исключение с текстом ошибки.
        """
        if 200 <= response.status < 300:
            try:
                return await response.json()
            except aiohttp.ContentTypeError:
                # DELETE или пустой контент
                return {}
        else:
            text = await response.text()
            raise ValueError(f"Request failed with status {response.status}: {text}")

    def _build_url(self, endpoint: str, pk=None, query_params: dict = None) -> str:
        """
        Собирает URL с учётом pk (если указан) и query_params.
        endpoint, например, 'monitors', 'sessions', 'settings' и т.д.
        """
        url = f"{self.base_url}/{endpoint}/"
        if pk is not None:
            url += f"{pk}/"
        if query_params:
            # Фильтруем от None, чтобы не добавлять параметр, если он не задан
            filtered = {k: v for k, v in query_params.items() if v is not None}
            if filtered:
                url += "?" + urllib.parse.urlencode(filtered)
        return url

    #
    # =========== MonitorAccount ===========
    #
    async def get_monitor_account(self, pk=None, user_id=None):
        """
        Если pk указан, получаем конкретный объект,
        иначе если user_id указан — получаем объект по user_id,
        иначе возвращаем список всех MonitorAccount.
        ОТВЕЧАЕТ ЗА: /api/monitors/
        """
        query_params = {}
        if user_id is not None:
            query_params["user_id"] = user_id

        # <-- меняем 'monitor-accounts' на 'monitors'
        url = self._build_url("monitors", pk=pk, query_params=query_params)
        return await self._fetch_json("GET", url)

    async def create_monitor_account(self, data: dict):
        """
        Создаём новый MonitorAccount (POST) => /api/monitors/
        """
        url = self._build_url("monitors")
        return await self._fetch_json("POST", url, data=data)

    async def update_monitor_account(self, data: dict, pk=None, user_id=None):
        """
        Частичное обновление MonitorAccount (PATCH).
        Можно указать pk или user_id.
        """
        query_params = {}
        if user_id is not None:
            query_params["user_id"] = user_id

        url = self._build_url("monitors", pk=pk, query_params=query_params)
        return await self._fetch_json("PATCH", url, data=data)

    async def delete_monitor_account(self, pk=None, user_id=None):
        """
        Удаление MonitorAccount (DELETE).
        Можно указать pk или user_id.
        """
        query_params = {}
        if user_id is not None:
            query_params["user_id"] = user_id

        url = self._build_url("monitors", pk=pk, query_params=query_params)
        return await self._fetch_json("DELETE", url)

    #
    # =========== AccountSession ===========
    #
    async def get_account_session(self, pk=None, monitor_id=None, user_id=None):
        """
        GET /api/sessions/
        """
        query_params = {}
        if monitor_id is not None:
            query_params["monitor_id"] = monitor_id
        if user_id is not None:
            query_params["user_id"] = user_id

        # <-- меняем 'account-sessions' на 'sessions'
        url = self._build_url("sessions", pk=pk, query_params=query_params)
        return await self._fetch_json("GET", url)

    async def create_account_session(self, data: dict):
        url = self._build_url("sessions")
        return await self._fetch_json("POST", url, data=data)

    async def update_account_session(self, data: dict, pk=None, monitor_id=None, user_id=None):
        query_params = {}
        if monitor_id is not None:
            query_params["monitor_id"] = monitor_id
        if user_id is not None:
            query_params["user_id"] = user_id

        url = self._build_url("sessions", pk=pk, query_params=query_params)
        return await self._fetch_json("PATCH", url, data=data)

    async def delete_account_session(self, pk=None, monitor_id=None, user_id=None):
        query_params = {}
        if monitor_id is not None:
            query_params["monitor_id"] = monitor_id
        if user_id is not None:
            query_params["user_id"] = user_id

        url = self._build_url("sessions", pk=pk, query_params=query_params)
        return await self._fetch_json("DELETE", url)

    #
    # =========== MonitorSetting ===========
    #
    async def get_monitor_setting(self, pk=None, monitor_id=None, user_id=None):
        """
        GET /api/settings/
        """
        query_params = {}
        if monitor_id is not None:
            query_params["monitor_id"] = monitor_id
        if user_id is not None:
            query_params["user_id"] = user_id

        # <-- меняем 'monitor-settings' на 'settings'
        url = self._build_url("settings", pk=pk, query_params=query_params)
        return await self._fetch_json("GET", url)

    async def create_monitor_setting(self, data: dict):
        url = self._build_url("settings")
        return await self._fetch_json("POST", url, data=data)

    async def update_monitor_setting(self, data: dict, pk=None, monitor_id=None, user_id=None):
        query_params = {}
        if monitor_id is not None:
            query_params["monitor_id"] = monitor_id
        if user_id is not None:
            query_params["user_id"] = user_id

        url = self._build_url("settings", pk=pk, query_params=query_params)
        return await self._fetch_json("PATCH", url, data=data)

    async def delete_monitor_setting(self, pk=None, monitor_id=None, user_id=None):
        query_params = {}
        if monitor_id is not None:
            query_params["monitor_id"] = monitor_id
        if user_id is not None:
            query_params["user_id"] = user_id

        url = self._build_url("settings", pk=pk, query_params=query_params)
        return await self._fetch_json("DELETE", url)

    #
    # =========== MonitoredAccount ===========
    #
    async def get_monitored_account(self, pk=None, username=None, monitor_id=None, user_id=None):
        """
        GET /api/monitored/
        """
        query_params = {}
        if username is not None:
            query_params["username"] = username
        if monitor_id is not None:
            query_params["monitor_id"] = monitor_id
        if user_id is not None:
            query_params["user_id"] = user_id

        # <-- меняем 'monitored-accounts' на 'monitored'
        url = self._build_url("monitored", pk=pk, query_params=query_params)
        return await self._fetch_json("GET", url)

    async def create_monitored_account(self, data: dict):
        url = self._build_url("monitored")
        return await self._fetch_json("POST", url, data=data)

    async def update_monitored_account(self, data: dict, pk=None, username=None):
        query_params = {}
        if username is not None:
            query_params["username"] = username

        url = self._build_url("monitored", pk=pk, query_params=query_params)
        return await self._fetch_json("PATCH", url, data=data)

    async def delete_monitored_account(self, pk=None, username=None):
        query_params = {}
        if username is not None:
            query_params["username"] = username

        url = self._build_url("monitored", pk=pk, query_params=query_params)
        return await self._fetch_json("DELETE", url)

    #
    # =========== OnlineStatus ===========
    #
    async def get_online_status(self, pk=None, monitored_id=None, username=None):
        """
        GET /api/statuses/
        """
        query_params = {}
        if monitored_id is not None:
            query_params["monitored_id"] = monitored_id
        if username is not None:
            query_params["username"] = username

        # <-- меняем 'online-status' на 'statuses'
        url = self._build_url("statuses", pk=pk, query_params=query_params)
        return await self._fetch_json("GET", url)
