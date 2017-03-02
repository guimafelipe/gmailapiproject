# RH Project

## O que é este projeto?
É um projeto feito para o setor de RH com o objetivo de automatizar a transferência de currículos do e-mail de vagas para a plataforma a ser utilizada.

Foi implementado usando o GMail API em python.

## Como baixar a API do Gmail?

* Primeiro, tenha Python (2.6 no mínimo) instalado em seu computador.
* Tenha o pip: https://pypi.python.org/pypi/pip
* Instale a GMail API através do pip:

> pip install --upgrade google-api-python-client

## Como executar o código?

Siga as instruções do site da Google para criar um projeto e gerar as credenciais necessárias para que a API possa acessar sua conta:

> https://developers.google.com/gmail/api/quickstart/python

Tendo movido o json para o mesmo diretório em que está o código em python, basta executá-lo:

> python quickstart.py

E basta conceder as permissões necessárias e o programa poderá ser executado.
