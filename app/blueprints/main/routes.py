from flask import redirect, render_template, request, flash, url_for
import requests
from .import bp as main
# from ...forms import PokemonForm
# from app.models import Pokemon, Pokedex, User
# import random


from flask_login import login_required, current_user



@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/shop', methods=['GET','POST'])
@login_required
def shop():
    return render_template('shop.html.j2')

@main.route('/item', methods=['GET','POST'])
@login_required
def item():
    return render_template('item.html.j2')

@main.route('/cart', methods=['GET','POST'])
@login_required
def cart():
    return render_template('cart.html.j2')

# @main.route('/delete_items/<int:id>', methods=['GET','POST'])
# # @login_required
# def delete_items(id):
#     return redirect(url_for('main.items.html.j2')