from sanic import Request


async def inject_db_connection_middleware(request: Request):
    async with request.app.ctx.db_pool.acquire() as connection:
        request.ctx.db = connection
        response = await request.app.handle_request(request)
        return response
