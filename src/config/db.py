import pyodbc


# Trocar os parametros para sua realidade
def conecta_ao_banco(DRIVER='ODBC Driver 17 for SQL SERVER', 
                     SERVER='localhost\\SQLEXPRESS', 
                     DATABASE='desafio_mrv', 
                     USERNAME=None, 
                     PASSWORD=None, 
                     TRUSTED_CONNECTION='yes'):
    
    """
    Função responsável por conectar ao SQL Server utilizando a biblioteca pyodbc.
    Caso o programa não consiga realizar a conexão, irá informar o erro e finalizar o código

    Args: Os argumentos passados são configuração do banco de dado para que a biblioteca consiga identicar
    
    Returns: Conexão e cursor. Cursor é utilizado como uma Query, apenas chamalo e digitar o comando de consulta dentro dele
    """

    string_conexao = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TRUSTED_CONNECTION={TRUSTED_CONNECTION};'
    
    # Tentando se conectar e caso não conseguir, finaliza o código.
    try:
        conexao = pyodbc.connect(string_conexao)
        cursor = conexao.cursor()

    except BaseException as e:
        print(f'Erro ao se conectar com o Banco de dados. {e}')
        exit()

    return conexao, cursor
