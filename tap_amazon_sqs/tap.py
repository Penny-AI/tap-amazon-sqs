"""amazon-sqs tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_amazon_sqs import streams


class Tapamazonsqs(Tap):
    """amazon-sqs tap class."""

    name = "tap-amazon-sqs"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "queue_url",
            th.StringType,
            required=True,
            secret=False,  
            description="URL of the SQS Queue",
        ),
        th.Property(
            "region",
            th.StringType,
            required=True,
            description="AWS Region of the SQS Queue",
            
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.mysample.com",
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.amazonsqsStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.GroupsStream(self),
            streams.UsersStream(self),
        ]


if __name__ == "__main__":
    Tapamazon-sqs.cli()
