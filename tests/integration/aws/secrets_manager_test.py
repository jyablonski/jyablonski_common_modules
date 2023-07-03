import boto3
from moto import mock_secretsmanager
from jyablonski_common_modules.aws import get_secret_value


@mock_secretsmanager
def test_get_secret_value():
    client = boto3.client("secretsmanager", region_name="us-east-1")
    secret_name = "bababooyee"
    secret_value = "mama mia"

    client.create_secret(Name=secret_name, SecretString=secret_value)

    result = get_secret_value(client=client, secret=secret_name)

    assert result == secret_value
