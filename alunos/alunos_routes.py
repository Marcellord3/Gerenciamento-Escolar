from flask import Blueprint, request, jsonify, render_template, redirect, \
    url_for
from .alunos_model import AlunoService, AlunoNaoEncontrado

alunos_blueprint = Blueprint('alunos', __name__)


@alunos_blueprint.route('/alunos/criar', methods=['GET', 'POST'])
def criar_alunos():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['nota_primeiro_semestre'] = float(
            data.get('nota_primeiro_semestre', 0))
        data['nota_segundo_semestre'] = float(
            data.get('nota_segundo_semestre', 0))
        novo_aluno = AlunoService.adicionar_aluno(data)
        if novo_aluno is None:
            return jsonify({'error': 'Turma não encontrada.'}), 404
        return redirect(url_for('alunos.listar_alunos'))
    return render_template('criar_alunos.html')


@alunos_blueprint.route('/alunos/atualizar/<int:id_aluno>',
                        methods=['GET', 'POST'])
def atualizar_alunos(id_aluno):
    try:
        aluno = AlunoService.aluno_por_id(id_aluno)
    except AlunoNaoEncontrado as e:
        return jsonify({'message': str(e)}), 404

    if request.method == 'POST':
        data = request.form.to_dict()
        data['nota_primeiro_semestre'] = float(
            data.get('nota_primeiro_semestre', 0))
        data['nota_segundo_semestre'] = float(
            data.get('nota_segundo_semestre', 0))
        try:
            AlunoService.atualizar_aluno(id_aluno, data)
            return redirect(url_for('alunos.listar_alunos'))
        except AlunoNaoEncontrado as e:
            return jsonify({'message': str(e)}), 404
    return render_template('atualizar_alunos.html', aluno=aluno)


@alunos_blueprint.route('/alunos/excluir/<int:id_aluno>',
                        methods=['GET', 'POST'])
def excluir_alunos(id_aluno):
    if request.method == 'POST':
        try:
            AlunoService.excluir_aluno(id_aluno)
            return redirect(url_for('alunos.listar_alunos'))
        except AlunoNaoEncontrado as e:
            return jsonify({'message': str(e)}), 404
    else:
        try:
            aluno = AlunoService.aluno_por_id(id_aluno)
            return render_template('excluir_alunos.html', aluno=aluno)
        except AlunoNaoEncontrado as e:
            return jsonify({'message': str(e)}), 404


@alunos_blueprint.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = AlunoService.listar_alunos()
    return render_template('listar_alunos.html', alunos=alunos)


@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    required_fields = ['nome', 'turma_id', 'data_nascimento',
                       'nota_primeiro_semestre', 'nota_segundo_semestre']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    data['nota_primeiro_semestre'] = float(
        data.get('nota_primeiro_semestre', 0))
    data['nota_segundo_semestre'] = float(data.get('nota_segundo_semestre', 0))
    novo_aluno = AlunoService.adicionar_aluno(data)
    if novo_aluno is None:
        return jsonify({'error': 'Turma não encontrada.'}), 404
    return jsonify(novo_aluno.to_dict()), 201


@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = AlunoService.aluno_por_id(id_aluno)
        return jsonify(aluno.to_dict())
    except AlunoNaoEncontrado as e:
        return jsonify({'message': str(e)}), 404


@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    data = request.get_json()
    data['nota_primeiro_semestre'] = float(
        data.get('nota_primeiro_semestre', 0))
    data['nota_segundo_semestre'] = float(data.get('nota_segundo_semestre', 0))
    try:
        aluno_atualizado = AlunoService.atualizar_aluno(id_aluno, data)
        return jsonify(aluno_atualizado.to_dict())
    except AlunoNaoEncontrado as e:
        return jsonify({'message': str(e)}), 404


@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        AlunoService.excluir_aluno(id_aluno)
        return '', 204
    except AlunoNaoEncontrado as e:
        return jsonify({'message': str(e)}), 404
