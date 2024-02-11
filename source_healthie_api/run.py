#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from .source import SourceHealthieApi

def run():
    source = SourceHealthieApi()
    launch(source, sys.argv[1:])
