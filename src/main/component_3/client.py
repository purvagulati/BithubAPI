import grpc
import bithub_service_pb2
import bithub_service_pb2_grpc


# For creating code changes in Delta
def create_code_change_list(code_changes):
    return [bithub_service_pb2.CodeChange(
                file_path=change["file_path"],
                original_code=change["original_code"],
                modified_code=change["modified_code"],
                change_status=bithub_service_pb2.ChangeStatus.Value(change.get("change_status", "UNCOMMITTED").upper())
            ) for change in code_changes]



def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bithub_service_pb2_grpc.BithubServiceStub(channel)

        # 1. WritePRDescription
        pr_response = stub.WritePRDescription(
            bithub_service_pb2.PRDescriptionRequest(
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
        )
        print("PR description:", pr_response.draft_description)

        # 2. SmartAutocomplete
        autocomplete_request = bithub_service_pb2.SmartAutocompleteRequest(
            repository_content=bithub_service_pb2.RepositoryContent(
                files=[
                    bithub_service_pb2.FileContent(
                        file_path="src/main.py", 
                        content="def add(a, b):\n    "
                    )
                ]
            ),
            committed_changes=bithub_service_pb2.CodeChanges(
                code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="src/main.py", 
                        original_code="", 
                        modified_code=""
                    )
                ]
            ),
            uncommitted_changes=bithub_service_pb2.CodeChanges(
                code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="src/main.py", 
                        original_code="", 
                        modified_code=""
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
        autocomplete_response = stub.SmartAutocomplete(autocomplete_request)
        print("Autocomplete suggestion:", autocomplete_response.completion_suggestion)

        # # 3. ChatGPT for Code

        
        response = stub.ChatGPTForCode(bithub_service_pb2.ChatGPTCodeTaskRequest(
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
        ))

        print("ChatGPT for Code response:", response)
        # if response.delta:
        #     for change in response.delta.changes.code_changes:
        #         print("\nChange in file:", change.file_path)
        #         print("Original code:\n", change.original_code)
        #         print("Modified code:\n", change.modified_code)
        #         print("Change status:", bithub_service_pb2.ChangeStatus.Name(change.change_status))
        
        # 4. Virtual Pair Programming
        # response = stub.VirtualPairProgramming(bithub_service_pb2.PairProgrammingRequest(repository_id=1))
        # print("Client received: ", response)
        #run_virtual_pair_programming(stub)
        response_iterator = stub.VirtualPairProgramming(generate_requests())
        for response in response_iterator:
             print("Virtual Pair Programming response:", response)       
        

def generate_requests():
    requests = [
        {
            "repository_id": 200,
            "issue_description": "Application crashes on startup",
            "existing_code": [
                {
                    "file_path": "src/app.py",
                    "original_code": "print('Hello world')",
                    "modified_code": "print('Hello universe')",
                    "change_status": "UNCOMMITTED"
                }
            ],
            "stack_trace": [
                {
                    "file_name": "app.py",
                    "line_number": 10,
                    "method_name": "main",
                    "code_context": "print('Hello universe')"
                }
            ]
        }
    ]
    for request in requests:
        # if request["existing_code"]:
        code_changes = [
            bithub_service_pb2.CodeChange(
                file_path=change['file_path'],
                original_code=change['original_code'],
                modified_code=change['modified_code'],
                change_status=bithub_service_pb2.ChangeStatus.Value(change['change_status'].upper())
            ) for change in request['existing_code']
        ]

        # if request[stack_trace]:
        stack_frames = [
            bithub_service_pb2.StackTrace.StackFrame(
                file_name=frame["file_name"],
                line_number=frame["line_number"],
                method_name=frame["method_name"],
                code_context=frame["code_context"]
            ) for frame in request["stack_trace"]
        ]
        
        yield bithub_service_pb2.PairProgrammingRequest(
            repository_id=request["repository_id"],
            existing_code=bithub_service_pb2.CodeChanges(code_changes=code_changes),
            stack_trace=bithub_service_pb2.StackTrace(frames=stack_frames),
            issue_description=request["issue_description"]
        )
        
    # yield bithub_service_pb2.PairProgrammingRequest(
    #     repository_id=200,  # Example repository ID
    #     issue_description="Application crashes on startup"
    #     # ... minimal necessary fields ...
    # )



# def generate_requests():
#     # repository_ids = [1]  # Modify as needed
#     # for repo_id in repository_ids:
#     #     yield bithub_service_pb2.PairProgrammingRequest(repository_id=repo_id)
#     #for repo_id in repository_ids:
    
    
#     predefined_requests = [
#         {
#             "repository_id": 200,
#             "existing_code": [
#                 {
#                     "file_path": "src/app.py",
#                     "original_code": "print('Hello world')",
#                     "modified_code": "print('Hello universe')",
#                     "change_status": "UNCOMMITTED"
#                 }
#             ],
#             "stack_trace": [
#                 {
#                     "file_name": "app.py",
#                     "line_number": 10,
#                     "method_name": "main",
#                     "code_context": "print('Hello universe')"
#                 }
#             ],
#             "issue_description": "Application crashes on startup"
#         }
#     ]

#     for predefined_request in predefined_requests:
#         print("Generating request for repository_id:", predefined_request["repository_id"])

#         existing_code = [
#             bithub_service_pb2.CodeChange(
#                 file_path=change["file_path"],
#                original_code=change["original_code"],
#                 modified_code=change["modified_code"],
#                 change_status=bithub_service_pb2.ChangeStatus.Value(change["change_status"])
#             ) for change in predefined_request["existing_code"]
#         ]

#         stack_trace = [
#             bithub_service_pb2.StackTrace.StackFrame(
#                 file_name=frame["file_name"],
#                 line_number=frame["line_number"],
#                 method_name=frame["method_name"],
#                 code_context=frame["code_context"]
#             ) for frame in predefined_request["stack_trace"]
#         ]
#         print("Repositry id is: ", predefined_request["repository_id"])
#         print("Issue description: ", predefined_request["issue_description"])
#         yield bithub_service_pb2.PairProgrammingRequest(
#             repository_id=predefined_request["repository_id"],
#             existing_code=existing_code,
#             stack_trace=stack_trace,
#             issue_description=predefined_request["issue_description"]
#         )
        

# def generate_requests_new():
#     # Example repository IDs to request
#     repository_ids = [1]  # Modify as needed
#     for repo_id in repository_ids:
#         yield bithub_service_pb2.PairProgrammingRequest(repository_id=repo_id)



if __name__ == '__main__':
    run()
        
