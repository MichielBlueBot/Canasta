from abc import ABCMeta, abstractmethod


class Drawable(metaclass=ABCMeta):

    @abstractmethod
    def draw(self, screen) -> None:
        raise NotImplementedError
