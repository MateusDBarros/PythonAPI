from flask import Flask, jsonify, request

app = Flask(__name__)

listOfPeople = [
    {
        'id': 1,
        'nome': 'Mateus de Barros',
        'idade': 22
    },
    {
        'id': 2,
        'nome': 'Solaire of Astoria',
        'idade': 32
    },
    {
        'id': 3,
        'nome': 'Vendrick',
        'idade': 45
    }
]

# Get all
@app.route('/Pessoas', methods=['GET'])
def getPerson():
    return jsonify(listOfPeople)
# Get

@app.route('/Pessoas/<int:id>', methods=['GET'])
def getById(id):
    for pessoa in listOfPeople:
        if pessoa.get('id') == id:
            return jsonify(pessoa)

# Put
@app.route('/Pessoas/<int:id>',methods=['PUT'])
def updateById(id):
    pessoaUpdate = request.get_json()
    for index,person in enumerate(listOfPeople):
        if person.get('id') == id:
            listOfPeople[index].update(pessoaUpdate)
            return jsonify(listOfPeople[index])

# Post
@app.route('/Pessoas',methods=['POST'])
def newPerson():
    person = request.get_json()
    listOfPeople.append(person)
    return jsonify(listOfPeople)
# Delete
@app.route('/Pessoas/<int:id>',methods=['DELETE'])
def deletePerson(id):
    for index, person in enumerate(listOfPeople):
        if person.get('id') == id:
            del listOfPeople[index]
    return jsonify(listOfPeople)

app.run(port=8080, host='localhost', debug= True)