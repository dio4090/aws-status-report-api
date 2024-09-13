import boto3
from app.models import VPCMetrics
from app.main import app

class AWSService:
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def get_vpc_metrics(self, vpc_id: str) -> VPCMetrics:
        vpc = self.ec2.describe_vpcs(VpcIds=[vpc_id])['Vpcs'][0]
        subnets = self.ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets']
        instances = self.ec2.describe_instances(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Reservations']
        security_groups = self.ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['SecurityGroups']

        return VPCMetrics(
            vpc_id=vpc_id,
            num_subnets=len(subnets),
            num_instances=sum(len(reservation['Instances']) for reservation in instances),
            num_security_groups=len(security_groups)
        )

aws_service = AWSService()

@app.get("/vpc-metrics/{vpc_id}", response_model=VPCMetrics)
async def get_vpc_metrics(vpc_id: str):
    return aws_service.get_vpc_metrics(vpc_id)
