import smtplib
import email.message
from config.db import conecta_ao_banco
from credentials.credentials import email_credentials

conexao, cursor = conecta_ao_banco() # Iniciando o Sql server

class Leads:
    """
    Classe responsável por armazenar o Lead da vez.
    Isso facilita pra quando o sistema identifica uma troca de status, entao apenas acionamos a função da classe que já estara com suas informações para poder mexermos no sistema

    Args: O argumento utilizado é o id. Com isso, consegue puxar as colunas do nosso Banco de dados para conseguirmos trabalhar de forma mais dinamica e facil.
    """

    def __init__(self, id):
        """
        Função que inicia a nossa classe. Ao passar o id já pegamos o chamado completo no sql e armazenamos nas variaveis

        Args: Id do chamado
        """
        self.id = int(id)

        # Pegando no sql o chamado completo de acordo com o ID
        cursor.execute("SELECT * FROM Leads WHERE ID = ?", (id,))
        lead_ = cursor.fetchone()


        # Se o chamado existir atribuimos as informações
        if lead_:
            self.contact_first_name =  lead_[1]
            self.contact_full_name =  lead_[2]
            self.contact_phone_number = lead_[3]
            self.email = lead_[4]
            self.date_created = lead_[5].strftime("%Y-%m-%d")
            self.suburb = lead_[6]
            self.category = lead_[7]
            self.details = lead_[8]
            self.price = float(lead_[9])
            self.status = lead_[10]
        else:
            raise ValueError("Lead não encontrado")
        
    
    def enviar_email(self, corpo_email, subject):
        """
        Função que conecta ao serviço de email do google e envia o email.

        Args: Passado o conteudo que vai ser enviado no email e o assundo.
        """

        # Informações para envio e recebimento do email.
        self.email_from, self.password_from = email_credentials()
        self.email_to = 'vendas@test.com' # Caso queira enviar email para a pessoa que abriu chamado é apenas trocar o valor por self.email
        
        

        try:
            msg = email.message.Message()
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            password = self.password_from
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email)
            s = smtplib.SMTP('smtp.gmail.com: 587')

            s.starttls()
            
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print('Email enviado')
        except BaseException as e:
            print(f'Não foi possível realizar o envio do email: {e}')


    def status_accepted(self): #atualiza no banco de dados
        """
        Toda a logica por dentro quando o user aceita um lead
        Temos 2 funções dentro: Enviar email que aciona a função enviar_email da classe e passa o que quer no envio do email
        E a função que verifica se o preço é acima de 500. Assim, aplica 10% de desconto.
        """

        def email_accepted(self):
            # Conteudo do email
            corpo_email = f"""
            <h1>Notificação de Novo Lead Aceito: #ID_{self.id}</h1><br>
            ----------------------------------<br>
            <br>
            <p>
            Nome: {self.contact_full_name}<br>
            Telefone: {self.contact_phone_number}<br>
            Email: {self.email}<br>
            Local: {self.suburb}<br>
            Data Criação: {self.date_created}<br>
            <br>
            **********************************
            <br>
            Categoria: {self.category}<br>
            <br>
            Detalhes: {self.details}<br>
            <br>
            Preço: {self.price}<br>
            </p>
            """
            # Titulo do email
            subject = f"#ID_{self.id} | notificacao_lead_aceito"

            # Acionando o envio
            self.enviar_email(corpo_email, subject)
            

        def preco_acima500(self):   
            
            price = self.price

            #Verificando se o valor é maior que 500
            if price > 500:            
                price = price - (price * 0.10)
                cursor.execute("UPDATE Leads SET Price = ? WHERE ID = ?", (price, self.id))
                conexao.commit()

        # Mudando o status do chamado para Accepted
        cursor.execute("UPDATE Leads SET Statu = ? WHERE ID = ?", ('Accepted', self.id))
        conexao.commit()

        # Executando as duas funções
        preco_acima500(self)
        email_accepted(self)
                      

    def status_declined(self):
        # apenas muda o status do chamado para recusado
        cursor.execute("UPDATE Leads SET Statu = ? WHERE ID = ?", ('Declined', self.id))
        conexao.commit()


    def status_finalized(self):
        """
        Quando temos um chamado e queremos tirar do site, clicamos em finalizar, 
        isso irá acionar essa função que vai enviar um email de chamado encerrado atualiza no banco de dados o status
        """
        
        def email_finalized(self):
            # Conteudo do email
            corpo_email = f"""
            <h1>Notificação | Lead Finalizado: #ID_{self.id}</h1><br>
            ----------------------------------<br>
            <br>
            <p>
            Nome: {self.contact_full_name}<br>
            Telefone: {self.contact_phone_number}<br>
            Email: {self.email}<br>
            <br>
            **********************************
            <br>
            Categoria: {self.category}<br>
            <br>
            Detalhes: {self.details}<br>
            <br>
            Preço: {self.price}<br>
            </p>
            """
            # Titulo do email
            subject = f"#ID_{self.id} | notificacao_lead_finalized"

            # Acionando o envio
            self.enviar_email(corpo_email, subject)
            
        # Atualizando status no Banco
        cursor.execute("UPDATE Leads SET Statu = ? WHERE ID = ?", ('Finalized', self.id))
        conexao.commit()

        #Enviando email
        email_finalized(self)
