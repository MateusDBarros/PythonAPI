from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

app = Flask(__name__)

USERNAME = "postgres"
PASSWORD = quote_plus("lilY@")
HOST = "localhost"
PORT = "5432"
DATABASE = "flaskapi"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "idade": self.idade}

with app.app_context():
    db.create_all()

# Get all
@app.route('/Pessoas', methods=['GET'])
def getPerson():
    pessoas = Pessoa.query.all()
    return jsonify([pessoa.to_json() for pessoa in pessoas])

# Get
@app.route('/Pessoas/<int:id>', methods=['GET'])
def getById(id):
    pessoa = Pessoa.query.get(id)
    if pessoa:
        return jsonify(pessoa.to_json())
    return jsonify({"error": "Pessoa não encontrada"}), 404

# Put
@app.route('/Pessoas/<int:id>', methods=['PUT'])
def updateById(id):
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return jsonify({"error": "Pessoa não encontrada"}), 404
    data = request.get_json()
    pessoa.nome = data.get('nome', pessoa.nome)
    pessoa.idade = data.get('idade', pessoa.idade)
    db.session.commit()
    return jsonify(pessoa.to_json())

# Post
@app.route('/Pessoas', methods=['POST'])
def newPerson():
    data = request.get_json()
    nova_pessoa = Pessoa(nome=data['nome'], idade=data['idade'])
    db.session.add(nova_pessoa)
    db.session.commit()
    return jsonify(nova_pessoa.to_json()), 201

# Delete
@app.route('/Pessoas/<int:id>', methods=['DELETE'])
def deletePerson(id):
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return jsonify({"error": "Pessoa não encontrada"}), 404
    db.session.delete(pessoa)
    db.session.commit()
    return jsonify({"message": "Pessoa deletada com sucesso"})

if __name__ == '__main__':
    app.run(port=8080, host='localhost', debug=True)



