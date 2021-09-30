from aws_cdk import core

from airflow.stack import AirflowStack
from athena.stack import AthenaStack
from common_stack import CommonStack
from data_lake.stack import DataLakeStack
from databricks.stack import DatabricksStack
from dms.stack import DmsStack
from glue_catalog.stack import GlueCatalogStack
from kinesis.stack import KinesisStack

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

app.synth()
