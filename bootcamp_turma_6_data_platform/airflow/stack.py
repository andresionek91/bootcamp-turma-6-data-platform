from aws_cdk import core
from aws_cdk import (
    aws_mwaa as mwaa,
    aws_logs as logs,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_deployment as s3deploy,
)

from common_stack import CommonStack
from bootcamp_turma_6_data_platform.data_lake.base import BaseDataLakeBucket
import os
from zipfile import ZipFile


class AirflowStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        common_stack: CommonStack,
        data_lake_raw_bucket: BaseDataLakeBucket,
        **kwargs,
    ) -> None:
        self.deploy_env = os.environ["ENVIRONMENT"]
        self.common_stack = common_stack
        self.data_lake_raw_bucket = data_lake_raw_bucket
        super().__init__(scope, id=f"{self.deploy_env}-airflow-stack", **kwargs)

        self.security_group = ec2.SecurityGroup(
            self,
            f"airflow-{self.deploy_env}-sg",
            vpc=self.common_stack.custom_vpc,
            allow_all_outbound=True,
            security_group_name=f"airflow-{self.deploy_env}-sg",
        )

        self.security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"), connection=ec2.Port.tcp(5432)
        )

        self.bucket = s3.Bucket(
            self,
            id=f"s3-{self.deploy_env}-belisquito-airflow",
            bucket_name=f"s3-{self.deploy_env}-belisquito-turma6-airflow",
            removal_policy=core.RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        self.execution_role = iam.Role(
            self,
            id=f"iam-{self.deploy_env}-data-lake-raw-airflow-role",
            description="Role to allow Airflow to access resources",
            assumed_by=iam.ServicePrincipal("airflow.amazonaws.com"),
        )
        self.execution_role.assume_role_policy.add_statements(
            iam.PolicyStatement(
                principals=[iam.ServicePrincipal("airflow-env.amazonaws.com")],
                actions=["sts:AssumeRole"],
            )
        )

        self.execution_policy = iam.Policy(
            self,
            id=f"iam-{self.deploy_env}-airflow-execution-policy",
            policy_name=f"iam-{self.deploy_env}-airflow-execution-policy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "s3:PutObjectTagging",
                        "s3:PutObjectAcl",
                        "s3:DeleteObject",
                        "s3:ListBucket",
                        "s3:GetObject",
                        "s3:PutObject",
                    ],
                    resources=[
                        self.data_lake_raw_bucket.bucket_arn,
                        f"{self.data_lake_raw_bucket.bucket_arn}/*",
                    ],
                ),
            ],
        )

        self.execution_role.attach_inline_policy(self.execution_policy)
        self.execution_role.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(
            self,
            id="MWAA-managed-policy",
            managed_policy_arn="arn:aws:iam::aws:policy/aws-service-role/AmazonMWAAServiceRolePolicy"))

        with ZipFile("bootcamp_turma_6_data_platform/airflow/resources.zip", "w") as zipObj2:
            zipObj2.write(
                "bootcamp_turma_6_data_platform/airflow/requirements.txt", arcname="requirements.txt"
            )
            for file in os.listdir("bootcamp_turma_6_data_platform/airflow/dags"):
                zipObj2.write(
                    f"bootcamp_turma_6_data_platform/airflow/dags/{file}", arcname=f"dags/{file}"
                )

        self.dag_upload = s3deploy.BucketDeployment(
            self,
            id=f"{self.deploy_env}-belisquito-airflow-content",
            destination_bucket=self.bucket,
            sources=[s3deploy.Source.asset("bootcamp_turma_6_data_platform/airflow/resources.zip")],
        )

        self.airflow = mwaa.CfnEnvironment(
            self,
            id=f"{self.deploy_env}-airflow",
            name=f"{self.deploy_env}-airflow",
            airflow_version="2.0.2",
            dag_s3_path="dags",
            environment_class="mw1.small",
            execution_role_arn=self.execution_role.role_arn,
            logging_configuration=mwaa.CfnEnvironment.LoggingConfigurationProperty(
                dag_processing_logs=mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(
                    enabled=True,
                    log_level="INFO",
                ),
                scheduler_logs=mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(
                    enabled=True,
                    log_level="INFO",
                ),
                task_logs=mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(
                    enabled=True,
                    log_level="INFO",
                ),
                webserver_logs=mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(
                    enabled=True,
                    log_level="INFO",
                ),
                worker_logs=mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(
                    enabled=True,
                    log_level="INFO",
                ),
            ),
            max_workers=2,
            min_workers=1,
            network_configuration=mwaa.CfnEnvironment.NetworkConfigurationProperty(
                security_group_ids=[self.security_group.security_group_id],
                subnet_ids=[
                    subnet.subnet_id
                    for subnet in self.common_stack.custom_vpc.private_subnets
                ],
            ),
            webserver_access_mode="PUBLIC_ONLY",
            weekly_maintenance_window_start="WED:01:00",
            source_bucket_arn=self.bucket.bucket_arn,
            requirements_s3_path="requirements.txt",
            schedulers=2
        )

        self.airflow.node.add_dependency(self.execution_role)
        self.airflow.node.add_dependency(self.security_group)
        self.airflow.node.add_dependency(self.bucket)
        self.airflow.node.add_dependency(self.dag_upload)
