from flask import Blueprint, request, jsonify, render_template, redirect, \
    url_for
from .professor_model import Professor

professor_blueprint = Blueprint('professores', __name__)


@professor_blueprint.route('/professores/criar', methods=['GET', 'POST'])
def criar_professor():
    if request.method == 'POST':
        Professor.create_professor(request.form)
        return redirect(url_for('professores.listar_professores'))
    return render_template('criar_professor.html')


@professor_blueprint.route('/professores/atualizar/<int:professor_id>',
                           methods=['GET', 'POST'])
def atualizar_professor(professor_id):
    professor = Professor.get_professor(professor_id)
    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404
    if request.method == 'POST':
        Professor.update_professor(professor_id, request.form)
        return redirect(url_for('professores.listar_professores'))
    return render_template('atualizar_professor.html', professor=professor)


@professor_blueprint.route('/professores/excluir/<int:professor_id>',
                           methods=['GET', 'POST'])
def excluir_professor(professor_id):
    if not Professor.delete_professor(professor_id):
        return jsonify({'message': 'Professor não encontrado'}), 404
    return redirect(url_for('professores.listar_professores'))


@professor_blueprint.route('/professores', methods=['GET'])
def listar_professores():
    return render_template('listar_professores.html',
                           professores=Professor.get_all_professores())


@professor_blueprint.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(
        [professor.to_dict() for professor in Professor.get_all_professores()])


@professor_blueprint.route('/professores', methods=['POST'])
def create_professor():
    professor = Professor.create_professor(request.json)
    return jsonify(professor.to_dict()), 201


@professor_blueprint.route('/professores/<int:professor_id>',
                           methods=['PUT'])
def update_professor(professor_id):
    professor = Professor.update_professor(professor_id, request.json)
    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404
    return jsonify(professor.to_dict())


@professor_blueprint.route('/professores/<int:professor_id>',
                           methods=['DELETE'])
def delete_professor(professor_id):
    if not Professor.delete_professor(professor_id):
        return jsonify({'message': 'Professor não encontrado'}), 404
    return jsonify({'message': 'Professor excluído com sucesso'}), 204
