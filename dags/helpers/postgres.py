from datetime import datetime
import tempfile
from psycopg2 import sql
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json, execute_values, register_json
from airflow.hooks.postgres_hook import PostgresHook


class Postgres:
    """
        Postgres
    """

    def __init__(self, conn_id):
        self.hook = PostgresHook(postgres_conn_id=conn_id)
        self.conn = self.hook.get_conn()

    def exec(self, query: str, query_name: str):
        """
            Executa query e printa log com:
                - Time elapsed tempo de execução
                - mensagens de retorno do postgres
                - notificações do postgres
        """
        start_time = datetime.now()
        self.conn.autocommit = False
        self.conn.notices = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

        time_elapsed = datetime.now() - start_time

        str_notice = ''
        if cursor.statusmessage != 'DO':
            str_notice = cursor.statusmessage

        for notice in self.conn.notices:
            str_notice += notice.strip().rstrip().replace('NOTICE:  ', '')

        msg = f'Time elapsed {format(time_elapsed)}   {query_name}'
        msg = msg + ((120 - len(msg)) * ' ') + str_notice
        print(msg)

    def exec_no_transaction(self, query: str, query_name: str):
        """
            Executa query sem transação
        """
        start_time = datetime.now()
        self.conn.notices = []
        self.conn.autocommit = True
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.autocommit = False

        time_elapsed = datetime.now() - start_time

        str_notice = ''

        if cursor.statusmessage != 'DO':
            str_notice = cursor.statusmessage

        for notice in self.conn.notices:
            str_notice += notice.strip().rstrip().replace('NOTICE:  ', '')

        msg = f'Time elapsed {format(time_elapsed)}   {query_name}'
        msg = msg + ((120 - len(msg)) * ' ') + str_notice
        print(msg)

    def exec_return(self, query: str, query_name: str):
        """
            Executa query e printa log com:
                - Time elapsed tempo de execução
                - mensagens de retorno do postgres
                - notificações do postgres
        """
        start_time = datetime.now()

        self.conn.autocommit = False
        self.conn.notices = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()
        self.conn.commit()

        time_elapsed = datetime.now() - start_time

        str_notice = ''
        if cursor.statusmessage != 'DO':
            str_notice = cursor.statusmessage

        for notice in self.conn.notices:
            str_notice += notice.strip().rstrip().replace('NOTICE:  ', '')

        msg = f'Time elapsed {format(time_elapsed)}   {query_name}'
        msg = msg + ((120 - len(msg)) * ' ') + str_notice
        print(msg)
        return tables

    def exec_insert(self, data: list, table: str, truncate: bool = False):
        """
            Insere lista em tabela
        """

        register_adapter(dict, Json)  # avoid parse to python dictionary (keeps postgres json)
        register_json(oid=3802, array_oid=3807, globally=True)  # avoid parse to python dictionary (keeps postgres json)

        print(f'Inserting in: {table}')

        self.conn.autocommit = False
        dest_cursor = self.conn.cursor()

        if truncate:
            dest_cursor.execute(f'TRUNCATE TABLE {table};')

        inserted = 0
        while True:
            lines = data[0:1000]
            del data[0:1000]
            inserted += len(lines)
            if not lines:
                break
            try:
                execute_values(
                    dest_cursor,
                    f'INSERT INTO {table} VALUES %s;'.format(table=sql.Identifier(table)),
                    lines,
                )
            except Exception as error:
                print(f'Line - {lines}')
                raise Exception(error) from error

            print(f'Inserted: {inserted}')
        self.conn.commit()

    def dump_to_dest(self, src_conn_id: str, t_schema: str, t_name: str):
        """
            Carrega dump da origem para o destino
        """
        # avoid parse to python dictionary (keeps postgres json)
        register_adapter(dict, Json)
        register_json(oid=3802, array_oid=3807, globally=True)

        src_hook = PostgresHook(postgres_conn_id=src_conn_id)
        src_conn = src_hook.get_conn()
        src_cursor = src_conn.cursor()
        src_cursor.execute(f'select count(0) from {t_name};')
        qtd = src_cursor.fetchone()[0]

        dest_cursor = self.conn.cursor()
        dest_cursor.execute(f'TRUNCATE TABLE {t_schema}.{t_name};')
        self.conn.commit()

        if qtd > 0:
            with tempfile.NamedTemporaryFile() as temp_file:
                print('Gerando dump tabela:', t_name, 'linhas:', qtd)
                src_hook.bulk_dump(t_name, temp_file.name)
                print('Carregando dump tabela:', f'{t_schema}.{t_name}', 'linhas:', qtd)
                self.hook.bulk_load(f'{t_schema}.{t_name}', temp_file.name)
        else:
            print('Não foi gerado dump tabela:', t_name, 'pois possui 0 registros')
