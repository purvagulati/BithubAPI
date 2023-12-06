## Steps to run gRPC API
1. cd /src/main/component_3


## To setup:
conda decativate
source env/bin/activate  
npm init -y  
python -m pip install grpcio
python -m pip install grpcio-tools
python -m venv env   


To run Protobuf:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bithub_service.proto

Run server: python server.py
In differnt terminal, Run Client: python client.py


To check missing terms in coverage report:
 pytest --cov=. --cov-report=term-missing 