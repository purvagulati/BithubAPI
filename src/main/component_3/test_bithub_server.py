# tests/test_bithub_server.py

import pytest
from bithub_server import BithubServiceServicer
import bithub_service_pb2

@pytest.fixture
def server():
    return BithubServiceServicer()

def test_write_pr_description(server):
    request = bithub_service_pb2.PRDescriptionRequest(repository_id=100)
    context = None  # Mock context as needed
    response = server.WritePRDescription(request, context)
    assert response.draft_description == "Modified the add function in src/main.py to include an additional parameter 'c'."

    