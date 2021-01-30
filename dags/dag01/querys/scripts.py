from dags.helpers.utils import sql_script_from_file


class Scripts():
    """ Querys que serão utilizadas no processo de carga
    """
    @sql_script_from_file
    def select_count(self): """ Select count na `tb1` """

    @sql_script_from_file
    def select_limit(self): """ `Select * from tb1` com limit 100 """
