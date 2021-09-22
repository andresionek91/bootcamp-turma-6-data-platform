from aws_cdk import core

from common_stack import CommonStack
from data_lake.stack import DataLakeStack
from dms.stack import DmsStack
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
app.synth()
