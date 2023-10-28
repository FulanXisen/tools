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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import program_pb2
import program_pb2_grpc

import subprocess 

class Greeter(program_pb2_grpc.ProgrammerServicer):
    def SayHello(self, request, context):
        return program_pb2.HelloReply(message="Hello, %s!" % request.name)

    def Program(self, request, context):
        command = request.app_name
        try:
            # Use subprocess to execute the CLI program and capture its output
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            # Read and yield the output in real-time as a stream to the client
            for line in process.stdout:
                response = program_pb2.ProgramReply(message=line)
                yield response

            process.wait()
        except Exception as e:
            response = program_pb2.ProgramReply(message=f"Error: {str(e)}")
            yield response

        # q = queue.Queue()
        # stream = program_pb2.ProgramReply()
        # output = subprocess.check_output(["ls","-la"])
        # output = output.decode("utf-8")
        # for i in range(3):
        #     response = program_pb2.ProgramReply(message=output)
        #     yield response


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    program_pb2_grpc.add_ProgrammerServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
