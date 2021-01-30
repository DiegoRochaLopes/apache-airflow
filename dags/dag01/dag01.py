"""## dag01
Objetivo: teste de taskgroup.

"""

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

from dags.dag01.model import load_dump, querys_no_return, querys_with_return

with DAG(
    dag_id="dag01",
    start_date=days_ago(1),
    tags=["test"]
) as dag:

    start = PythonOperator(
        task_id="start",
        trigger_rule='all_success',
        python_callable=querys_with_return)

    with TaskGroup("section_1", tooltip="pipeline xpto") as section_1:
        task_load_dump = PythonOperator(
            task_id="task_load_dump",
            trigger_rule='all_success',
            python_callable=load_dump)

        task_querys_with_return = PythonOperator(
            task_id="task_querys_with_return",
            trigger_rule='all_success',
            python_callable=querys_with_return)

        task_querys_no_return = PythonOperator(
            task_id="task_querys_no_return",
            trigger_rule='all_success',
            python_callable=querys_no_return)

        task_load_dump >> [task_querys_with_return, task_querys_no_return]

        with TaskGroup("inner_section_2", tooltip="Tasks for inner_section2") as inner_section_2:
            task_2 = BashOperator(task_id="task_2", bash_command='echo 2')
            task_3 = DummyOperator(task_id="task_3")
            task_4 = DummyOperator(task_id="task_4")

            [task_2, task_3] >> task_4

    end = DummyOperator(task_id='end')

    # docs
    dag.doc_md = __doc__
    for task in dag.tasks:
        str_doc = 'exemplo'
        if task.task_type == 'PythonOperator':
            str_doc = task.python_callable.__doc__
        dag.doc_md += f""" - __{task.task_id}:__ {str_doc} \n"""

    start >> section_1 >> end
