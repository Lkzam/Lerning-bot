import sqlite3
import re

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect("error_solutions.db")
cursor = conn.cursor()

# Criar a tabela para armazenar erros e soluções
cursor.execute('''CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY,
                    error_description TEXT NOT NULL,
                    solution TEXT NOT NULL
                  )''')
conn.commit()

def add_error_solution(error_description, solution):
    cursor.execute("INSERT INTO errors (error_description, solution) VALUES (?, ?)", (error_description, solution))
    conn.commit()
    print("Erro e solução adicionados com sucesso.")

def get_keywords(text):
    keywords = re.findall(r'\b(?!de|para|o|a|e|não|um|uma|com)\w+', text.lower())
    return ' '.join(keywords)

def get_solution(error_description):
    keywords = get_keywords(error_description)
    cursor.execute("SELECT solution FROM errors WHERE error_description LIKE ?", ('%' + keywords + '%',))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return "Erro não encontrado. Adicione uma nova solução."

def list_all_errors():
    cursor.execute("SELECT id, error_description, solution FROM errors")
    results = cursor.fetchall()
    if results:
        print("Erros e soluções cadastrados:")
        for row in results:
            print(f"ID: {row[0]} | Erro: {row[1]} | Solução: {row[2]}")
    else:
        print("Nenhum erro cadastrado.")

def edit_error_solution(error_id, new_error_description=None, new_solution=None):
    if new_error_description:
        cursor.execute("UPDATE errors SET error_description = ? WHERE id = ?", (new_error_description, error_id))
    if new_solution:
        cursor.execute("UPDATE errors SET solution = ? WHERE id = ?", (new_solution, error_id))
    conn.commit()
    print("Erro ou solução editados com sucesso.")

def delete_error_solution(error_id):
    cursor.execute("DELETE FROM errors WHERE id = ?", (error_id,))
    conn.commit()
    print("Erro e solução apagados com sucesso.")

def assistente_erro():
    while True:
        user_input = input("\nDigite o erro que você está enfrentando, 'listar' para ver todos os erros, 'editar' para modificar um erro, 'apagar' para deletar um erro, ou 'sair' para encerrar: ").strip()
        if user_input.lower() == 'sair':
            print("Encerrando a assistente de erro.")
            break
        elif user_input.lower() == 'listar':
            list_all_errors()
        elif user_input.lower() == 'editar':
            error_desc = input("Digite a descrição do erro que deseja editar: ")
            matches = search_error(error_desc)
            if matches:
                print("Erros encontrados:")
                for match in matches:
                    print(f"ID: {match[0]} | Erro: {match[1]} | Solução: {match[2]}")
                selected_id = int(input("Digite o ID do erro que deseja editar: "))
                new_error = input("Nova descrição do erro (deixe em branco para manter a atual): ")
                new_solution = input("Nova solução (deixe em branco para manter a atual): ")
                edit_error_solution(selected_id, new_error_description=new_error or None, new_solution=new_solution or None)
            else:
                print("Nenhum erro encontrado para editar.")
        elif user_input.lower() == 'apagar':
            list_all_errors()
            selected_id = int(input("Digite o ID do erro que deseja apagar: "))
            delete_error_solution(selected_id)
        else:
            solution = get_solution(user_input)
            if solution == "Erro não encontrado. Adicione uma nova solução.":
                print(solution)
                new_solution = input("Por favor, forneça a solução para este erro: ")
                add_error_solution(user_input, new_solution)
            else:
                print(f"Solução encontrada: {solution}")

# Executar a assistente
assistente_erro()

# Fechar a conexão com o banco de dados ao finalizar
conn.close()
