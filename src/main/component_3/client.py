import grpc
import bithub_service_pb2
import bithub_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bithub_service_pb2_grpc.BithubServiceStub(channel)


        # 1. WritePRDescription
        pr_response = stub.WritePRDescription(
            bithub_service_pb2.PRDescriptionRequest(
                repository_id=10002, 
                committed_changes=bithub_service_pb2.CodeChanges(code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="file1.py", 
                        original_code="print('Hello')", 
                        modified_code="print('Hello, world!')")
            ])
        ))
        print("PR description:", pr_response.draft_description)


        # 2. SmartAutocomplete
        auto_response = stub.SmartAutocomplete(
            bithub_service_pb2.SmartAutocompleteRequest(
                repository_content=bithub_service_pb2.RepositoryContent(files=[
                    bithub_service_pb2.FileContent(
                        file_path="main.py", 
                        content="def main():\n    "
                    )
                ]),
                committed_changes=bithub_service_pb2.CodeChanges(code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="utils.py", 
                        original_code="", 
                        modified_code="def helper():\n    return",
                        change_status=bithub_service_pb2.COMMITTED
                    )
                ]),
                uncommitted_changes=bithub_service_pb2.CodeChanges(code_changes=[ 
                    bithub_service_pb2.CodeChange(
                        file_path="main.py", 
                        original_code="", 
                        modified_code="def main():\n    ",
                        change_status=bithub_service_pb2.UNCOMMITTED
                    )
                ]),
                recent_edits=bithub_service_pb2.Edits(edits=[
                    bithub_service_pb2.Edit(
                        file_path="main.py", 
                        line_number=1, 
                        before_edit="", 
                        after_edit="def main():\n    "
                    )
                ])
            ))
        print("Autocomplete:", auto_response.completion_suggestion)


        # 3. ChatGPTForCode
        code_response = stub.ChatGPTForCode(
            bithub_service_pb2.ChatGPTCodeTaskRequest(
                task_description="Create a login function",
            ))
        print("Code task response:", code_response.response)


        # 4. VirtualPairProgramming
        pair_requests = [bithub_service_pb2.PairProgrammingRequest(
            repository_id=789,
            existing_code=bithub_service_pb2.CodeChanges(code_changes=[
                bithub_service_pb2.CodeChange(
                    file_path="app.py",
                    original_code="def main():\n    print('Hello')",
                    modified_code="def main():\n    print('Hello, world!')"
                ),
                bithub_service_pb2.CodeChange(
                    file_path="utils.py",
                    original_code="def add(a, b):\n    return a + b",
                    modified_code="def add(a, b):\n    return a - b"  # Intentional mistake to demo
                )
            ]),
            stack_trace=bithub_service_pb2.StackTrace(frames=[
                bithub_service_pb2.StackTrace.StackFrame(
                    file_name="utils.py",
                    line_number=2,
                    method_name="add",
                    code_context="def add(a, b):\n    return a - b"
                ),
                bithub_service_pb2.StackTrace.StackFrame(
                    file_name="app.py",
                    line_number=2,
                    method_name="main",
                    code_context="def main():\n    print('Hello, world!')"
                )
            ]),
            issue_description="Fixing a bug where the add function subtracts instead of adding",
        )]

        responses = stub.VirtualPairProgramming(iter(pair_requests))
        for response in responses:
            print("Response from Virtual Pair Programming:", response.plain_english_description)


if __name__ == '__main__':
    run()