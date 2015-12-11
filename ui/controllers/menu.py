from functools import wraps

from flask import jsonify, request, g, abort
import rethinkdb as r

from app import app
from models.Error import Error


def login_required(function_to_wrap):
    @wraps(function_to_wrap)
    def wrap(*args, **kwargs):
        try:
            if request.method == 'GET':
                data = r.table("user_token").filter(
                    {"user_id": request.args.get('user_id'), "auth_token": request.args.get('auth_token')}).run(
                    g.rdb_conn)
            else:
                data = r.table("user_token").filter(
                    {"user_id": request.json.get('user_id'), "auth_token": request.json.get('auth_token')}).run(
                    g.rdb_conn)

            if data.next():
                print("cool you are authorized man!")
                return function_to_wrap(*args, **kwargs)
            else:
                abort(400)
        except Exception as e:
            abort(403)

    return wrap


@app.route("/page/", methods=['GET'])
@login_required
def get_next_page():
    data = r.table('page').filter({'completed': False}).run(g.rdb_conn)
    try:
        result_json = data.next()
        return jsonify({"restaurant_id": result_json['restaurant_id'], "page_id": result_json['id'],
                        "page_url": result_json['url']})
    except Exception as e:
        print(e)
        return jsonify({"status": "No urls left"})


@app.route("/menu/", methods=['POST'])
@login_required
def create_menu():
    if ('restaurant_id' and 'type' and 'user_id' and 'page_id' and 'description') in request.json:
        data = request.get_json()
        try:
            page_data = r.table('page').get(data['page_id']).run(g.rdb_conn)
            data['page_url'] = page_data['url']
        except Exception as e:
            print(e)
            return Error(code=8, message='invalid_page_id').to_json()

        try:
            restaurant_data = r.table('restaurant').get(data['restaurant_id']).run(g.rdb_conn)
            data['restaurant_name'] = restaurant_data['name']
            data['restaurant_address'] = restaurant_data['address']
            data['restaurant_zip'] = restaurant_data['zip']
        except Exception as e:
            print(e)
            return Error(code=9, message='invalid_restaurant_id').to_json()

        menu = r.table('menu').insert(data).run(g.rdb_conn)

        if menu['inserted'] == 1:
            return jsonify({"status": "okay", "restaurant_id": data['restaurant_id'], "page_id": data['page_id'],
                            "menu_id": menu['generated_keys'][0]})
        else:
            abort(400)
    else:
        return Error(code=10, message='missing_parameters').to_json()


@app.route("/menu/category/", methods=['POST'])
@login_required
def create_category():
    if ('menu_id' and 'name' and 'user_id' and 'description') in request.json:
        data = request.get_json()
        try:
            menu_data = r.table('menu').get(data['menu_id']).run(g.rdb_conn)
            data['restaurant_id'] = menu_data['restaurant_id']
            data['restaurant_name'] = menu_data['restaurant_name']
            data['restaurant_address'] = menu_data['restaurant_address']
            data['restaurant_zip'] = menu_data['restaurant_zip']
            data['page_id'] = menu_data['page_id']
            data['page_url'] = menu_data['page_url']
            data['menu_type'] = menu_data['type']
            data['menu_description'] = menu_data['description']



        except Exception as e:
            print(e)
            return Error(code=11, message='invalid_menu_id').to_json()

        menu_category = r.table('menu_category').insert(data).run(g.rdb_conn)

        if menu_category['inserted'] == 1:
            return jsonify({"status": "okay", "restaurant_id": data['restaurant_id'], "page_id": data['page_id'],
                            "menu_id": data['menu_id'], "menu_category_id": menu_category['generated_keys'][0]})
        else:
            abort(400)
    else:
        return Error(code=10, message='missing_parameters').to_json()


@app.route("/menu/item/", methods=['POST'])
@login_required
def create_item():
    if ('menu_category_id' and 'name' and 'user_id' and 'description' and 'price' and 'extras') in request.json:
        data = request.get_json()
        try:
            menu_category_data = r.table('menu_category').get(data['menu_category_id']).run(g.rdb_conn)
            data['restaurant_id'] = menu_category_data['restaurant_id']
            data['restaurant_name'] = menu_category_data['restaurant_name']
            data['restaurant_address'] = menu_category_data['restaurant_address']
            data['restaurant_zip'] = menu_category_data['restaurant_zip']
            data['page_id'] = menu_category_data['page_id']
            data['page_url'] = menu_category_data['page_url']
            data['menu_id'] = menu_category_data['menu_id']
            data['menu_type'] = menu_category_data['menu_type']
            data['menu_description'] = menu_category_data['menu_description']
            data['menu_category_id'] = menu_category_data['id']
            data['menu_category_name'] = menu_category_data['name']
            data['menu_category_description'] = menu_category_data['description']

        except Exception as e:
            print(e)
            return Error(code=12, message='invalid_menu_category_id').to_json()

        menu_item = r.table('menu_item').insert(data).run(g.rdb_conn)

        if menu_item['inserted'] == 1:
            return jsonify({"status": "okay", "restaurant_id": data['restaurant_id'], "page_id": data['page_id'],
                            "menu_id": data['menu_id'], "menu_category_id": data['menu_category_id'],
                            "menu_item_id": menu_item['generated_keys'][0]})
        else:
            abort(400)
    else:
        return Error(code=10, message='missing_parameters').to_json()


def load():
    pass
