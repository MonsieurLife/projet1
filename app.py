from flask import Flask, jsonify, request

server = Flask(__name__)

@server.route('/') #http://127.0.0.1:
def le_truc():

    return jsonify(
        {
            "res":"welccome to my games API !!!"
        }
    )
games_list=[
    {
        "id":1,
        "title":"Hollow Knight"
    },
    {
        "id":2,
        "title":"Undertale"
    }
]

@server.route('/api/games/', methods=['GET', 'POST'])
def all_games():
    limit = 2
    if request.method == 'GET':
        return jsonify(games_list)
    elif request.method == 'POST':
        try:
            req = request.json
            new_id = len(games_list) + 1  # Assuming each game has a unique ID
            
            new_games = [{
                "id": new_id + index,
                "title": req[index]['title'],
                # Add other properties as needed
            } for index in range(min(limit, len(req)))]
        
            games_list.extend(new_games)
            return jsonify({"msg": f"{len(new_games)} games created"}), 201
        except (TypeError, KeyError, IndexError):
            return jsonify({"msg": "Invalid data in the request"}), 400
    else:
        return 'Invalid request method'
@server.route('/api/games/<int:id>', methods=['GET', 'POST','DELETE','PUT'])
def book_one(id):
    if request.method == 'GET':
        try :
            return jsonify({"msg":games_list[id-1]})
        except :
            return jsonify({"msg":"Livre non trouvé"}),404
    elif request.method == 'DELETE':
        try:
            games_list.remove(games_list[id-1])
            return jsonify({"msg":"Livre {id} supprimé"}),200
        except :
            return jsonify({"msg":"Livre non trouvé"}),404
    elif request.method == 'PUT':
        try:
            games_list[id-1]['title'] = request.json['title']
            return jsonify({"msg":"Book updated"}),200
        except :
            return jsonify({"msg":"Livre non trouvé"}),404
    elif request.method == 'POST':
        try:
            new_game = {
                'id': request.json.get('id', None),  # Use provided id or let it be None
                'title': request.json.get('title'),  # Use provided title or return None
                # Add other properties as needed
            }
            games_list.append(new_game)
            return jsonify({"msg": f"Livre {new_game['id']} créé"}), 201
        except KeyError:
            return jsonify({"msg": "Données invalides"}), 400
server.debug = True
server.run()


