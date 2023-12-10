## Steps to run gRPC API
1. cd src/main/component_3


## To setup environment:
conda deactivate
source env/bin/activate 

If facing errors:
npm init -y  
python -m pip install grpcio
python -m pip install grpcio-tools
python -m venv env   


# To run Protobuf:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bithub_service.proto

# To Run server and Client: 
    python bithub_server.py
    In differnt terminal, run Client: python client.py

# To run Tests:
    In one terminal run, python server.py
    In differnt terminal, run: pytest


To check missing terms in coverage report:
 pytest --cov=. --cov-report=term-missing 