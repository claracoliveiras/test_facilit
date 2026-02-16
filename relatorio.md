# Relatório

## Instruções de configuração

1. Ao baixar os conteúdos do repositório, na pasta principal, criar um arquivo `.env` com as informações especificadas no arquivo `README.md`. Essas informações dizem respeito as configurações, principalmente, do banco de dados que vai ser criado no próximo passo, além de uma chave de encriptação do n8n. Essa chave serve para o n8n utilizar na proteção dos dados importantes que forem registrados nele, como contas e senhas.
2. Após criar o arquivo, ainda na pasta principal, deve-se executar o seguinte comando no terminal, que vai gerar os containers do **n8n**, **postgres** e da **API** em si:
```bash
docker compose up --build -d
```
3. Ao gerar os containers e assumindo que mudanças não foram feitas no código, podemos acessar a instância do n8n por este link:
```bash
http://localhost:5678/
```
4. Acessando o n8n, deve-se criar uma conta para acessar os fluxos, e logo em seguida, importar os dois fluxos que se encontram na pasta "/n8n/". A importação é feita criando um novo fluxo e selecionando os três pontinhos no canto superior direito, onde se encontra a opção `Import from file`.
5. O primeiro fluxo a ser configurado é o fluxo `Migração de dados`, onde devemos configurar as credenciais OAuth que vai nos permitir o acesso as planilhas do google.
6. Após criar a credencial, devemos abrir os nódulos de planilha (notáveis pelo ícone idêntico ao do google) e verificar se eles possuem as credenciais que acabamos de criar na opção `Credential to connect with`.
7. Depois disso, vamos abrir o fluxo `Consulta com IA`, onde devemos inserir nossa chave do Open API no nódulo `Model`.
8. Nesse passo, ative também o fluxo para que possamos iniciar os testes com o nosso chatbot.
9. Selecionando o primeiro nódulo do nosso fluxo de `Consulta com IA`, podemos visualizar o link do nosso webhook, que é por onde nossas mensagens entram no fluxo.
```bash
http://localhost:5678/webhook/consulta-com-ia
```
10. Nesse link, vamos adicionar dois parâmetros, que são informações que vamos enviar pela URL do webhook:
```bash
http://localhost:5678/webhook/consulta-com-ia?mensagem=Insira aqui a mensagem que você gostaria de inserir&chatid=Esse é um número relativo ao ID do chat
```
11. Em alguns segundos, a resposta do bot será exibida na tela. Para continuar a conversa, basta utilizar o mesmo número de chatid que foi utilizado para enviar a mensagem anterior.

## 1. Infraestrutura
O projeto foi iniciado a partir da construção do arquivo `docker-compose.yml`, que incluia inicialmente as instâncias para o n8n e o banco de dados Postgres. O Codex foi utilizado para a criação desse arquivo.

## 2. API
Em seguida, analisei as planilhas para determinar a estrutura e propriedades necessárias no banco de dados, passando a relação para o Codex para que ele gerasse um CRUD básico para mim baseado nessas informações, utilizando SQLAlchemy para as operações com o banco de dados que já havia sido criado anteriormente, visto que as informações de conexão já estavam no .env do projeto. Após as configurações iniciais, pedi também que ele adicionasse tratamento de erros nas funções e fizesse modificações na estrutura para se aproximar mais de um padrão MVC.
Na estruturação da API, tive uma pequena dificuldade em relação a necessidade de uma maior distinção entre periodicidades (eventos trimestrais e semestrais), principalmente relativo a quantidade e a necessidade de repetições no banco de dados. Por esse motivo, criei apenas uma propriedade que é preenchida caso a informação esteja presente.

## 3. n8n (Fluxo de migração de dados)
Para o fluxo de migração de dados, iniciei criando os nódulos para ler os dados das três planilhas fornecidas e criei a credencial OAuth necessária no n8n. Para esse passo:
- Criei uma aplicação no console do google e utilizei as informações fornecidas (client id e client secret) para conectar a credencial;
- No console, ativei as APIs do Google Sheets e Google Drive;
- Nas configurações da aplicação, adicionei os escopos para o Google Sheets e o Google Drive.

Após isso, retomei a configuração no n8n, onde adicionei uma condição para que eventos só sejam criados caso o nome esteja preenchido, em caso de linhas vazias na planilha.

Utilizei o Codex novamente para criar um nódulo de código para tratar e retornar as datas formatadas para que sejam utilizadas na API, e em seguida mais uma vez para um nódulo que identifica se existe menção de periodicidade na data (Semestral, trimestral).

Para finalizar, enviei os dados tratados para a API utilizando um post.

## 4. n8n (Fluxo de IA)
No fluxo de IA, organizei a automação para receber mensagens por webhook e responder no mesmo request.

Dentro do `AI Agent`, conectei os seguintes nós:
- `OpenAI Chat Model` para interpretação das mensagens,
- o `Simple Memory` para manter o contexto por `chatid`
- Três tools HTTP para operar no banco pela API: leitura (`Ler eventos do banco`), criação (`Inserir evento no banco`) e atualização (`Editar evento no banco`)

Utilizei o ChatGPT 5.2 para gerar um Prompt para o agente, adicionando ele no nódulo `AI Agent`. No prompt, especifiquei que o agente é responsável por gerenciar informações de Eventos da Facilit e as regras de linguagem. Solicitei que negasse educadamente quando perguntado sobre informações fora do escopo. Dentro das tools, também escrevi descrições para cada propriedade e tool, especificando quando e como devem ser utilizadas. 

Com esse desenho, o agente consegue consultar os eventos existentes, decidir quando criar um novo registro e também editar um evento já cadastrado, sempre retornando a resposta final pelo `Respond to Webhook`.
