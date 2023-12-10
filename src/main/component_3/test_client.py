
import pytest
import grpc
import bithub_service_pb2
import bithub_service_pb2_grpc

@pytest.fixture(scope="module")
def stub():
    channel = grpc.insecure_channel('localhost:50051')
    return bithub_service_pb2_grpc.BithubServiceStub(channel)

# Test for normal behavior
def test_write_pr_description(stub):
    pr_request = bithub_service_pb2.PRDescriptionRequest(
        repository_id=100,
        committed_changes=bithub_service_pb2.CodeChanges(
            code_changes=[
                bithub_service_pb2.CodeChange(
                    file_path="src/main.py",
                    original_code="def add(a, b):\n    return a + b",
                    modified_code="def add(a, b):\n    return a + b + c",
                    change_status=1  # COMMITTED
                )
            ]
        )
    )
    response = stub.WritePRDescription(pr_request)

    expected_description = "Modified the add function in src/main.py to include an additional parameter 'c'."
    assert response.draft_description == expected_description

# PR Description error path
def test_write_pr_description_error(stub):
    pr_request = bithub_service_pb2.PRDescriptionRequest(
        repository_id=999,  # Invalid repository ID
    )
    response = stub.WritePRDescription(pr_request)
    assert response.draft_description == "No description available for this request."
    # with pytest.raises(grpc.RpcError) as e:
    #     stub.WritePRDescription(pr_request)
    # assert e.value.code() == grpc.StatusCode.NOT_FOUND

# Test for normal behavior
def test_smart_autocomplete(stub):
    autocomplete_request = bithub_service_pb2.SmartAutocompleteRequest(
        repository_content=bithub_service_pb2.RepositoryContent(
            files=[
                bithub_service_pb2.FileContent(
                    file_path="src/main.py", 
                    content="def add(a, b):\n    "
                )
            ]
        ),
        recent_edits=bithub_service_pb2.Edits(
            edits=[
                bithub_service_pb2.Edit(
                    file_path="src/main.py", 
                    line_number=2, 
                    before_edit="", 
                    after_edit=""
                )
            ]
        )
    )
    response = stub.SmartAutocomplete(autocomplete_request)
    expected_suggestion = "return a + b"
    assert response.completion_suggestion == expected_suggestion


def test_smart_autocomplete_error(stub):
    autocomplete_request = bithub_service_pb2.SmartAutocompleteRequest(
        repository_content=bithub_service_pb2.RepositoryContent(
            files=[
                bithub_service_pb2.FileContent(
                    file_path="src/main.py", 
                )
            ]
        )
    )
    
    response = stub.SmartAutocomplete(autocomplete_request)
    assert response.completion_suggestion == "No autocomplete suggestion available."
    # with pytest.raises(grpc.RpcError) as e:
    #     stub.SmartAutocomplete(autocomplete_request)
    # assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT

def test_chatgpt_for_code(stub):
    chatgpt_request = bithub_service_pb2.ChatGPTCodeTaskRequest(
        task_description="Add a function to calculate the sum of two numbers",
        repository_id=100,
        committed_changes=bithub_service_pb2.CodeChanges(
                code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="src/math_utils.py", 
                        original_code="def multiply(a, b): return a * b", 
                        modified_code="def multiply(a, b, c=1): return a * b * c"
                    )
                ]
            ),
            uncommitted_changes=bithub_service_pb2.CodeChanges(
                code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="src/main.py", 
                        original_code="print('Hello')", 
                        modified_code="print('Hello, world!')"
                    )
                ]
            ),
        current_file_context="src/math_utils.py"
    )
    response = stub.ChatGPTForCode(chatgpt_request)
    expected_response = "Function 'add' added to src/math_utils.py" 
    assert response.response == expected_response
    assert response.needs_clarification == False
    
    
def test_chatgpt_for_code_error(stub):
    chatgpt_request = bithub_service_pb2.ChatGPTCodeTaskRequest(
        task_description="Unclear or ambiguous task description",
        repository_id=100,
    )
    # with pytest.raises(grpc.RpcError) as e:
    #     stub.ChatGPTForCode(chatgpt_request)
    # assert e.value.code() == grpc.StatusCode.FAILED_PRECONDITION
    response = stub.ChatGPTForCode(chatgpt_request)
    assert response.needs_clarification == True



def test_virtual_pair_programming(stub):
    
    request_iterator = iter([
        bithub_service_pb2.PairProgrammingRequest(
            repository_id=200, 
            issue_description="Application crashes on startup"
        )
    ])
    responses = list(stub.VirtualPairProgramming(request_iterator))
    assert len(responses) == 1
    assert responses[0].plain_english_description == "Fixed a syntax error in src/app.py"


def test_virtual_pair_programming_not_found(stub):
    request_iterator = iter([
        bithub_service_pb2.PairProgrammingRequest(
            repository_id=999, # Non-existing ID
            issue_description="...." # Unclear issue description
        )  
    ])
    responses = list(stub.VirtualPairProgramming(request_iterator))
    assert len(responses) == 0  # No response expected for non-existing ID
