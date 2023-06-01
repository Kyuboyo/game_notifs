from django.core import serializers
from django.core.cache import cache

from epicstore_api import EpicGamesStoreAPI, OfferData
from .models import GamesModel, ImagesModel, CategoriesModel

import json
from datetime import datetime

api = EpicGamesStoreAPI()

def get_fields(call_by='epic'):
    if call_by == 'epic':
        fields = ["title", "description", "keyImages", "seller", "categories", "slug"]
    return fields

def pull_free_games_epic(call_by):
    games = api.get_free_games().get('data').get('Catalog').get('searchStore').get('elements')
    game_list = []
    if games:
        for game in games:
            fields = get_fields(call_by)
            details = {field: game.get(field) or None for field in fields}
            details['slug'] = game.get('productSlug') or ''
            game_list.append(details)
            
    return game_list

def get_free_games(store):
    queryset = GamesModel.objects.select_related().filter(store=store, deleted_at=None)
    data = []
    for game in queryset:
        images = json.loads(serializers.serialize('json', game.imagesmodel_set.all()))
        details = json.loads(serializers.serialize('json', [game]))
        details[0]['fields']['images'] = images
        data.append(details[0])

    return data

def save_offers(obj, store):
    if store == 'epic':
        old_games = GamesModel.objects.filter(store=store)
        for entry in old_games:
            entry.deleted_at = datetime.now()
            entry.save()
        for item in obj:
            description = chec_desc_len(item.get('description'))
            game = GamesModel.objects.create(
                                                title       = item.get('title'), 
                                                description = description, 
                                                seller      = item.get('seller').get('name'), 
                                                store       = store,
                                                slug        = item.get('productSlug')
                                            )
            for image in item.get('keyImages'):
                ImagesModel.objects.create(url=image.get('url'), game=game)
            
            for category in item.get('categories'):
                CategoriesModel.objects.create(category=category.get('path'), game=game)
                
def get_cached_data(store):
    cache_key = "gamesmodel"
    cached_instance = cache.get(cache_key)

    if cached_instance is None:
        instance = get_free_games(store)
        cache.set(cache_key, instance)
    else:
        instance = cached_instance
    
    return instance

def update_cached_data(store):
    cache_key = "gamesmodel"
    instance = get_free_games(store)
    cache.delete(cache_key)

    cache.set(cache_key, instance)

def chec_desc_len(desc):
    if len(desc)> 255:
        desc = desc[:252] + "..."
    return desc

def compare_cache_with_data(fresh_data, cache_data):
    fresh_data_games = {item.get('title') for item in fresh_data}

    cache_data_games = [game.get('fields').get('titlle') for game in cache_data]

    return fresh_data_games, cache_data_games

def get_free_games_with_images(store):
    queryset = GamesModel.objects.select_related().filter(store=store, deleted_at=None)
    gameset = []
    for game in queryset:
        images = json.loads(serializers.serialize('json', game.imagesmodel_set.all()))
        details = json.loads(serializers.serialize('json', [game]))
        details[0]['fields']['images'] = images
        gameset.append(details[0])

    data = gameset
    return data

def getURL(store, slug):
    if store == 'epic':
        return 'https://store.epicgames.com/en-US/p/' + slug