from aiogram.fsm.state import StatesGroup, State


# -----------------Monitor Accounts----------------
# --------GET--------
class GetMonitorAccountByPK(StatesGroup):
    waiting_for_pk = State()


class GetMonitorAccountByUserID(StatesGroup):
    waiting_for_user_id = State()


# --------ADD--------
class AddMonitorAccount(StatesGroup):
    waiting_for_form = State()


#--------EDIT--------
class EditMonitorAccountByPK(StatesGroup):
    waiting_for_pk = State()
    waiting_for_form = State()

class EditMonitorAccountByUserID(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_form = State()