from flask import Flask, request, jsonify
import json

app = Flask(__name__)

ARQUIVO = 'produtos.json'

def ler_dados():
    try:
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    except:
        return []

def salvar_dados(dados):
    with open(ARQUIVO, 'w') as f:
        json.dump(dados, f, indent=4)

def gerar_id(dados):
    if not dados:
        return 1
    return max(p['id'] for p in dados) + 1

@app.route('/produtos', methods=['GET'])
def listar():
    return jsonify(ler_dados())

@app.route('/produtos', methods=['POST'])
def criar():
    dados = ler_dados()
    novo = request.json

    if not novo.get('nome') or not novo.get('preco'):
        return jsonify({"erro": "Nome e preço são obrigatórios"}), 400

    novo['id'] = gerar_id(dados)
    dados.append(novo)
    salvar_dados(dados)

    return jsonify(novo), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar(id):
    dados = ler_dados()
    novo = request.json

    for i, p in enumerate(dados):
        if p['id'] == id:
            dados[i]['nome'] = novo.get('nome', p['nome'])
            dados[i]['preco'] = novo.get('preco', p['preco'])
            salvar_dados(dados)
            return jsonify(dados[i])

    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar(id):
    dados = ler_dados()
    novos = [p for p in dados if p['id'] != id]

    if len(dados) == len(novos):
        return jsonify({"erro": "Produto não encontrado"}), 404

    salvar_dados(novos)
    return jsonify({"mensagem": "Produto removido"})
    
if __name__ == '__main__':
    app.run(debug=True)