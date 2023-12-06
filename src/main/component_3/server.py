from concurrent import futures
import grpc
import random
import bithub_service_pb2
import bithub_service_pb2_grpc

# Sample Responses
PR_DESCRIPTIONS = [
    "PR includes several bug fixes and performance improvements.",
    "PR introduces new features and refactors existing modules.",
    "PR addresses critical security vulnerabilities.",
    "PR adds unit tests.",
    "PR updates documentation."
]

AUTOCOMPLETE_SUGGESTIONS = [
        "Suggested Completion: I don't have suggestion for this."
        "Suggested completion: add if(condition) {...}",
        "Suggested completion: add return value;",
        "Suggested completion: add for loop structure.",
        "Suggested completion: add API call implementation."
]

CHAT_GPT_RESPONSES = [
    (
        "Add logging for better debugging.", 
        bithub_service_pb2.Delta(
            is_it_commited=False,
            changes=bithub_service_pb2.CodeChanges(code_changes=[
                bithub_service_pb2.CodeChange(
                    file_path="main.py",
                    original_code="print('Error occurred')",
                    modified_code="logger.error('Error occurred')",
                    change_status=bithub_service_pb2.UNCOMMITTED
                )
            ])
        ),
        False
    ),
    (
        "Optimize the query for faster execution.", 
        bithub_service_pb2.Delta(
            is_it_commited=True,
            changes=bithub_service_pb2.CodeChanges(code_changes=[
                bithub_service_pb2.CodeChange(
                    file_path="database.py",
                    original_code="SELECT * FROM users",
                    modified_code="SELECT id, name FROM users",
                    change_status=bithub_service_pb2.COMMITTED
                )
            ])
        ),
        False
    ),
    (
        "Implement authentication in the API endpoint.",
        bithub_service_pb2.Delta(),  # left blank for clarification
        True
    ),
    (
        "Refactor the class to follow the singleton pattern.",
        bithub_service_pb2.Delta(
            is_it_commited=False,
            changes=bithub_service_pb2.CodeChanges(code_changes=[
                bithub_service_pb2.CodeChange(
                    file_path="user_manager.py",
                    original_code="class UserManager:",
                    modified_code="class UserManager:\n    _instance = None\n    def __new__(cls, *args, **kwargs):\n        if not cls._instance:\n            cls._instance = super(UserManager, cls).__new__(cls, *args, **kwargs)\n        return cls._instance",
                    change_status=bithub_service_pb2.UNCOMMITTED
                )
            ])
        ),
        False
    )
]

PAIR_PROGRAMMING_RESPONSES = [
    (
        "Check the file permissions before opening.",
        bithub_service_pb2.ProposedDelta(
            file_deltas=bithub_service_pb2.Delta(
                is_it_commited=False,
                changes=bithub_service_pb2.CodeChanges(code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="file_manager.py",
                        original_code="with open(file_path, 'r') as file:",
                        modified_code="if os.access(file_path, os.R_OK):\n    with open(file_path, 'r') as file:",
                        change_status=bithub_service_pb2.UNCOMMITTED
                    )
                ])
            )
        ),
        "File permission issue"
    ),
    (
        "Catch the specific exception for better error handling.",
        bithub_service_pb2.ProposedDelta(
            file_deltas=bithub_service_pb2.Delta(
                is_it_commited=False,
                changes=bithub_service_pb2.CodeChanges(code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="error_handling.py",
                        original_code="try:\n    # some code\nexcept Exception as e:\n    # handle exception",
                        modified_code="try:\n    # some code\nexcept ValueError as e:\n    # handle ValueError\nexcept Exception as e:\n    # handle other exceptions",
                        change_status=bithub_service_pb2.UNCOMMITTED
                    )
                ])
            )
        ),
        "Exception handling improvement"
    ),
    (
        "Use thread-safe collections to avoid concurrency issues.",
        bithub_service_pb2.ProposedDelta(
            file_deltas=bithub_service_pb2.Delta(
                is_it_commited=True,
                changes=bithub_service_pb2.CodeChanges(code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="concurrency.py",
                        original_code="my_list = []",
                        modified_code="my_list = threading.Lock()",
                        change_status=bithub_service_pb2.COMMITTED
                    )
                ])
            )
        ),
        "Concurrency handling"
    ),
    (
        "Optimize the loop to reduce computational complexity.",
        bithub_service_pb2.ProposedDelta(
            file_deltas=bithub_service_pb2.Delta(
                is_it_commited=False,
                changes=bithub_service_pb2.CodeChanges(code_changes=[
                    bithub_service_pb2.CodeChange(
                        file_path="optimization.py",
                        original_code="for i in range(len(data)):\n    # process data[i]",
                        modified_code="for item in data:\n    # process item",
                        change_status=bithub_service_pb2.UNCOMMITTED
                    )
                ])
            )
        ),
        "Optimization suggestion"
    )
]

class BithubServiceServicer(bithub_service_pb2_grpc.BithubServiceServicer):
    def WritePRDescription(self, request, context):
        return bithub_service_pb2.PRDescriptionResponse(
            draft_description=random.choice(PR_DESCRIPTIONS)
        )

    def SmartAutocomplete(self, request, context):        
        return bithub_service_pb2.SmartAutocompleteResponse(
            completion_suggestion=random.choice(AUTOCOMPLETE_SUGGESTIONS)
        )

    def ChatGPTForCode(self, request, context):        
        response, delta, needs_clarification = random.choice(CHAT_GPT_RESPONSES)
        return bithub_service_pb2.ChatGPTCodeTaskResponse(
            response=response,
            delta=delta,
            needs_clarification=needs_clarification
        )

    def VirtualPairProgramming(self, request_iterator, context):
        for request in request_iterator:
            description, proposed_delta, plain_english_description = random.choice(PAIR_PROGRAMMING_RESPONSES)
            yield bithub_service_pb2.PairProgrammingResponse(
                conversation=bithub_service_pb2.Conversation(),
                proposed_delta=proposed_delta,
                plain_english_description=plain_english_description
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bithub_service_pb2_grpc.add_BithubServiceServicer_to_server(BithubServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()




