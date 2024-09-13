from pydantic import BaseModel


class VPCMetrics(BaseModel):
    vpc_id: str
    num_subnets: int
    num_instances: int
    num_security_groups: int
