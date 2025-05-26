import logging
from orm import Table, Query, MySQLConnection, PER_PAGE
from utils import *
from collections import Counter


logger = logging.getLogger(__name__)

#ALL Tables
film_actor_table = Table('film_actor')
film_table = Table('film')
film_text_table = Table('film_text')
actor_table = Table('actor')
category_table = Table('category')
film_category_table = Table('film_category')
serch_forms_log_table = Table('serch_forms_log')

#All set_all_columns
columns_film_table = film_table.get_column()
columns_film_actor_table = film_actor_table.get_column()
columns_film_category_table = film_category_table.get_column()
columns_actor_table = actor_table.get_column()
columns_category_table = category_table.get_column()
columns_film_text_table = film_text_table.get_column()
columns_serch_forms_log_table = serch_forms_log_table.get_column()


def get_films(page: int = None):
    """Получение списка всех фильмов с пагинаией по странице"""
    q = Query(
        table=film_table
    )
    if page:
        q = q.set_limit(PER_PAGE).set_offset(page)
    q = q.build()
    return select_from_db(q, serialeizer_many_to_json)

def get_film(film_id):
    """Получение информации о фильме по ид фильма"""
    columns_film = film_table.get_column()
    q = Query(table=film_table).filter(
        colum=columns_film[0],
        compare="=",
        value=film_id
    ).build()
    return select_from_db(q, serialeizer_one_to_json)


def get_all_film_by_filters(**kwargs):
    """Поиск фильмов по фильтрам: название, актёр, категория, год, страница"""
    film = kwargs.get('film')
    actor = kwargs.get('actor')
    category = kwargs.get('category')
    year = kwargs.get('year')

    fields_output = columns_film_table[0:4] + [columns_film_text_table[2]] + [columns_category_table[1]]

    q = Query(table=film_table).select(
        fields=fields_output,
    ).set_distinct().join(
        join_type="LEFT",
        table_class=film_actor_table,
        on_from=columns_film_table[0],
        on_too=columns_film_actor_table[1],
    ).join(
        join_type="LEFT",
        table_class=film_category_table,
        on_from=columns_film_table[0],
        on_too=columns_film_category_table[0],
    ).join(
        join_type="LEFT",
        table_class=actor_table,
        on_from=columns_film_actor_table[0],
        on_too=columns_actor_table[0]
    ).join(
        join_type="LEFT",
        table_class=category_table,
        on_from=columns_film_category_table[1],
        on_too=columns_category_table[0]
    ).join(
        join_type="LEFT",
        table_class=film_text_table,
        on_from=columns_film_table[0],
        on_too=columns_film_text_table[0]
    )

    if film:
        q.filter(
            colum=columns_film_table[1],
            compare="like",
            value=prepare_like(film)
        )
    if actor:
        q.filter(
            colum=f"CONCAT({columns_actor_table[1]},' ', {columns_actor_table[2]})",
            compare="like",
            value=prepare_like(actor)
        )
    if category:
        q.filter(
            colum=columns_film_category_table[1],
            compare="=",
            value=category
        )
    if year:
        q.filter(
            colum=columns_film_table[3],
            compare="=",
            value=year
        )

    q = q.build()
    return select_from_db(q, serialeizer_many_to_json)


def get_film_by_filters(**kwargs):
    """Поиск фильмов по фильтрам: название, актёр, категория, год, страница"""
    film = kwargs.get('film')
    actor = kwargs.get('actor')
    category = kwargs.get('category')
    year = kwargs.get('year')
    page = int(kwargs.get('page', 1))

    fields_output = columns_film_table[0:4] + [columns_film_text_table[2]] + [columns_category_table[1]]

    q = Query(table=film_table).select(
        fields=fields_output,
    ).set_distinct().join(
        join_type="LEFT",
        table_class=film_actor_table,
        on_from=columns_film_table[0],
        on_too=columns_film_actor_table[1],
    ).join(
        join_type="LEFT",
        table_class=film_category_table,
        on_from=columns_film_table[0],
        on_too=columns_film_category_table[0],
    ).join(
        join_type="LEFT",
        table_class=actor_table,
        on_from=columns_film_actor_table[0],
        on_too=columns_actor_table[0]
    ).join(
        join_type="LEFT",
        table_class=category_table,
        on_from=columns_film_category_table[1],
        on_too=columns_category_table[0]
    ).join(
        join_type="LEFT",
        table_class=film_text_table,
        on_from=columns_film_table[0],
        on_too=columns_film_text_table[0]
    )

    if film:
        q.filter(
            colum=columns_film_table[1],
            compare="like",
            value=prepare_like(film)
        )
    if actor:
        q.filter(
            colum=f"CONCAT({columns_actor_table[1]},' ', {columns_actor_table[2]})",
            compare="like",
            value=prepare_like(actor)
        )
    if category:
        q.filter(
            colum=columns_film_category_table[1],
            compare="=",
            value=category
        )
    if year:
        q.filter(
            colum=columns_film_table[3],
            compare="=",
            value=year
        )
    if page:
        q = q.set_limit(PER_PAGE).set_offset(page)
    q = q.build()
    print(q)
    return select_from_db(q, serialeizer_many_to_json)


