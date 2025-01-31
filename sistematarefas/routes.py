
from flask import render_template, redirect, url_for, flash, request
from sistematarefas import app, database
from sistematarefas.forms import FormCriarTarefas
from datetime import datetime
from sqlalchemy import func 
from sistematarefas.models import Tarefas



# Rota para a página principal. Ordena as tarefas pela data e coloca as pendentes acima.
@app.route('/')
def homePage():
    """
    Carrega a página principal da aplicação, listando as tarefas.
    
    As tarefas são ordenadas por status (pendentes primeiro) e data de vencimento.

    Returns:
        render_template: Retorna o template 'index.html' com a lista de tarefas.
    """
    tarefas = Tarefas.query.order_by(Tarefas.is_completed.asc(), Tarefas.data_limite.asc()).all()
    return render_template('index.html', tarefas=tarefas)

# Criação de tarefas, possui tratamento para caso haja algum erro ao tentar adicionar.
@app.route('/tarefas', methods=['GET', 'POST'])
def criarTarefa():
    """
    Cria uma nova tarefa.
    A tarefa é criada a partir dos dados do formulário e validada.

    Returns:
    redirect: Redireciona para a página principal..
    render_template: Retorna o template 'tarefas.html' caso ocorra um erro.
    
    Raises:
        ExceptionError: Erro ao salvar as alterações no banco de dados.
    
    """
    formTarefas = FormCriarTarefas() 
    if request.method == 'POST' and formTarefas.validate_on_submit():
        tarefa = Tarefas(
            nome_tarefa=formTarefas.nome_tarefa.data,
            descricao=formTarefas.descricao.data,
            data_limite=formTarefas.data_limite.data,
            is_completed=False
        )
        try:
            database.session.add(tarefa)
            database.session.commit()
            flash('Tarefa adicionada com sucesso!', 'alert-success')
            return redirect(url_for('homePage'))
        except Exception as e:
            database.session.rollback()
            flash('Ocorreu um erro ao adicionar a tarefa. Tente novamente!', 'alert-danger')
            print(f'Erro da exceção: {e}')
    return render_template('tarefas.html', formTarefas=formTarefas)


# Edição de tarefa, procura pelo ID e atualiza. Não permite alterar para uma de mesmo nome assim como na criação.
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """
    Permite editar uma tarefa que já foi adicionada.

    Args:
        id (int): Identificador único da tarefa a ser editada.
    
    Raises:
        ExceptionError: Erro ao ao salvar as alterações no banco de dados.
    
    """
    tarefa = Tarefas.query.get_or_404(id)
    
    if request.method == 'POST':
        novo_nome_tarefa = request.form['nome'].strip()

        # Verifica se já existe outra tarefa com o mesmo nome (ignora maiúsculas/minúsculas)
        tarefa_existente = Tarefas.query.filter(
            func.lower(Tarefas.nome_tarefa) == func.lower(novo_nome_tarefa),
            Tarefas.id != id  # Garante que não seja a própria tarefa
        ).first()

        if tarefa_existente:
            flash('Já existe uma tarefa com esse nome. Escolha outro.', 'alert-danger')
            return redirect(url_for('homePage', id=id))
        
        # Atualiza os dados da tarefa
        tarefa.nome_tarefa = novo_nome_tarefa
        tarefa.descricao = request.form['descricao']
        tarefa.data_limite = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        
        try:
            database.session.commit()
            flash('Tarefa alterada com sucesso!', 'alert-warning')
        except Exception as e:
            database.session.rollback()
            flash('Ocorreu um erro ao editar a tarefa. Tente novamente!', 'alert-danger')
            print(f'Erro da exceção: {e}')
        
        return redirect(url_for('homePage'))
    
    tarefas = Tarefas.query.all()
    flash('Erro: A página de edição não foi encontrada.', 'alert-danger')
    return render_template('index.html', tarefas=tarefas)


# Exclusão de tarefa, busca pelo ID.
@app.route('/excluirTarefa/<int:id>', methods=['GET', 'POST'])
def excluirTarefa(id):  
    """
    Permite excluir uma tarefa que já foi adicionada.

    Args:
        id (int): Identificador único da tarefa a ser editada.
    
    Raises:
        ExceptionError: Erro ao ao salvar as alterações no banco de dados.
    
    """
    tarefa_excluir = Tarefas.query.get_or_404(id)
    try:
        database.session.delete(tarefa_excluir)
        database.session.commit()
        flash('🗑️ Tarefa removida com sucesso!', 'alert-warning')
    except Exception as e:
        database.session.rollback()
        flash('Erro ao excluir a tarefa.', 'alert-danger')
        print(f'Erro ao excluir: {e}')
    
    return redirect(url_for('homePage'))



# Marcar tarefa como concluída. 
@app.route('/completar/<int:id>', methods=['POST'])
def completar(id):
    """
    Permite marcar a tarefa adicionada como concluída.
    
    Raises:
        ExceptionError: Erro ao fazer o commit no banco de dados.
    """
    tarefa = Tarefas.query.get_or_404(id)
    tarefa.is_completed = not tarefa.is_completed  
    try:
        database.session.commit()
        if tarefa.is_completed:
            flash('Tarefa concluída com sucesso! ✅ ', 'alert-success')
    except Exception as e:
        database.session.rollback()
        flash('Erro ao atualizar o status da tarefa.', 'alert-danger')
        print(f'Erro ao completar: {e}')
    return redirect(url_for('homePage'))
     




    





        
    