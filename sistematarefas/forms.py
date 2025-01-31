from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from sistematarefas.models import Tarefas
from sqlalchemy import func


class FormCriarTarefas(FlaskForm):
   
    nome_tarefa = StringField('Adicione sua tarefa', validators=[DataRequired(message='Por favor, insira um nome válido.')], render_kw={"placeholder": "Exemplo: 'Ir à academia', 'Fazer compras no supermercado'"})
    descricao = TextAreaField('Descrição',validators=[DataRequired(message='Por favor, insira a descrição da tarefa.')],render_kw={"placeholder": "Escreva uma descrição detalhada aqui..."})
    data_limite = DateField('Data Limite', validators=[DataRequired(message='Por favor, insira uma data válida.')], format='%Y-%m-%d')
    botao_submit = SubmitField('Feito!')

                
    def validate_nome_tarefa(self, nome_tarefa):
        nome_tarefa_normalizado = nome_tarefa.data.strip()
        tarefa_existente = Tarefas.query.filter(func.lower(Tarefas.nome_tarefa) == func.lower(nome_tarefa_normalizado)).first()
        if tarefa_existente:
            raise ValidationError('O nome que você está tentando utilizar já está em uso. Tente outro nome.')


            
            
           
            