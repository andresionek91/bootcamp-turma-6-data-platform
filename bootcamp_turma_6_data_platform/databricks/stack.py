import os

from aws_cdk import core
from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
)


class DatabricksStack(core.Stack):
    """
    Docs followed to create permissions:
    https://docs.databricks.com/administration-guide/account-settings/aws-accounts.html

    https://docs.databricks.com/administration-guide/cloud-configurations/aws/instance-profiles.html

    https://docs.databricks.com/spark/latest/structured-streaming/auto-loader.html

    https://docs.databricks.com/data/metastores/aws-glue-metastore.html
    + spark.databricks.hive.metastore.glueCatalog enabled

    https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-data-catalog-hive.html
    """

    def __init__(self, scope: core.Construct, **kwargs) -> None:
        self.deploy_env = os.environ["ENVIRONMENT"]
        super().__init__(scope, id=f"{self.deploy_env}-databricks-stack", **kwargs)

        access_role = iam.Role(
            self,
            id=f"iam-{self.deploy_env}-databricks-data-lake-access-role",
            assumed_by=iam.ServicePrincipal("ec2"),
            description=f"Allows databricks access to data lake",
        )

        access_policy = iam.Policy(
            self,
            id=f"iam-{self.deploy_env}-databricks-data-lake-access-policy",
            policy_name=f"iam-{self.deploy_env}-databricks-data-lake-access-policy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "s3:ListBucket",
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:DeleteObject",
                        "s3:PutObjectAcl",
                    ],
                    resources=[
                        f"arn:aws:s3:::s3-belisco-turma-6-{self.deploy_env}-data-lake-*",
                        f"arn:aws:s3:::s3-belisco-turma-6-{self.deploy_env}-data-lake-*/*",
                    ],
                ),
                iam.PolicyStatement(
                    actions=[
                        "glue:BatchCreatePartition",
                        "glue:BatchDeletePartition",
                        "glue:BatchGetPartition",
                        "glue:CreateDatabase",
                        "glue:CreateTable",
                        "glue:CreateUserDefinedFunction",
                        "glue:DeleteDatabase",
                        "glue:DeletePartition",
                        "glue:DeleteTable",
                        "glue:DeleteUserDefinedFunction",
                        "glue:GetDatabase",
                        "glue:GetDatabases",
                        "glue:GetPartition",
                        "glue:GetPartitions",
                        "glue:GetTable",
                        "glue:GetTables",
                        "glue:GetUserDefinedFunction",
                        "glue:GetUserDefinedFunctions",
                        "glue:UpdateDatabase",
                        "glue:UpdatePartition",
                        "glue:UpdateTable",
                        "glue:UpdateUserDefinedFunction",
                    ],
                    resources=["*"],
                ),
            ],
        )
        access_role.attach_inline_policy(access_policy)

        iam.CfnInstanceProfile(
            self,
            id=f"iam-{self.deploy_env}-databricks-data-lake-access-instance-profile",
            instance_profile_name=f"iam-{self.deploy_env}-databricks-data-lake-access-instance-profile",
            roles=[access_role.role_name],
        )

        cross_account_role = iam.Role.from_role_arn(
            scope=self,
            id="databricks-cross-account",
            role_arn="arn:aws:iam::480800208880:role/db-a205e963818fcee8fb1136385513e11a-iam-role",
        )

        cross_account_policy_data_access = iam.Policy(
            self,
            id=f"iam-{self.deploy_env}-databricks-cross-account-policy-data-access",
            policy_name=f"iam-{self.deploy_env}-databricks-cross-account-policy-data-access",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "iam:PassRole",
                    ],
                    resources=[access_role.role_arn],
                )
            ],
        )

        cross_account_role.attach_inline_policy(cross_account_policy_data_access)
