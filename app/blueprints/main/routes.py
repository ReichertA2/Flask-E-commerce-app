from flask import redirect, render_template, request, flash, url_for
import requests
from .import bp as main
# from ...forms import PokemonForm
from app.models import Item, Cart
# import random
import random

from flask_login import login_required, current_user



@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')



@main.route('/movies', methods=['GET','POST'])
@login_required
def movies():
    movies=Item.query.all()
    
    return render_template('movies.html.j2', movies=movies)

@main.route('/item_view/<int:id>', methods=['GET','POST'])
@login_required
def item_view(id):
    movies = Item.query.get(id)
    # movies = Item.query.filter_by(movie.id=id).first()
    
    return render_template('item.html.j2', movies=movies)

@main.route('/cart_add/<int:id>', methods=['GET','POST'])
@login_required
def cart_add(id):
    m = Item.query.filter_by(item_id=id).first()
    current_user.add_item(m)

    cart=Cart.query.filter_by(user_id=current_user.id)
    return render_template('cart.html.j2', cart=cart)

@main.route('/cart', methods=['GET'])
@login_required
def cart():
    cart=Cart.query.filter_by(user_id=current_user.id)
    

    return render_template('cart.html.j2', cart=cart)

# @main.route('/delete_items/<int:id>', methods=['GET','POST'])
# # @login_required
# def delete_items(id):
#     return redirect(url_for('main.items.html.j2')
@main.route('/movie_download', methods=['GET','POST'])
@login_required
def movie_download():
    prices = [12.00,15.00,10.00,1500.00]
    search_query = ['seattle','houston','dallas']
    movie_api_key = '29c54491a1b5999cf31098796cecae0b'
    url = f'https://api.themoviedb.org/3/search/movie?api_key={movie_api_key}&query={search_query[1]}'
    response = requests.get(url)
    resp_json = response.json()
    movies = resp_json["results"]
    # print(movies["results"][0])
    for i,item in enumerate(movies):

        movie_dict = {
            "name": movies[i]["title"],
            "desc": movies[i]["overview"],
            "price": random.choice(prices),
            "img": f'https://image.tmdb.org/t/p/w500{movies[i]["poster_path"]}'

        }
        print(movie_dict)
        new_movie = Item()
        new_movie.from_dict(movie_dict)
        new_movie.save()

        new_cart = Cart()
        new_cart.user_id=current_user.id
        new_cart.item_id = new_movie.item_id
        my_movie = Cart.query.filter_by(user_id=current_user.id).all()
        

        



    return render_template('movies.html.j2')

@main.route('/cart_remove/<int:id>', methods=['GET','POST'])
@login_required
def cart_remove(id):
    # m = Cart.query.filter_by(id=id)
    # print(m)
    # print(current_user.item)
    # current_user.remove_item(m)
    m=Item.query.filter_by(item_id=id).first()
    current_user.remove_item(m)

    cart=Cart.query.filter_by(user_id=current_user.id)
    return render_template('cart.html.j2' ,cart=cart)