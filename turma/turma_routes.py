from flask import Blueprint, request, jsonify, render_template, redirect, \
    url_for
from .turma_model import Turma
from professor.professor_model import Professor

turma_blueprint = Blueprint('turmas', __name__)


@turma_blueprint.route('/turmas/criar', methods=['GET', 'POST'])
def criar_turma():
    if request.method == 'POST':
        data = request.form
        if not Professor.query.get(data['professor_id']):
            return jsonify({'error': 'Professor não encontrado'}), 404
        data = data.to_dict()
        data['ativo'] = data['ativo'] == 'sim'
        Turma.create_turma(data)
        return redirect(url_for('turmas.listar_turma'))
    return render_template('criar_turma.html')


@turma_blueprint.route('/turmas/atualizar/<int:turma_id>',
                       methods=['GET', 'POST'])
def atualizar_turma(turma_id):
    turma = Turma.get_turma(turma_id)
    if request.method == 'POST':
        data = request.form
        data = data.to_dict()
        data['ativo'] = data['ativo'] == 'sim'
        if not turma:
            return jsonify({'message': 'Turma não encontrada'}), 404
        Turma.update_turma(turma_id, data)
        return redirect(url_for('turmas.listar_turma'))
    return render_template('atualizar_turma.html', turma=turma)


@turma_blueprint.route('/turmas/excluir/<int:turma_id>',
                       methods=['GET', 'POST'])
def excluir_turma(turma_id):
    if not Turma.delete_turma(turma_id):
        return jsonify({'message': 'Turma não encontrada'}), 404
    return redirect(url_for('turmas.listar_turma'))


@turma_blueprint.route('/turmas', methods=['GET'])
def listar_turma():
    turmas = Turma.get_all_turmas()
    turmas_detalhadas = [turma.to_dict() for turma in turmas]
    return render_template('listar_turma.html', turmas=turmas_detalhadas)


@turma_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.get_all_turmas()
    return jsonify([turma.to_dict() for turma in turmas])


@turma_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    data = request.json
    if not Professor.query.get(data['professor_id']):
        return jsonify({'error': 'Professor não encontrado'}), 404
    data['ativo'] = data['ativo'] == 'sim'
    nova_turma = Turma.create_turma(data)
    return jsonify(nova_turma.to_dict()), 201


@turma_blueprint.route('/turmas/<int:turma_id>', methods=['GET'])
def get_turma(turma_id):
    turma = Turma.get_turma(turma_id)
    if not turma:
        return jsonify({'message': 'Turma não encontrada'}), 404
    return jsonify(turma.to_dict())


@turma_blueprint.route('/turmas/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    data = request.json
    data['ativo'] = data['ativo'] == 'sim'
    turma = Turma.update_turma(turma_id, data)
    if not turma:
        return jsonify({'message': 'Turma não encontrada'}), 404
    return jsonify(turma.to_dict())


@turma_blueprint.route('/turmas/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    if not Turma.delete_turma(turma_id):
        return jsonify({'message': 'Turma não encontrada'}), 404
    return jsonify({'message': 'Turma excluída com sucesso'}), 204
