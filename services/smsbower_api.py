import aiohttp

class SmsBowerAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_data(self, endpoint: str) -> dict:
        """
        Пример базового GET-запроса к внешнему API.
        endpoint: например, "/todos/1"
        """
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
