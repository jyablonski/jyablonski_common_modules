import boto3
from moto import mock_aws
import pytest

from jyablonski_common_modules.aws import get_secret_value


@mock_aws
def test_get_secret_value_success():
    client = boto3.client("secretsmanager", region_name="us-east-1")
    secret_name = "bababooyee"
    secret_value = "mama mia"

    client.create_secret(Name=secret_name, SecretString=secret_value)

    result = get_secret_value(client=client, secret=secret_name)

    assert result == secret_value


@mock_aws
def test_get_secret_value_fail():
    client = boto3.client("secretsmanager", region_name="us-east-1")

    secret_name = "bababooyee2"
    fake_secret_name = "this doesn't exist hoe"
    secret_value = "mama mia"

    client.create_secret(Name=secret_name, SecretString=secret_value)

    with pytest.raises(TypeError):
        secret = get_secret_value(client=client, secret=fake_secret_name)