def get_actors(page: int = None):
    """Получение списка всех актеров с пагинаией по странице"""
    q = Query(
        table=actor_table
    )
    if page:
        q = q.set_limit(PER_PAGE).set_offset(page)
    q = q.build()
    return select_from_db(q, serialeizer_many_to_json)


def get_actor(actor_id):
    """Получение информации об Актере по его ИД"""
    q = Query(table=actor_table).filter(
        colum=columns_actor_table[0],
        compare="=",
        value=actor_id
    ).build()
    return select_from_db(q, serialeizer_one_to_json)


def get_films_by_actor(actor_id):
    """Получение списка фильмов по Актеру"""
    q = (Query(table=film_actor_table).join(
        table_class=film_table,
        on_from=columns_film_actor_table[1],
        on_too=film_table.get_column()[0]
    ).filter(
        colum=columns_film_actor_table[0],
        compare="=",
        value=actor_id
    ).set_order(
        film_table.get_column()[3], "DESC"
    ).build())
    return select_from_db(q, serialeizer_many_to_json)


def get_actors_by_film(actor_id):
    """Получение списка фильмов по Актеру"""
    q = (Query(
        table=film_actor_table
    ).join(
        table_class=actor_table,
        on_from=columns_film_actor_table[0],
        on_too=columns_actor_table[0]
    ).filter(
        colum=columns_film_actor_table[1],
        compare="=",
        value=actor_id
    ).build())
    return select_from_db(q, serialeizer_many_to_json)


def get_categories():
    """Получение списка всех Категорий"""
    q = Query(table=category_table).build()
    return select_from_db(q, serialeizer_many_to_json)


def get_category(category_id):
    """Получение Информации о категории"""
    q = Query(table=category_table).filter(
        colum=columns_category_table[0],
        compare="=",
        value=category_id
    ).build()
    return select_from_db(q, serialeizer_one_to_json)


def films_by_category(category_id):
    """Получение списка всех фильмов по Категории"""
    q = (Query(
        table=film_category_table
    ).join(
        table_class=film_table,
        on_from=columns_film_category_table[0],
        on_too=film_table.get_column()[0]
    ).filter(
        colum=columns_film_category_table[1],
        compare="=",
        value=category_id
    ).build())
    return select_from_db(q, serialeizer_many_to_json)


def get_categories_choice():
    """Формирование выбора категорий для формы"""
    q = Query(table=category_table).build()
    return select_from_db(q, serialeizer_many_to_choice)


def log_form_data(**kwargs):
    """Записуем результаты поиска в таблицу serch?forms?log"""
    film = kwargs.get('film')
    actor = kwargs.get('actor')
    category = kwargs.get('category')
    year = kwargs.get('year')
    serch_string = ""
    if film:
        serch_string += f"Film: {film} "
    if actor:
        serch_string += f"Actor: {actor} "
    if category:
        q = Query(
            table=category_table
            ).select(
            [columns_category_table[1]]
            ).filter(
            colum=columns_category_table[0],
            compare="=",
            value=category
            ).build()
        category = select_from_db(q, serialeizer_one_to_json).get('name')
        serch_string += f"Category: {category} "
    if year:
        serch_string += f"Year: {year} "
    q = f"INSERT INTO serch_forms_log (form_input) VALUES ('{serch_string}')"
    return insert_to_db(q)


def get_popular_queries():
    """Получение списка популярнейших запросов пользователей"""
    q = Query(
        table=serch_forms_log_table
    ).filter(
        colum=columns_serch_forms_log_table[1],
        compare="!=",
        value=""
    ).build()
    return Counter(select_from_db(q, serialeizer_to_list)).most_common(10)



