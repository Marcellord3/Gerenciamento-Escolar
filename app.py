from config import app, db
from alunos.alunos_routes import alunos_blueprint
from professor.professor_routes import professor_blueprint
from turma.turma_routes import turma_blueprint
from services.atividade_routes import atividade_blueprint

def create_app():
    myApp = app

    myApp.register_blueprint(alunos_blueprint)
    myApp.register_blueprint(professor_blueprint)
    myApp.register_blueprint(turma_blueprint)
    myApp.register_blueprint(atividade_blueprint)

    with myApp.app_context():
        db.create_all()

    return myApp

if __name__ == '__main__':
    myApp = create_app()
    myApp.run(host=myApp.config["HOST"], port=myApp.config['PORT'], debug=myApp.config['DEBUG'])
