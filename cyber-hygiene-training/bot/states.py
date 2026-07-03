"""FSM states for the training bot conversation flow."""

from aiogram.fsm.state import State, StatesGroup


class TrainingFlow(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
