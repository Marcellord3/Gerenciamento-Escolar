from config import app, db
from alunos.alunos_routes import alunos_blueprint
from professor.professor_routes import professor_blueprint
from turma.turma_routes import turma_blueprint
from services.atividade_routes import atividade_blueprint

app.register_blueprint(alunos_blueprint, url_prefix='/alunos')
app.register_blueprint(professor_blueprint, url_prefix='/professores')
app.register_blueprint(turma_blueprint, url_prefix='/turmas')
app.register_blueprint(atividade_blueprint, url_prefix='/atividades')


@app.route('/')
def index():
    return "Bem-vindo ao Sistema de Gerenciamento Escolar"


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=app.config["HOST"],
            port=app.config['PORT'], debug=app.config['DEBUG'])
