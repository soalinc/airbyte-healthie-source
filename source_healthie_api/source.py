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

from .graph_ql_queries import (
    users_query,
    appointment_types_query,
    appointments_query,
    available_item_types_query,
    conversations_query,
    form_completion_requests_query,
    forms_query,
    onboarding_flows_query,
    organization_members_query,
    programs_query,
    unassociated_completed_onboarding_items_query,
)



# Basic full refresh stream
class HealthieApiStream(HttpStream, ABC):
    # url_base = "https://staging-api.gethealthie.com/graphql"

    def __init__(self, config: Mapping[str, Any], **kwargs):
        super().__init__(**kwargs)
        self._base_url = config.get("base_url")
    

    @property
    def url_base(self) -> str:
        return self._base_url
    

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
    
    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return ""
    
    @property
    def http_method(self) -> str:
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


class Users(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("users", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset}
    
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
        
        variables = {}
        if next_page_token:
            variables = next_page_token
        
        return {"query": users_query, "variables": variables}


class AppointmentTypes(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("appointmentTypes", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset, "should_paginate": True}
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("appointmentTypes")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:
        
        variables = {"should_paginate": True}
        if next_page_token:
            variables = next_page_token

        return {"query": appointment_types_query, "variables": variables}


class Appointments(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("appointments", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset, "should_paginate": True}
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("appointments")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:
        
        variables = {"should_paginate": True}
        if next_page_token:
            variables = next_page_token

        return {"query": appointments_query, "variables": variables}


class AvailableItemTypes(HealthieApiStream):
    primary_key = "id"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("availableItemTypes")
        json_data = json.loads(data)
        return json_data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:

        variables = {}
        if next_page_token:
            variables = next_page_token

        return {"query": available_item_types_query, "variables": variables}


class Conversations(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("conversationMemberships", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset}
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("conversationMemberships")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:
        
        variables = {}
        if next_page_token:
            variables = next_page_token

        return {"query": conversations_query, "variables": variables}


class FormCompletionRequests(HealthieApiStream):
    primary_key = "id"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("requestedFormCompletions")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:
        
        variables = {}
        if next_page_token:
            variables = next_page_token

        return {"query": form_completion_requests_query, "variables": variables}


class Forms(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("customModuleForms", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset, "should_paginate": True}
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("customModuleForms")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:

        variables = {"should_paginate": True}
        if next_page_token:
            variables = next_page_token

        return {"query": forms_query, "variables": variables}


class OnboardingFlows(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("onboardingFlows", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset, "should_paginate": True}
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("onboardingFlows")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:

        variables = {"should_paginate": True}
        if next_page_token:
            variables = next_page_token

        return {"query": onboarding_flows_query, "variables": variables}


class OrganizationMembers(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("organizationMembers", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset}
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("organizationMembers")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:
        
        variables = {}
        if next_page_token:
            variables = next_page_token

        return {"query": organization_members_query, "variables": variables}


class Programs(HealthieApiStream):
    primary_key = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_offset = 0

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_data = response.json().get("data", {}).get("courses", [])
        if not current_data:
            return None
                
        self.current_offset += len(current_data)
        return {"offset": self.current_offset, "should_paginate": True}
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("courses")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:
        
        variables = {"should_paginate": True}
        if next_page_token:
            variables = next_page_token

        return {"query": programs_query, "variables": variables}


class UnassociatedCompletedOnboardingItems(HealthieApiStream):
    primary_key = "id"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None
    
    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        data = response.json().get("data").get("unassociatedCompletedOnboardingItems")
        return data

    def request_body_json(
        self,
        stream_state: Optional[Mapping[str, Any]],
        stream_slice: Optional[Mapping[str, Any]] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping[str, Any]]:

        variables = {}
        if next_page_token:
            variables = next_page_token

        return {"query": unassociated_completed_onboarding_items_query, "variables": variables}


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
            base_url = config.get("base_url")
            headers = {
                "Authorization": f"Basic {api_key}",
                "Content-Type": "application/json",
                "AuthorizationSource": "API"
            }

            response = requests.post(url=base_url, json=data, headers=headers)
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
        return [
            Users(authenticator=auth, config=config),
            AppointmentTypes(authenticator=auth, config=config),
            Appointments(authenticator=auth, config=config),
            AvailableItemTypes(authenticator=auth, config=config),
            Conversations(authenticator=auth, config=config),
            FormCompletionRequests(authenticator=auth, config=config),
            Forms(authenticator=auth, config=config),
            OnboardingFlows(authenticator=auth, config=config),
            OrganizationMembers(authenticator=auth, config=config),
            Programs(authenticator=auth, config=config),
            UnassociatedCompletedOnboardingItems(authenticator=auth, config=config),
        ]
