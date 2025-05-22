from config.db import conecta_ao_banco
from classes.Leads import Leads
from flask import Flask, render_template, request, redirect, url_for

# Iniciando flask
app = Flask(__name__)

# realizando conexao com o banco de dados
conexao, cursor = conecta_ao_banco()

@app.route('/')
def view_home():
    """
    Rota incial. Ao abrir o serviço, já nos deparamos com a renderição da página leads
    e o envio das leads Invited e accepted separadamente para exibirmos no front

    Returns: renderização de leads.html e envio de leads invited e accepted por arquivo json
    """

    # Selecionando os leads que ainda não foram aceitos
    query = list(cursor.execute("SELECT * FROM Leads WHERE Statu = ?", ('Invited',)))
    
    # Passando os itens por arquivo json
    leads_invited = [
        {
            'id': int(item[0]),
            'username': item[1],
            'date_created': item[5].strftime("%Y-%m-%d"), # a data estava vindo em um tipo diferente que nao era compativel. Foi preciso formatar
            'suburb': item[6],
            'category': item[7],
            'details': item[8],
            'price': float(item[9]),
            'status': item[10]
        }
        for item in query
    ]
    # Selecionando os leads que ainda já foram aceitos
    query = list(cursor.execute("SELECT * FROM Leads WHERE Statu = ?", ('Accepted',)))

    leads_accepted = [
        {
            'id': int(item[0]),
            'username': item[2],
            'contact_phone_number': item[3],
            'email': item[4],
            'date_created': item[5].strftime("%Y-%m-%d"),
            'suburb': item[6],
            'category': item[7],
            'details': item[8],
            'price': float(item[9]),
            'status': item[10]
        }
        for item in query
    ]

    # renderizando a pagina e passando os dois arquivos json
    return render_template('leads.html', leads_invited=leads_invited, leads_accepted=leads_accepted)
 

@app.route('/accepted_declined', methods=['POST'])
def leads_accept_declined():
    """
    Função responsável por identificar a opção do usuario e chamar a função correspondente.
    Estamos iniciando a nossa classe Leads por meio do ID do chamado. assim, conseguimos garantir o resultado esperado.

    Returns: Estamos redirecionando para a pagina principal. Isso faz com que não precisemos de uma segunda página, mantendo a simulação de um SPA
    """

    decisao = str(request.form['decisao_lead']).split('|') #Separando a resposta por item para conseguirmos iniciar a classe
    chamado = Leads(int(decisao[1])) # Iniciando a classe com o ID
    
    # Estamos executando a função de acordo com o botao clicado
    match decisao[0]:
        case 'accepted': chamado.status_accepted()
        case _: chamado.status_declined()

    return redirect(url_for('view_home'))


@app.route('/finalized', methods=['POST'])
def leads_finalized():
    """
    Essa função identifica quando o botao de finalizar lead é apertado, entao ele manda um sinal para a função dentro da classe que irá finalizar o chamado

    Returns: redirecionamento para a pagina inicial.
    """

    decisao = str(request.form['finalizar']).split('|')#Separando a resposta por item para conseguirmos iniciar a classe
    chamado = Leads(int(decisao[1])) # Iniciando a classe com o ID

    chamado.status_finalized() # chamando função

    return redirect(url_for('view_home'))


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()