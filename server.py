from flask import Flask, request
import logging
import json
from geo import get_country, get_distance, get_coordinates

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):

    user_id = req['session']['user_id']

    if req['session']['new']:

        res['response']['text'] = 'ÐŸÑ€Ð¸Ð²ÐµÑ‚! Ð¯ Ð¼Ð¾Ð³Ñƒ ÑÐºÐ°Ð·Ð°Ñ‚ÑŒ Ð² ÐºÐ°ÐºÐ¾Ð¹ ÑÑ‚Ñ€Ð°Ð½Ðµ Ð³Ð¾Ñ€Ð¾Ð´ Ð¸Ð»Ð¸ ÑÐºÐ°Ð·Ð°Ñ‚ÑŒ Ñ€Ð°ÑÑÑ‚Ð¾ÑÐ½Ð¸Ðµ Ð¼ÐµÐ¶Ð´Ñƒ Ð³Ð¾Ñ€Ð¾Ð´Ð°Ð¼Ð¸!'

        return

    cities = get_cities(req)

    if len(cities) == 0:

        res['response']['text'] = 'Ð¢Ñ‹ Ð½Ðµ Ð½Ð°Ð¿Ð¸ÑÐ°Ð» Ð½Ð°Ð·Ð²Ð°Ð½Ð¸Ðµ Ð½Ðµ Ð¾Ð´Ð½Ð¾Ð³Ð¾ Ð³Ð¾Ñ€Ð¾Ð´Ð°!'

    elif len(cities) == 1:

        res['response']['text'] = 'Ð­Ñ‚Ð¾Ñ‚ Ð³Ð¾Ñ€Ð¾Ð´ Ð² ÑÑ‚Ñ€Ð°Ð½Ðµ - ' + get_country(cities[0])

    elif len(cities) == 2:

        distance = get_distance(get_coordinates(cities[0]), get_coordinates(cities[1]))
        res['response']['text'] = 'Ð Ð°ÑÑÑ‚Ð¾ÑÐ½Ð¸Ðµ Ð¼ÐµÐ¶Ð´Ñƒ ÑÑ‚Ð¸Ð¼Ð¸ Ð³Ð¾Ñ€Ð¾Ð´Ð°Ð¼Ð¸: ' + str(round(distance)) + ' ÐºÐ¼.'

    else:

        res['response']['text'] = 'Ð¡Ð»Ð¸ÑˆÐºÐ¾Ð¼ Ð¼Ð½Ð¾Ð³Ð¾ Ð³Ð¾Ñ€Ð¾Ð´Ð¾Ð²!'


def get_cities(req):

    cities = []

    for entity in req['request']['nlu']['entities']:

        if entity['type'] == 'YANDEX.GEO':

            if 'city' in entity['value'].keys():
                cities.append(entity['value']['city'])

    return cities

if __name__ == '__main__':
    app.run()
