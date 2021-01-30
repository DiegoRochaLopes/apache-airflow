from dags.helpers.postgres import Postgres
from dags.dag01.querys.scripts import Scripts


def querys_no_return():
    """ Executa querys sem retorno """
    # esta será a ordem que a carga será executada sequencialmente
    querys = [
        Scripts().select_count(),
        Scripts().select_limit(),
    ]

    conn = Postgres('db_destino')

    for query in querys:
        conn.exec(query[0], query[1])


def querys_with_return():
    """ Executa querys com retorno """
    # esta será a ordem que a carga será executada sequencialmente
    querys = [
        Scripts().select_count(),
        Scripts().select_limit(),
    ]

    conn = Postgres('db_destino')

    for query in querys:
        print(conn.exec_return(query[0], query[1]))


def load_dump():
    """ Dump da origem para destino """

    conn = Postgres('db_destino')
    conn.dump_to_dest('db_origem', 'public', 'tb1')