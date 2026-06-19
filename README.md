 Envio de Mensagens WhatsApp com Supabase + Z-API
Projeto Python que lê contatos armazenados no Supabase e envia uma mensagem personalizada via WhatsApp utilizando a Z-API.
- Conexão com o Supabase para buscar contatos (nome e telefone)
- Envio de mensagem: `"Olá {nome_contato}, tudo bem com você?"`
- Tratamento de erros e logging
- Testes unitários com mocks (TDD: Red → Green → Refactor)
- Configuração de qualidade com Black, Flake8 e pre-commit

Stack
- Python 3.10+
- Poetry (gerenciamento de dependências)
- Supabase (PostgreSQL na nuvem)
- Z-API (API de WhatsApp)
- Pytest, Black, Flake8, pre-commit

## Como configurar

Clone o repositório e instale as dependências:
   poetry install
Configure as variáveis de ambiente criando um arquivo .env

  SUPABASE_URL=
  
  SUPABASE_KEY=
  
  ZAPI_INSTANCE_ID=
  
  ZAPI_TOKEN=
  
Execute o pre-commit:
  poetry run pre-commit install
Testes unitários :
  poetry run pytest tests/ -v


Melhorias futuras
  Alembic – versionamento de migrações do banco de dados
  Supabase Vault – criptografia de colunas sensíveis (ex: telefone)
  Criptografia de dados via AES (Fernet) a nível de aplicação
  Agendamento automático de envios (CRON / APScheduler)
  Integração com outras APIs de WhatsApp

