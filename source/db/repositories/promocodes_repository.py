from source.db.repositories.base_repository import BaseRepository
from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from source.db.utils.payment import generate_payment_code
from source.dto import PromocodeInfo


class PromocodesRepository(BaseRepository):
    def __init__(self, connection: Connection):
        super().__init__(connection)

    async def create_code(self, interval_str: str, count: int) -> PromocodeInfo:
        query = """
                INSERT INTO promocodes (code, count_activation, interval)
                VALUES ($1, $2, $3)
                ON CONFLICT (code) DO NOTHING
                RETURNING *;
            """

        while True:
            code = generate_payment_code()
            record = await self.connection.fetchrow(query, code, count, interval_str)
            
            if record:
                return PromocodeInfo.load_from_record(record)

    async def use_promocode(self, user_id: int, code: str) -> dict:
        response = {
            "success": False,
            "message": "Что-то пошло не так...",
            "message_type": "error"
        }
        try:
            async with self.connection.transaction():
                # 1. Проверяем существование
                check_query = "SELECT id, count_activation, interval FROM promocodes WHERE code = $1"
                promo = await self.connection.fetchrow(check_query, code)

                if not promo:
                    response["message"] = "Промокод не найден"
                    return response

                if promo['count_activation'] is not None and promo['count_activation'] <= 0:
                    response["message"] = "Лимит активаций этого кода исчерпан"
                    return response

                # !!! ДОБАВЛЕНО: Уменьшаем счетчик (важно для атомарности)
                update_promo_query = """
                    UPDATE promocodes 
                    SET count_activation = count_activation - 1 
                    WHERE id = $1 AND (count_activation > 0 OR count_activation IS NULL)
                    RETURNING id;
                """
                if not await self.connection.fetchval(update_promo_query, promo['id']):
                    response["message"] = "Лимит активаций исчерпан (только что)"
                    return response

                # 2. Обновляем подписку
                user_query = """
                    UPDATE users 
                    SET paid_until = GREATEST(paid_until, (NOW() AT TIME ZONE 'utc')) + $1::INTERVAL
                    WHERE id = $2
                    RETURNING paid_until;
                """
                new_paid_until = await self.connection.fetchval(user_query, promo['duration'], user_id)

                # 3. Записываем в историю
                history_query = "INSERT INTO history_promocodes (user_id, promocode_id) VALUES ($1, $2);"
                await self.connection.execute(history_query, user_id, promo['id'])

                response.update({
                    "success": True,
                    "message": f"Промокод успешно активирован!\nДобавлено: {promo['duration']}",
                    "message_type": "success"
                })
                return response

        except UniqueViolationError:
            response["message"] = "Вы уже активировали этот промокод ранее"
            return response
        except Exception as e:
            return response
        