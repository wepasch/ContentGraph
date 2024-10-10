class Disease:
    __name: str
    __short_name: str

    def __init__(self, name: str, short_name: str):
        self.__name = name
        self.__short_name = short_name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def short_name(self) -> str:
        return self.__short_name