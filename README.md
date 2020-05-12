## O que é
O one-pass-vault é uma biblioteca insparada no [aws-vault](https://github.com/99designs/aws-vault) que visa deixar o desenvolvimento local e administração de senhas mais segura. É uma CLI (command-line interface) que interage com o 1password coletando as credenciais requisitadas e lançando elas como variáveis ambiente para serem consumidas por comandos que são incluídos como argumento na command-line do one-pass-vault. Vale ressaltar que nenhuma dessas variáveis ambiente criadas pelo one-pass-vault persiste no sistema, elas só existirão dentro do processo gerado pelo comando do one-pass-vault e ao fim da execução elas somem.

## Instalação

1. Baixar CLI do OP:  https://app-updates.agilebits.com/product_history/CLI
2. Unzip & mover op  pro /bin
3. Clonar repo do one-pass-vault
4. pip3 install <path_to>/one-pass-vault 

## Como funciona
O único comando disponível, no momento, é:
```shell
one-pass-vault --item=<nome das credenciais separadas por virgula> exec <profile-name> -- <cmd>
```
* **one-pass-vault**: função principal que irá chamar outras funções da biblioteca
* **--item**: lista de credenciais que o usuário quer coletar no 1password (separadas por virgulas)
* **exec**: função responsável por credenciar o `profile-name` e executar o `cmd`
* **profile-name**: alias de um perfil do 1password você cadastrou no one-pass-vault. Caso você não tenha um perfil cadastrado, um fluxo de cadastro é iniciado antes de continuar a execução do comando.
* **cmd**: comando o qual você quer executar após todo fluxo anterior de cadastro ou credenciamento e coleta de credenciais selecionadas no 1password.

Exemplo:
```shell
one-pass-vault --item=app_cred_1,db_cred_2 exec personal -- docker-compose up -d
```
O processo de execução desse comando acontece da seguinte forma:
1. A função `one-pass-vault` recebe os argumentos e faz o parse deles
2. A função exec é chamada e recebe o valor de `--item`, `profile-name` e o `cmd`
3. O fluxo da `exec` é:
    1. Autenticar. A classe **OnePassAuth** é responsável autentica ou registra o `profile-name` (personal) e se loga no 1password. Existem alguns fluxos de checar a validade do session-token e caso ele ja esteja inválido, outro é gerado.
    2. Fazer request e receber a `response` em json. A classe **OnePass** é responsável por fazer os requests ao 1password e pegar os objetos requisitados. No momento, o único objeto implementado no one-pass-vault é o `item`
    3. Fazer o parse da resposta. A classe **OnePassParserFactory** é responsável por trazer o `Parser` especifico para o objeto requisitado, pegando os campos necessários da `response` e organizando dentro de um novo dicionário.
    4. Transformar o novo dicionário gerado pelo Parser em variáveis ambientes. Tem uma função especifica para isso, presente no `__init__.py` chamada `spawn_parsed_response`. 
    5. Executar o `cmd`. No caso do exemplo é o `docker-compose up -d`.
 
As variáveis ambiente lançadas durante esse execução serão:
* app_cred_1_user=<valor1>
* app_cred_2_password=<valor2>
* db_cred_1_host=<valor3>
* db_cred_2_port=<valor4>
* etc

Dentro do OnePassword, um `item` pode ter vários *tipos*, sendo eles *dados de acesso, banco de dados, servidor, conta de email*, etc. Por hora, o Parser de Item (OnePassItemParser) implementa somente `dados de acesso` (ApplicationItem) e `banco de dados` (DatabaseItem). Cada uma dessas classes terão campos específicos que serão pesquisados dentro da *response* para gerar um novo *dicionário* que vai ser importante para criar as variáveis ambiente. O formato padrão das variáveis ambientes sempre vai ser: `<nome_da_credencial>_<campo_da_credencial>=<valor>`.
 
