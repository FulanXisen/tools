# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import program_pb2
import program_pb2_grpc
import argparse

def parse_args():
    """Parses and returns command line arguments."""
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--bootloader',
        action='store_true',
        type=str,
        default="",
        help='Build without refresh makefile')

    parser.add_argument(
        '--clean',
        action='store_true',
        default=False,
        help='Clean before Build')

    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='Build debuggable')

    parser.add_argument(
        '--bear',
        action='store_true',
        default=False,
        help='Build Bear\'s Compiler Database')

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = program_pb2_grpc.ProgrammerStub(channel)
        response = stub.SayHello(program_pb2.HelloRequest(name="you"))
        print("Greeter client received: " + response.message)
        response = stub.Program(program_pb2.ProgramRequest(ota_name="CC-OtaBootloader_1.1.hex", app_name="cmake ../"))
        for reply in response:
            print(reply.message, end="")


if __name__ == "__main__":
    logging.basicConfig()
    run()
