
# Desafio MRV

App feito em Flask para gerenciar leads conectando ao SQL Server. Você pode aceitar, recusar e finalizar leads diretamente pela interface, e o sistema envia notificações por email automaticamente.

## O que o app faz

- Lista leads Invited e leads Accepted
- Permite aceitar ou recusar leads
- Finaliza leads aceitos
- Envia email notificando as ações feitas nos leads
- Aplica desconto automático para leads com preço maior que R$ 500

## Como usar

1. Clone o projeto e entre na pasta

```bash
git clone https://github.com/arthurrsn/desafio_mrv.git
cd desafio_mrv 
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows    
```

3. Instale as dependências

```bash
pip install -r requirements.txt
```

4. Configure suas credenciais de email e banco de dados
    - Em src/credentials/credentials.py coloque seu email e senha

      ```python
      def email_credentials():
          email = 'email'
          password = 'senha'

          return email, password
      ```
      
    - Em src/db.py configure os dados de conexão com seu SQL Server

5. Rode o app

```bash
python src/app.py # Linux/Mac
python src\app.py # Windows
```

6. Acesse no navegador: http://127.0.0.1:5000

---

## 🧪 Como inserir dados de teste no banco SQL Server

Para que o app funcione corretamente logo após a instalação, você pode copiar os dados de exemplos no seu SQL Server com as instruções abaixo:

1. Abra o arquivo src/config/arquivo_testes_db.txt

2. Copie tudo e cole em uma nova query dentro do SQL Server.

Obs: Lembre configurar seu banco de dados com as informações para a conexão correta.

---

## 📸 Execução

Abaixo uma imagem de como o sistema aparece durante a execução:

![image](https://github.com/user-attachments/assets/57b249a5-19bc-4928-a259-1d41425d2c9c)

