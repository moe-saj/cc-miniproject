from flask import Flask, request, jsonify
import requests
from cassandra.cluster import Cluster

cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
session = cluster.connect()
app = Flask(__name__)
POKEAPI_URL = 'https://pokeapi.co/api/v2/pokemon/'

'''Function to deal with GET, PUT, DELETE requests made to /pokemon/<name>'''
@app.route('/pokemon/<name>', methods=['GET', 'DELETE', 'PUT'])
def select_pokemon(name):
    #check pokemon with <name> name exists in DB
    rows = session.execute( """Select * From pokemon.stats
                            where name = '{}'""".format(name.capitalize()))

    #if pokemon does not exist, return 404
    if rows == []:
        return (jsonify({'error': '{} not found.'.format(name)}), 404)
    #if GET, return specific pokemon
    if request.method == 'GET':
        response = []
        resp = requests.get(POKEAPI_URL + name) #makes request to PokeAPI
        games = []
        if resp.ok: #if response from PokeAPI call is ok then add game_indices to game list
            pokeapi_resp = resp.json()
            for x in pokeapi_resp['game_indices']:
                        games.append(x['version']['name'])
        else: #if response is not ok, print reason and add error to game list
            print(resp.reason)
            games.append('data unavailable right now')
        for pokemon in rows:
                    response.append({
                    "name": pokemon.name, "attack": pokemon.attack, "defence": pokemon.defence,
                    "generation" : pokemon.generation, "hp": pokemon.hp, "id" : pokemon.id,
                    "legendary" : pokemon.legendary, "spDefence": pokemon.spdefence,
                    "spAttack": pokemon.spattack, "speed": pokemon.speed, "total": pokemon.total,
                    "type1": pokemon.type1, "type2": pokemon.type2, "appears_in" : games
                    })
        return (jsonify(response), 200)
    #if DELETE, remove pokemon from database
    elif request.method == 'DELETE':
        session.execute(""" Delete from pokemon.stats
                where name = '{}'""".format(name))
        return ('', 204)
    #if PUT, update pokemon in database
    elif request.method == 'PUT':
        body = request.json
        if body is None:
            return (jsonify({'error': 'Missing data. Request not fulfilled.'}), 400)
        try:
            session.execute(""" Update pokemon.stats
                            set attack = {}, defence = {}, generation = {},
                            hp = {}, id = {}, legendary = {}, total = {},
                            spDefence = {}, spAttack = {},
                            speed = {}, type1 = '{}', type2 = '{}'
                            where name = '{}';""".format(body['attack'], body['defence'], body['generation'], body['hp'],
                            body['id'], body['legendary'], body['total'],
                            body['spDefence'], body['spAttack'], body['speed'], body['type1'], body['type2'],
                            body['name']))
        except Exception as e:
            return (jsonify({'error': "'" + str(e) + "'"}), 400)
        return ('', 204)


'''function to deal with get requests - gets pokemon from pokemon database'''
@app.route('/pokemon/all', methods=['GET'])
def all_pokemon():
	rows = session.execute( """Select * From pokemon.stats""")
	response = []
	for pokemon in rows:
		response.append({"id": pokemon.id, "name": pokemon.name})
	return (jsonify(response), 200)

'''function to deal with post requests - creates a new pokemon into database'''
@app.route('/pokemon/new', methods=['POST'])
def new_pokemon():
    body = request.json
    if body is None:
        return (jsonify({'error': 'Missing data. Request not fulfilled.'}), 400)
    try:
        session.execute(""" Insert into pokemon.stats (name, attack, defence, generation,
                            hp, id, legendary, spdefence, spattack, speed, total, type1,
                            type2)
                    values('{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', '{}');"""
                    .format(body['name'], body['attack'], body['defence'],
                    body['generation'], body['hp'], body['id'], body['legendary'], body['spDefence'],
                    body['spAttack'], body['speed'], body['total'], body['type1'], body['type2']))
    except:
        return (jsonify({'error': 'Invalid data.'}), 400)
    return ('', 201)

if __name__ == '__main__':
	app.run(debug=True)
