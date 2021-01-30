# Airflow 2.0 exemplo

Mostra como criar bancos de dados ao executar containers no docker.
Ao executar serão criados os bancos:
- db_origem
- db_destino

Os dois bancos contem a tabela `tb1`.

Contem uma dag com exemplo de `TaskGroup`, dump load e auto documentação.


## Execução

OS X & Linux:

```sh
docker-compose up -d
```


## Acesso

http://localhost:8080

user: dev

pass: dev