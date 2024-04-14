# Dependências

## Flask:

1. Framework Python para desenvolvimento web microframework, leve e fácil de usar.
2. Permite criar interfaces web dinâmicas e APIs RESTful com Python.
3. Sua aplicação Flask utiliza o Flask para gerenciar o roteamento de URLs, manipulação de requisições e respostas HTTP, e renderização de templates.

## Flask-SQLAlchemy:

1. Extensão do Flask que facilita a integração com bancos de dados relacionais.
2. Permite definir modelos de dados e realizar operações CRUD (Create, Read, Update, Delete) com SQL.
3. Sua aplicação Flask utiliza o Flask-SQLAlchemy para mapear seus modelos de dados para tabelas no banco de dados, realizar consultas e manipular dados.

## AWS S3 boto:

1. Biblioteca Python para interagir com o serviço de armazenamento de objetos Amazon S3.
2. Permite realizar operações como upload, download, deleção e gerenciamento de arquivos no S3.
3. Sua aplicação Flask utiliza o AWS S3 boto para armazenar arquivos estáticos, como imagens e scripts, ou para persistir dados de forma escalável e segura.

## Biblioteca requests

Permite interagir com APIs e outros recursos da web. Ela simplifica o processo de enviar e receber solicitações HTTP, permitindo que você acesse dados, publique informações e integre seu programa com diversos serviços online.

## Biblioteca pymysql

PyMySQL é uma biblioteca Python popular que facilita a interação com bancos de dados MySQL. Ela fornece uma interface simples para conectar a servidores MySQL, executar consultas SQL e gerenciar dados do banco de dados. A biblioteca PyMySQL é conhecida por sua eficiência e aderência ao protocolo MySQL, tornando-se uma escolha confiável para o desenvolvimento de aplicações baseadas em MySQL.

## Flask-Login:

Uma extensão do Flask que facilita a implementação de autenticação e autorização em aplicações web Flask.

1. Sistema de login e logout simples.
2. Suporte para sessões de usuário e gerenciamento de permissões.
3. Integração com bancos de dados para armazenamento de dados de login.
4. Proteção contra ataques CSRF (Cross-Site Request Forgery).

## Flask-WTF:

Uma extensão do Flask que simplifica a validação e manipulação de formulários em aplicações web Flask.

1. Integração com o framework WTForms para validação de campos de formulário.
2. Criação e renderização de formulários HTML com validação integrada.
3. Manipulação de dados de formulário submetidos e detecção de erros de validação.
4. Integração com Flask-Classy para validação em modelos de formulário.

## Email Validator

Uma biblioteca Python para validar endereços de e-mail.

1. Valida a sintaxe de endereços de e-mail.
2. Detecta e elimina endereços de e-mail inválidos ou malformados.
3. Suporte para diversos formatos de endereços de e-mail.
4. Fácil de integrar em aplicações Python que manipulam endereços de e-mail.

## Referências: 

Flask - https://flask.palletsprojects.com

Flask-SQLAlchemy - https://flask-sqlalchemy.palletsprojects.com

boto3 - https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

requests - https://requests.readthedocs.io/en/latest

pymysql - https://github.com/PyMySQL/PyMySQL

Flask-login - https://flask-login.readthedocs.io

Flask-WTD - https://flask-wtf.readthedocs.io

Email validator - https://pypi.org/project/email-validator
