# Criando uma instância de banco no AWS RDS

Passos para criar uma instância e um banco no serviço AWS RDS

## Veja mais detalhes no seguinte exemplo

https://aws.amazon.com/pt/getting-started/hands-on/create-mysql-db

## Crie a instância AWS RDS na sua VPC default 

Para efeito de testes, pode ser na VPC default. Já em um ambiente real, crie uma configuração específica de acordo com o contexto da sua solução.

## Crie a instância em no Grupo de Segurança default

Para efeito de testes, pode ser na VPC default. Já em um ambiente real crie uma configuração específica de acordo com o contexto da sua solução.

Obs: libere o acesso a porta 3306 no grupo de segurança default para permitir a conexão externa (quando for de acesso público). Quando for de acesso privado, libere a porta para o CIRD que vai acessar a instância do banco de dados. 

## Configure o banco para acesso público (apenas para testes)

Após os testes iniciais bem sucedido, altere o acesso do banco para acesso privado. Esta mudança implicará no funcionamento da aplicação rodando em um instância EC2 da VPC configurada da instância do banco. Além disso, será necessário fazer as devidas configurações de acesso de conexão na(s) instancia(s) que vai acessar o banco na VPC previamente configurada.

## Certifique-se de que a instância tenha um banco criado

Na aba configuração da instância selecionada, confirme o nome do banco de dados. Este passo pode ser realizado no momento da criação da instância de acesso ao AWS RDS.

## Capture o endpoint para acessar a instância do banco de trabalho

Na aba Segurança e conexão copie o conteúdo "Endpoint" para salvar na string de conexão da sua aplicação principal.

## Caso tenha optado por acesso ao banco com um usuário próprio da instância do banco

Este passo é realizado durante a criação da nova instância do banco no serviço AWS RDS. Caso tenha escolhido por acessar o banco via IAM, então você deve apontar para a respectiva conta IAM e passar estas credenciais na aplicação principal que vai acessar a instância do banco.

Obs: Nunca compartilhe as informações do usuário admin da instância do banco.