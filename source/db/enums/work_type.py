from enum import Enum


class WorkTypeEnum(str, Enum):
    CROUPIER = "croupier"
    CASINO = "casino"
    CAFETERIA = "cafeteria"
    COOK = "cook"
    ROBBER = "robber"
    CAREFREE = "carefree"

    @property
    def title(self) -> str:
        return {
            WorkTypeEnum.CROUPIER: "Крупье",
            WorkTypeEnum.CASINO: "Казино",
            WorkTypeEnum.CAFETERIA: "Столовая",
            WorkTypeEnum.COOK: "Повар",
            WorkTypeEnum.ROBBER: "Грабитель",
            WorkTypeEnum.CAREFREE: "Беззаботный",
        }.get(self, "Беззаботный")
