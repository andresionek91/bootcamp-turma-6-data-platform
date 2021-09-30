import os

from aws_cdk import core

from bootcamp_turma_6_data_platform.athena.base import (
    BaseAthenaBucket,
    BaseAthenaWorkgroup,
)


class AthenaStack(core.Stack):
    def __init__(self, scope: core.Construct, **kwargs) -> None:
        self.deploy_env = os.environ["ENVIRONMENT"]
        super().__init__(scope, id=f"{self.deploy_env}-athena", **kwargs)

        self.athena_bucket = BaseAthenaBucket(
            self,
        )

        self.athena_workgroup = BaseAthenaWorkgroup(
            self, athena_bucket=self.athena_bucket, gb_scanned_cutoff_per_query=1
        )
