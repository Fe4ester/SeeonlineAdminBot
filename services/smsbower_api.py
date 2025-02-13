import aiohttp
import re
import json


class SmsBowerAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_balance(self, token: str):
        url = f"{self.base_url}?api_key={token}&action=getBalance"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()

                match = re.search(r"ACCESS_BALANCE:(\d+(\.\d+)?)", data)
                if match:
                    balance = float(match.group(1))
                else:
                    balance = 0.0

                return balance

    async def get_prices(
            self, token: str, country: int = None, version: int = 1, max_price: float = 40, min_count: int = 5
    ):
        if version == 1:
            if country:
                url = f"{self.base_url}?api_key={token}&action=getPrices&service=tg&country={country}"
            else:
                url = f"{self.base_url}?api_key={token}&action=getPrices&service=tg"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    text_data = await response.text()
                    data = json.loads(text_data)

                    filtered_data = {
                        key: value for key, value in data.items()
                        if value.get("tg", {}).get("cost", float("inf")) <= max_price
                           and value.get("tg", {}).get("count", 0) >= min_count
                    }

                    return filtered_data
