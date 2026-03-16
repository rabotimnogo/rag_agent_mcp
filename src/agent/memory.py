from abc import ABC, abstractmethod


class BaseMemory(ABC):
    """
    Абстракция памяти.
    SimpleMemory — просто список сообщений.
    В будущем: RAGMemory будет здесь же, реализуя тот же интерфейс.
    AgentRunner работает только с BaseMemory — переключение прозрачно.
    """

    @abstractmethod
    def add(self, role: str, content: str) -> None: ...

    @abstractmethod
    def get_messages(self) -> list[dict]: ...

    @abstractmethod
    def clear(self) -> None: ...


class SimpleMemory(BaseMemory):
    def __init__(self, system_prompt: str):
        self._messages = [{"role": "system", "content": system_prompt}]

    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})

    def get_messages(self) -> list[dict]:
        return self._messages.copy()

    def clear(self) -> None:
        system = self._messages[0]
        self._messages = [system]
