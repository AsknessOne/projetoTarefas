from sistematarefas import database
from datetime import datetime

class Tarefas(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_tarefa = database.Column(database.String, unique=True, nullable=False)
    descricao =  database.Column(database.Text, nullable=False)
    data_limite = database.Column(database.DateTime, nullable=False)
    is_completed = database.Column(database.Boolean, default=False) 
    data_criacao = database.Column(database.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Tarefa {self.nome_tarefa}>'