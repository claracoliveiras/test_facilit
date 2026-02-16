# Relatorio do Projeto

## Etapa 1: Configuração da infraestrutura do projeto

1. Inicializei o repositorio no github para versionamento com arquivos base como .env, .gitignore e README.md.
2. Utilizei o agente Codex para definir a estrutura inicial de um arquivo docker-compose.yml para as instancias do banco de dados Postgresql e n8n.
3. Movi as informacoes sensiveis do docker-compose para o arquivo .env, afim de minimizar o acesso as informacoes.
4. Gerei um novo arquivo para relatorio chamado relatorio.md, onde vou atualizar as informacoes sobre o passo-a-passo da criacao do aplicativo.
5. Pedi ao Codex que gerasse um CRUD básico para a API, utilizando postgres e SQLAlchemy e entregando um esquema básico para as propriedades da tabela, especificando o modelo de pastas que eu gostaria que fosse utilizado.
6. Pedi ao Codex que adicionasse a inicialização da API no arquivo docker-compose.yml e que ele gerasse um arquivo Docker. Também pedi para que ele adicionasse um check para que a data final do evento fosse sempre maior do que a inicial, e também que ele incluisse error handling nos chamados. 
7. Iniciei a configuração dos fluxos do N8N, criando primeiro as credenciais OAuth para o aplicativo no google e incluindo as credenciais necessárias.
8. Ao iniciar a configuração do fluxo, identifiquei a necessidade de uma distinção maior entre as propriedades (por conta da diferença entre os eventos do RH e do Marketing), onde pedi ao Codex que adicionasse a propriedade de alcance no código da API. Também pedi que adicionasse a propriedade de "departamento" para que possamos filtrar melhor no futuro.


### Dificuldades

1. Temos eventos trimestrais e semestrais, mas como determinar até quando esses eventos irão acontecer/quantos adicionar no banco de dados?