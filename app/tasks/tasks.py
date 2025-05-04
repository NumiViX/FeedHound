from app.celery_app import celery_app
from app.parsers.rbc import parse_rbc
from app.crud.sync_news import save_news_sync

parser_map = {
    "lenta": lenta.parse_lenta,
    "rbc": rbc.parse_rbc,
}

@celery_app.task
def run_parser(parser_name: str, source_id: int):
    """
    Запускает нужный парсер по имени.
    """
    parser = parser_map.get(parser_name)
    if not parser:
        raise ValueError(f"Парсер '{parser_name}' не найден")

    return await parser(source_id)



"""@celery_app.task
def fetch_rbc_news_task(source_id: int):
    news_list = parse_rbc(source_id)
    save_news_sync(news_list)
"""