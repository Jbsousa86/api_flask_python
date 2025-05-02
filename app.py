from flask import Flask, request, jsonify, render_template
import mysql.connector
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
app.secret_key = '123456789'

# configuarações do banco de dado
try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        auth_plugin="mysql_native_password",
        database=os.getenv("DB_NAME")
    )
    print(" Conexão com MySQL bem-sucedida!")
except mysql.connector.Error as erro:
    print(f" Erro ao conectar no MySQL: {erro}")
    exit()


# pagina do formulário de cadastro
@app.route('/')
def index():
    return render_template('index.html')

# Rota para página de gerenciar alunos
@app.route('/gerenciar_alunos.html')
def gerenciar_alunos():
    return render_template('gerenciar_alunos.html')

# Rota para página de editar aluno
@app.route('/editar_aluno.html')
def editar():
    return render_template('editar_aluno.html')


# rota para cadastrar aluno
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():

    nome = request.form.get('nome')
    email = request.form.get('email')
    matricula = request.form.get('matricula')
    senha = generate_password_hash(request.form.get('senha'))

    


    if not nome or not email or not matricula or not senha:
        return "Todos os campos são obrigatórios!", 400


    cursor = conexao.cursor(dictionary=True)
    cursor.execute("INSERT INTO aluno(nome, email, matricula, senha) VALUES (%s, %s, %s, %s)", (nome, email, matricula, senha))
    conexao.commit()
    cursor.close()

  
    return "aluno cadastrado com sucesso!"
    
      # Rota para listar alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aluno")
    alunos = cursor.fetchall()
    cursor.close()

    lista = []
    for aluno in alunos:
        lista.append({
          'idaluno': aluno['idaluno'],
          'nome': aluno['nome'],
          'email': aluno['email'],
          'matricula': aluno['matricula'],
        })  

    return jsonify(lista)  

  # Rota para atualizar aluno
@app.route('/alunos/<int:idaluno>', methods=['PUT'])
def editar_aluno(idaluno):
    try:
        dados = request.get_json()
        nome = dados.get('nome')
        email = dados.get('email')
        senha = generate_password_hash(dados.get('senha'))


        cursor = conexao.cursor()
        query = """
            UPDATE aluno 
            SET nome = %s, email = %s, senha = %s 
            WHERE idaluno = %s
        """
        cursor.execute(query, (nome, email, senha, idaluno))
        conexao.commit()
        cursor.close()

        return jsonify({'mensagem': 'Aluno atualizado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

    
   

# Rota para deletar aluno
@app.route('/alunos/<int:idaluno>', methods=['DELETE'])
def deletar_aluno(idaluno):
    cursor = conexao.cursor()

    # Primeiro, verifica se o aluno existe
    cursor.execute("SELECT * FROM aluno WHERE idaluno = %s", (idaluno,))
    aluno = cursor.fetchone()

    if aluno is None:
        cursor.close()
        return jsonify({"erro": "Aluno não encontrado"}), 404

    # Se existe, deleta
    cursor.execute("DELETE FROM aluno WHERE idaluno = %s", (idaluno,))
    conexao.commit()
    cursor.close()

    return jsonify({"mensagem": "Aluno removido com sucesso!"})

if __name__ == '__main__':

    app.run(debug=True) 
