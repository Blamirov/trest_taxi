from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    # User_id, time, from, to, comment
    none = State()
    start = State()
    user_id = State()  # telegram user_id
    order_time = State()  # Время заказа
    service_time = State()  # Время подачи такси
    pickup_point = State()  # Место подачи такси
    destination_point = State()  # Место назначения
    need_comment = State()  # Комментарий
    comment = State()
    done = State()
    user_changing = State()
    need_order_time = State()
    user_choose_order = State()
    approved_changing = State()


class DriverStates(StatesGroup):
    send_order = State()
    accept_order = State()
    cancel_order = State()
    cancel_order_after_approved = State()
    send_message_to_pas = State()
    order_done = State()
