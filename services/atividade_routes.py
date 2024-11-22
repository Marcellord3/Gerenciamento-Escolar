from flask import Blueprint, request, jsonify, render_template, redirect, \
    url_for
from .atividade_model import Atividade

atividade_blueprint = Blueprint('atividades', __name__)


@atividade_blueprint.route('/atividades/criar', methods=['GET', 'POST'])
def criar_atividade():
    if request.method == 'POST':
        data = request.form.to_dict()
        nova_atividade = Atividade.create_atividade(data)
        if nova_atividade:
            return redirect(url_for('atividades.listar_atividades'))
        return jsonify({'error': 'Erro ao criar a atividade.'}), 500
    return render_template('criar_atividade.html')


@atividade_blueprint.route('/atividades/atualizar/<int:id_atividade>',
                           methods=['GET', 'POST'])
def atualizar_atividade(id_atividade):
    atividade = Atividade.get_atividade(id_atividade)
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada.'}), 404
    if request.method == 'POST':
        data = request.form.to_dict()
        atividade_atualizada = Atividade.update_atividade(id_atividade, data)
        if not atividade_atualizada:
            return jsonify({'error': 'Erro ao atualizar atividade.'}), 400
        return redirect(url_for('atividades.listar_atividades'))
    return render_template('atualizar_atividade.html',
                           atividade=atividade.to_dict())


@atividade_blueprint.route('/atividades/excluir/<int:id_atividade>',
                           methods=['GET', 'POST'])
def excluir_atividade(id_atividade):
    if request.method == 'POST':
        if not Atividade.delete_atividade(id_atividade):
            return jsonify({'error': 'Atividade não encontrada.'}), 404
        return redirect(url_for('atividades.listar_atividades'))
    else:
        atividade = Atividade.get_atividade(id_atividade)
        if not atividade:
            return jsonify({'error': 'Atividade não encontrada.'}), 404
        return render_template('excluir_atividade.html',
                               atividade=atividade.to_dict())


@atividade_blueprint.route('/atividades/listar', methods=['GET'])
def listar_atividades():
    atividades = Atividade.get_all_atividades()
    return render_template('listar_atividades.html', atividades=[
        atividade.to_dict() for atividade in atividades])


@atividade_blueprint.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = Atividade.get_all_atividades()
    return jsonify([atividade.to_dict() for atividade in atividades]), 200


@atividade_blueprint.route('/atividades/<int:id_atividade>', methods=['GET'])
def get_atividade(id_atividade):
    atividade = Atividade.get_atividade(id_atividade)
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada.'}), 404
    return jsonify(atividade.to_dict()), 200


@atividade_blueprint.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()
    if not data or 'id_disciplina' not in data or 'enunciado' not in data:
        return jsonify({'error': 'Todos os campos são obrigatórios.'}), 400
    nova_atividade = Atividade.create_atividade(data)
    return jsonify(nova_atividade.to_dict()), 201


@atividade_blueprint.route('/atividades/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    data = request.get_json()
    atividade = Atividade.update_atividade(id_atividade, data)
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada.'}), 404
    return jsonify(atividade.to_dict()), 200


@atividade_blueprint.route('/atividades/<int:id_atividade>',
                           methods=['DELETE'])
def delete_atividade(id_atividade):
    if not Atividade.delete_atividade(id_atividade):
        return jsonify({'error': 'Atividade não encontrada.'}), 404
    return '', 204
