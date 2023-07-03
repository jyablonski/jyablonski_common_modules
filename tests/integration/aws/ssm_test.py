import boto3
from moto import mock_ssm

from jyablonski_common_modules.aws import get_ssm_parameter


@mock_ssm
def test_get_ssm_parameter():
    client = boto3.client("ssm", region_name="us-east-1")
    parameter_name = "jacobs_test_parameter"
    parameter_value = "my super secret value"

    client.put_parameter(
        Name=parameter_name,
        Description="A test parameter",
        Value=parameter_value,
        Type="String",
    )

    parameter = get_ssm_parameter(client=client, parameter_name="jacobs_test_parameter")

    assert parameter == parameter_value
