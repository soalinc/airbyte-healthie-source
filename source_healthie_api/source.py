#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
import json
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator, NoAuth

"""
TODO: Most comments in this class are instructive and should be deleted after the source is implemented.

This file provides a stubbed example of how to use the Airbyte CDK to develop both a source connector which supports full refresh or and an
incremental syncs from an HTTP API.

The various TODOs are both implementation hints and steps - fulfilling all the TODOs should be sufficient to implement one basic and one incremental
stream from a source. This pattern is the same one used by Airbyte internally to implement connectors.

The approach here is not authoritative, and devs are free to use their own judgement.

There are additional required TODOs in the files within the integration_tests folder and the spec.yaml file.
"""


# Basic full refresh stream
class HealthieApiStream(HttpStream, ABC):
    """
    TODO remove this comment

    This class represents a stream output by the connector.
    This is an abstract base class meant to contain all the common functionality at the API level e.g: the API base URL, pagination strategy,
    parsing responses etc..

    Each stream should extend this class (or another abstract subclass of it) to specify behavior unique to that stream.

    Typically for REST APIs each stream corresponds to a resource in the API. For example if the API
    contains the endpoints
        - GET v1/customers
        - GET v1/employees

    then you should have three classes:
    `class HealthieApiStream(HttpStream, ABC)` which is the current class
    `class Customers(HealthieApiStream)` contains behavior to pull data for customers using v1/customers
    `class Employees(HealthieApiStream)` contains behavior to pull data for employees using v1/employees

    If some streams implement incremental sync, it is typical to create another class
    `class IncrementalHealthieApiStream((HealthieApiStream), ABC)` then have concrete stream implementations extend it. An example
    is provided below.

    See the reference docs for the full list of configurable options.
    """
    url_base = "https://staging-api.gethealthie.com/graphql"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        """
        TODO: Override this method to define a pagination strategy. If you will not be using pagination, no action is required - just return None.

        This method should return a Mapping (e.g: dict) containing whatever information required to make paginated requests. This dict is passed
        to most other methods in this class to help you form headers, request bodies, query params, etc..

        For example, if the API accepts a 'page' parameter to determine which page of the result to return, and a response from the API contains a
        'page' number, then this method should probably return a dict {'page': response.json()['page'] + 1} to increment the page count by 1.
        The request_params method should then read the input next_page_token and set the 'page' param to next_page_token['page'].

        :param response: the most recent response from the API
        :return If there is another page in the result, a mapping (e.g: dict) containing information needed to query the next page in the response.
                If there are no more pages in the result, return None.
        """
        return None
    
    @property
    def http_method(self) -> str:
        """
        Override if needed. See get_request_data/get_request_json if using POST/PUT/PATCH.
        """
        return "POST"


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        """
        TODO: Override this method to define any query parameters to be set. Remove this method if you don't need to define request params.
        Usually contains common params e.g. pagination size etc.
        """
        return None
    
    def request_headers(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Mapping[str, Any]:
        return {
            'AuthorizationSource': 'API',
            'Content-Type': 'application/json',    
        }

    # def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
    #     """
    #     TODO: Override this method to define how a response is parsed.
    #     :return an iterable containing each record in the response
    #     """
    #     yield [response.json()]


class Users(HealthieApiStream):
    # primary_key = "id"
    primary_key = None


    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return ""
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        users = response.json().get("data").get("users")
        return users

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:
        
        graph_ql_query = """
            query users(
                $offset: Int,
                $keywords: String,
                $sort_by: String,
                $active_status: String,
                $group_id: String,
                $show_all_by_default: Boolean,
                $should_paginate: Boolean,
                $provider_id: String,
                $conversation_id: ID,
                $limited_to_provider: Boolean,
                ) {
                usersCount(
                    keywords: $keywords,
                    active_status:$active_status,
                    group_id: $group_id,
                    conversation_id: $conversation_id,
                    provider_id: $provider_id,
                    limited_to_provider: $limited_to_provider
                )
                users(
                    offset: $offset,
                    keywords: $keywords,
                    sort_by: $sort_by,
                    active_status: $active_status,
                    group_id: $group_id,
                    conversation_id: $conversation_id,
                    show_all_by_default: $show_all_by_default,
                    should_paginate: $should_paginate,
                    provider_id: $provider_id,
                    limited_to_provider: $limited_to_provider
                ) {
                    id
                }
            }
        """

        return {"query": graph_ql_query, "variables": {}}

# Source
class SourceHealthieApi(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        """
        TODO: Implement a connection check to validate that the user-provided config can be used to connect to the underlying API

        See https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-stripe/source_stripe/source.py#L232
        for an example.

        :param config:  the user-input config object conforming to the connector's spec.yaml
        :param logger:  logger object
        :return Tuple[bool, any]: (True, None) if the input config can be used to connect to the API successfully, (False, error) otherwise.
        """
        try:
            graph_ql_query = """
                query currentUser {
                    currentUser {
                        id
                    }
                }
            """


            data = {"query": graph_ql_query, "variables": {}}
            api_key = config.get("apikey")
            headers = {
                "Authorization": f"Basic {api_key}",
                "Content-Type": "application/json",
                "AuthorizationSource": "API"
            }

            response = requests.post(url="https://staging-api.gethealthie.com/graphql", json=data, headers=headers)
            data = response.json()
            logger.info(f"Data: {data}")
            if data.get("errors"):
                logger.error(f"Request was not successfull")
                return False, data.get("errors")
            
            return True, None
        
        except Exception as e:
            logger.info(f"Request was not successfull")
            return False, "Unable to connect to the API with the provided credentials"

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        TODO: Replace the streams below with your own streams.

        :param config: A Mapping of the user input configuration as defined in the connector spec.
        """
        auth = TokenAuthenticator(token=config.get("apikey"), auth_method="Basic")
        # auth = NoAuth()
        return [Users(authenticator=auth)]
