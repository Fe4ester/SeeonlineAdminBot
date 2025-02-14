import aiohttp
import json
import re


class SmsBowerAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _fetch_text(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    def _check_errors(self, text: str, errors: dict):
        """
        Проверяет наличие ошибок в ответе API и выбрасывает исключение с соответствующим сообщением.
        """
        for error_key, error_msg in errors.items():
            if error_key in text:
                raise ValueError(error_msg)

    async def get_balance(self, token: str):
        url = f"{self.base_url}?api_key={token}&action=getBalance"
        text = await self._fetch_text(url)
        if "BAD_KEY" in text:
            raise ValueError("Некорректный апи ключ")
        match = re.search(r"ACCESS_BALANCE:(\d+(\.\d+)?)", text)
        return float(match.group(1)) if match else 0.0

    async def get_prices(self, token: str, country: int = None, version: int = 1,
                         max_price: float = 40, min_count: int = 5):
        if version not in (1, 2):
            raise ValueError("Invalid version")
        action = "getPricesV2" if version == 2 else "getPrices"
        url = f"{self.base_url}?api_key={token}&action={action}&service=tg"
        if country:
            url += f"&country={country}"
        text = await self._fetch_text(url)
        self._check_errors(text, {
            "BAD_KEY": "Неверный API-ключ",
            "BAD_ACTION": "Некорректное действие",
            "BAD_SERVICE": "Некорректное наименование сервиса"
        })
        data = json.loads(text)
        if version == 1:
            return {
                key: value
                for key, value in data.items()
                if value.get("tg", {}).get("cost", float("inf")) <= max_price and
                   value.get("tg", {}).get("count", 0) >= min_count
            }
        else:
            filtered_data = {}
            for country_id, details in data.items():
                filtered_prices = {}
                for price, count in details.get("tg", {}).items():
                    try:
                        price_val = float(price)
                    except ValueError:
                        continue
                    if price_val <= max_price and count >= min_count:
                        filtered_prices[price] = count
                if filtered_prices:
                    filtered_data[country_id] = {"tg": filtered_prices}
            return filtered_data

    async def get_number(self, token: str, max_price: float, country: int,
                         provider_ids: str = None, except_provider_ids: str = None):
        params = [
            f"api_key={token}",
            "action=getNumberV2",
            "service=tg",
            f"maxPrice={max_price}",
            f"country={country}"
        ]
        if provider_ids:
            params.append(f"providerIds={provider_ids}")
        if except_provider_ids:
            params.append(f"exceptProviderIds={except_provider_ids}")
        url = f"{self.base_url}?{'&'.join(params)}"
        text = await self._fetch_text(url)
        self._check_errors(text, {
            "BAD_KEY": "Неверный API-ключ",
            "BAD_ACTION": "Некорректное действие",
            "BAD_SERVICE": "Некорректное наименование сервиса"
        })
        return json.loads(text)

    async def get_sms(self, token: str, activation_id: str) -> str:
        url = f"{self.base_url}?api_key={token}&action=getStatus&id={activation_id}"
        text = await self._fetch_text(url)
        self._check_errors(text, {
            "BAD_KEY": "Неверный API-ключ",
            "BAD_ACTION": "Некорректное действие",
            "NO_ACTIVATION": "Id активации не существует"
        })
        if text.startswith("STATUS_OK"):
            parts = text.split(":", 1)
            activation_code = parts[1].strip(" '\"") if len(parts) > 1 else None
            return f"Код пришел: {activation_code}"
        if text.startswith("STATUS_CANCEL"):
            return "Активация отменена"
        if text.startswith("STATUS_WAIT_RESEND"):
            return "Ожидание следующих смс:"
        if text.startswith("STATUS_WAIT_CODE"):
            return "Ожидание смс"
        return text

    async def set_status(self, token: str, activation_id: str, status: str) -> str:
        url = f"{self.base_url}?api_key={token}&action=setStatus&status={status}&id={activation_id}"
        text = (await self._fetch_text(url)).strip()
        self._check_errors(text, {
            "NO_ACTIVATION": "Id активации не существует",
            "BAD_SERVICE": "Некорректное наименование сервиса",
            "BAD_STATUS": "Некорректный статус",
            "BAD_KEY": "Неверный API-ключ",
            "BAD_ACTION": "Некорректное действие",
            "EARLY_CANCEL_DENIED": "Отменить номер возможно спустя 2 минуты после покупки"
        })
        status_mapping = {
            "ACCESS_READY": "Готовность номера подтверждена",
            "ACCESS_RETRY_GET": "Ожидание нового смс",
            "ACCESS_ACTIVATION": "Сервис успешно активирован",
            "ACCESS_CANCEL": "Активация отменена"
        }
        if text in status_mapping:
            return status_mapping[text]
        raise ValueError(f"Неизвестный ответ API: {text}")
