from aws_cdk import core

from data_lake.stack import DataLakeStack

app = core.App()
DataLakeStack(app)
app.synth()
