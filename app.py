import logging
from flask import Flask, render_template, request
from models import *
from forms import SerchForm
from settings import Config
from orm import PER_PAGE
from logger_config import logger


log = logging.getLogger(__name__)
log.info("Приложение запущено")



app = Flask(__name__)
app.config.from_object(Config)



@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    find_all_films_query_result = get_all_film_by_filters(**request.args)
    find_films_query_result = get_film_by_filters(**request.args)
    form = SerchForm(**request.args.to_dict())
    total_pages = (len(find_all_films_query_result) + PER_PAGE - 1) // PER_PAGE
    if find_all_films_query_result:
        log_form_data(**request.args)
    result_popular_queries = get_popular_queries()
    content = {
        "title": "Поиск Фильмов",
        "popular_queries": result_popular_queries,
        "page": page,
        "pages": [p for p in range(page, page + 3) if p <= total_pages],
        "total_pages": total_pages,
        "films": find_films_query_result,
        }
    return render_template('index.html', form=form, content=content)

@app.route('/films')
def view_all_films():
    page = request.args.get('page', 1, type=int)
    films_all_result = get_films()
    total_pages = (len(films_all_result) + PER_PAGE - 1) // PER_PAGE
    films_query_result = get_films(page=page)
    content = {
        "title": "Фильми",
        "films": films_query_result,
        "tabel": "includes/films_tabel.html",
        "page": page,
        "pages": [p for p in range(page, page + 3) if p <= total_pages],
        "total_pages": total_pages
    }
    return render_template('view_all.html', content=content)

@app.route('/films/<film_id>')
def view_film_detail(film_id: int):
    film_result = get_film(film_id)
    actors_result = get_actors_by_film(film_id)
    content = {
        "title": film_result.get('title'),
        "film": film_result,
        "table": "includes/film_detail.html",
        "actors": actors_result
    }
    return render_template('view_one.html', content=content)

@app.route('/actors')
def view_all_actors():
    page = request.args.get('page', 1, type=int)
    actors_all_result = get_actors()
    total_pages = (len(actors_all_result) + PER_PAGE - 1) // PER_PAGE
    actors_result = get_actors(page=page)
    content = {
        "title": "Актеры",
        "actors": actors_result,
        "tabel": "includes/actors_tabel.html",
        "page": page,
        "pages": [p for p in range(page, page + 3) if p <= total_pages],
        "total_pages": total_pages
    }
    return render_template('view_all.html', content=content)

@app.route('/actors/<actor_id>')
def view_actor_detail(actor_id: int):
    actor_result = get_actor(actor_id)
    films_result = get_films_by_actor(actor_id)
    content = {
        "title": f"{actor_result.get('first_name')} {actor_result.get('last_name')}".upper(),
        "actor": actor_result,
        "table": "includes/actor_detail.html",
        "films": films_result
    }
    return render_template('view_one.html', content=content)

@app.route('/categories')
def view_all_categories():
    categories_result = get_categories()
    content = {
        "title": "Жанры",
        "categories": categories_result,
        "tabel": "includes/categories_tabel.html",
    }
    return render_template('view_all.html', content=content)

@app.route('/categories/<category_id>')
def view_category_detail(category_id: int):
    category_result = get_category(category_id)
    films_result = films_by_category(category_id)
    content = {
        "title": f"{category_result.get('name')}".upper(),
        "category": category_result,
        "table": "includes/category_detail.html",
        "films": films_result
        }
    return render_template('view_one.html', content=content)

if __name__ == '__main__':
    app.run()
