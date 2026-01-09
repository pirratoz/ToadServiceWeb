from enum import Enum


class TaskTypeEnum(Enum):
    WORK = "work"
    REWARD_CLAN = "reward_clan"
    REWARD_MARRIAGE = "reward_marriage"
    EAT_FROG = "eat_frog"
    EAT_TOAD = "eat_toad"
    FROG_DAY = "frog_day"

    @property
    def title(self) -> str:
        return {
            TaskTypeEnum.WORK: "Работа",
            TaskTypeEnum.REWARD_CLAN: "Награда клана",
            TaskTypeEnum.REWARD_MARRIAGE: "Награда брака",
            TaskTypeEnum.EAT_FROG: "Покормить жабу",
            TaskTypeEnum.EAT_TOAD: "Покормить жабёнка",
            TaskTypeEnum.FROG_DAY: "Жаба дня",
        }[self]
    