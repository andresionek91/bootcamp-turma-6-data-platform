from aws_cdk import core

from bootcamp_turma_6_data_platform.airflow_stack.stack import AirflowStack
from bootcamp_turma_6_data_platform.athena.stack import AthenaStack
from bootcamp_turma_6_data_platform.common_stack import CommonStack
from bootcamp_turma_6_data_platform.data_lake.stack import DataLakeStack
from bootcamp_turma_6_data_platform.databricks.stack import DatabricksStack
from bootcamp_turma_6_data_platform.dms.stack import DmsStack
from bootcamp_turma_6_data_platform.glue_catalog.stack import GlueCatalogStack
from bootcamp_turma_6_data_platform.kinesis.stack import KinesisStack
from bootcamp_turma_6_data_platform.redshift.stack import RedshiftStack

app = core.App()
data_lake_stack = DataLakeStack(app)
common_stack = CommonStack(app)
kinesis_stack = KinesisStack(
    app, data_lake_raw_bucket=data_lake_stack.data_lake_raw_bucket
)
dms_stack = DmsStack(
    app,
    common_stack=common_stack,
    data_lake_raw_bucket=data_lake_stack.data_lake_raw_bucket,
)
athena_stack = AthenaStack(app)
glue_catalog_stack = GlueCatalogStack(
    app,
    raw_data_lake_bucket=data_lake_stack.data_lake_raw_bucket,
    processed_data_lake_bucket=data_lake_stack.data_lake_raw_processed,
)
databricks_stack = DatabricksStack(app)
airflow_stack = AirflowStack(
    app,
    common_stack=common_stack,
    data_lake_raw_bucket=data_lake_stack.data_lake_raw_bucket,
)
redshift_stack = RedshiftStack(
    app,
    common_stack=common_stack,
    data_lake_raw=data_lake_stack.data_lake_raw_bucket,
    data_lake_processed=data_lake_stack.data_lake_raw_processed,
)

app.synth()
