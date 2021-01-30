from pathlib import Path


def sql_script_from_file(func):
    """ Retornará o script sql do arquivo do nome da função
    """
    def get_sql_script_from_file(self, snapshots: int = None):
        dummy = self
        script_name = func.__name__ + '.sql'
        file_sql = Path(func.__code__.co_filename).with_name(script_name)
        script_name = file_sql.relative_to(file_sql.parent.parent.parent)

        with file_sql.open('r') as tmp:
            script_sql = tmp.read()

        if snapshots is not None:
            script_sql = script_sql.replace('limit 1', 'limit ' + str(snapshots))

        return script_sql, script_name
    return get_sql_script_from_file
