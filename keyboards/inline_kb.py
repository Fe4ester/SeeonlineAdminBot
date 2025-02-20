from typing import List, Tuple, Dict
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# базовый класс для исключения повторения кода
class BaseCategoryKeyboard:
    menus: Dict[str, List[Tuple[str, str]]] = {}

    @classmethod
    def get_keyboard(cls, menu: str = "main") -> InlineKeyboardMarkup:
        if menu not in cls.menus:
            raise ValueError(f"Меню '{menu}' не определено для {cls.__name__}")
        kb_builder = InlineKeyboardBuilder()
        for text, callback_data in cls.menus[menu]:
            kb_builder.row(InlineKeyboardButton(text=text, callback_data=callback_data))
        return kb_builder.as_markup()


# Клавиатура для мониторинг-аккаунтов
class MonitorAccountsKeyboard(BaseCategoryKeyboard):
    menus = {
        "main": [
            ("Получить аккаунты", "get-monitor-accounts"),
            ("Добавить аккаунты", "add-monitor-accounts"),
            ("Изменить данные", "edit-monitor-accounts"),
            ("Удалить аккаунты", "delete-monitor-accounts"),
            ("Авторизовать аккаунты", "auth-monitor-accounts"),
        ],
        "get": [
            ("Получить весь список", "get-list-monitor-accounts"),
            ("Получить аккаунт по PK", "get-monitor-account-by-pk"),
            ("Получить аккаунт по UserID", "get-monitor-account-by-user_id"),
            ("<<< Назад", "back-monitor-accounts"),
        ],
        "add": [], # нахуй не нужно, на будущее
        "edit": [
            ("Изменить по PK", "edit-monitor-account-by-pk"),
            ("Изменить по UserID", "edit-monitor-account-by-user_id"),
            ("<<< Назад", "back-monitor-accounts"),
        ],
        "delete": [],
        "auth": []
    }


# Клавиатура для мониторинговых аккаунтов
class MonitoredAccountsKeyboard(BaseCategoryKeyboard):
    menus = {
        "main": [
            ("Получить аккаунты", "get-monitored-accounts"),
            ("Добавить аккаунты", "add-monitored-accounts"),
            ("Изменить аккаунты", "edit-monitored-accounts"),
            ("Удалить аккаунты", "delete-monitored-accounts"),
        ],
        "secondary": [
            ("Доп. функция 1", "monitored_sub1"),
            ("Доп. функция 2", "monitored_sub2"),
        ],
    }


# Клавиатура для настроек мониторинг-аккаунтов
class MonitorSettingsKeyboard(BaseCategoryKeyboard):
    menus = {
        "main": [
            ("Получить настройки", "get-monitor-settings"),
            ("Добавить настройки", "add-monitor-settings"),
            ("Изменить настройки", "edit-monitor-settings"),
            ("Удалить настройки", "delete-monitor-settings"),
        ],
        "secondary": [
            ("Настройка доп. 1", "settings_sub1"),
            ("Настройка доп. 2", "settings_sub2"),
        ],
    }


# Клавиатура для дополнительных функций
class AdditionalFunctionsKeyboard(BaseCategoryKeyboard):
    menus = {
        "main": [
            ("Получить системную информацию", "get-system-info"),
            ("Получить метрики", "get-metrics"),
        ],
        "secondary": [
            ("Функция доп. 1", "additional_sub1"),
            ("Функция доп. 2", "additional_sub2"),
        ],
    }


# остальные клавиатуры, доп.

## пагинация, по сути подходит для всех хэндлеров, но поаккуратнее, потому что пока что костыль
# todo сделать все по красоте, без копипасты в будущем
def get_pagination_keyboard(page: int, total_pages: int):
    buttons = []

    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="<< Назад",
                callback_data=f"monitor_accounts_page:{page - 1}"
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data="noop"  # заглушка, от всяких долбаебов
        )
    )

    if page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text="Вперёд >>",
                callback_data=f"monitor_accounts_page:{page + 1}"
            )
        )

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
