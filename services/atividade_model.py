from config import db
from alunos.alunos_model import AlunoService


class Atividade(db.Model):
    id_atividade = db.Column(db.Integer, primary_key=True)
    id_disciplina = db.Column(db.Integer, nullable=False)
    enunciado = db.Column(db.String(500), nullable=False)
    respostas = db.Column(db.JSON, default=[])

    def to_dict(self):
        id_aluno = self.respostas[0]['id_aluno'] if self.respostas else None
        aluno = AlunoService.aluno_por_id(
            id_aluno).to_dict() if id_aluno else None

        return {
            'id_atividade': self.id_atividade,
            'id_disciplina': self.id_disciplina,
            'enunciado': self.enunciado,
            'respostas': self.respostas,
            'aluno': aluno
        }

    @classmethod
    def create_atividade(cls, data):
        try:
            nova_atividade = cls(
                id_disciplina=data['id_disciplina'],
                enunciado=data['enunciado'],
                respostas=data.get('respostas', [])
            )
            db.session.add(nova_atividade)
            db.session.commit()
            return nova_atividade
        except Exception:
            db.session.rollback()
            return None
