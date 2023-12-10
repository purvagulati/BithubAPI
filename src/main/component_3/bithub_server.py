import logging
from concurrent import futures
import grpc
import bithub_service_pb2
import bithub_service_pb2_grpc
from db import PR_DESCRIPTION_DATABASE, SMART_AUTOCOMPLETE_DATABASE, CHATGPT_CODE_DATABASE, VIRTUAL_PAIR_PROGRAMMING_DATABASE


class BithubServiceServicer(bithub_service_pb2_grpc.BithubServiceServicer):
    # 1. Write a PR description for me
    def WritePRDescription(self, request, context):

        for key, value in PR_DESCRIPTION_DATABASE.items():
            if value['request']['repository_id'] == request.repository_id:
                return bithub_service_pb2.PRDescriptionResponse(
                    draft_description=value['response']['draft_description']
                )
        return bithub_service_pb2.PRDescriptionResponse(
            draft_description="No description available for this request."
        )

    # 2. Smart Autocomplete
    def request_matches(self, predefined_request, actual_request):
        # Implement your logic to compare the actual request with the predefined request
        # For example, you can compare repository_content, committed_changes, etc.
        # This is a simplified comparison logic
        return (
            predefined_request['repository_content']['files'][0]['content'] ==
            actual_request.repository_content.files[0].content
        )
    
    def SmartAutocomplete(self, request, context):
        # Iterate through each entry in the database
        for entry in SMART_AUTOCOMPLETE_DATABASE.values():
            # Check if the request matches the predefined scenario
            if self.request_matches(entry["request"], request):
                # If a match is found, return the corresponding response
                return bithub_service_pb2.SmartAutocompleteResponse(
                    completion_suggestion=entry['response']['completion_suggestion']
                )

        # If no match is found, return a default response
        return bithub_service_pb2.SmartAutocompleteResponse(
            completion_suggestion="No autocomplete suggestion available."
        )

    # 3. ChatGPT for Code
    def ChatGPTForCode(self, request, context):
        task_description = request.task_description
        repository_id = request.repository_id

        # Search for a matching task in the database
        for task_id, task in CHATGPT_CODE_DATABASE.items():
        #     if task["request"]["repository_id"] == repository_id:
            if (task["request"]["repository_id"] == repository_id and
                task["request"]["task_description"] == task_description):  # Match based on repository_id and task_description

                response_data = task["response"]
                delta = response_data.get("delta", {})
                code_changes_list = delta.get("changes", [])  # Directly access the list of changes

                # Convert the changes for the response
                converted_changes = [
                   bithub_service_pb2.CodeChange(
                        file_path=change["file_path"],
                        original_code=change["original_code"],
                        modified_code=change["modified_code"],
                        change_status=bithub_service_pb2.ChangeStatus.Value(
                            change.get("change_status", "UNCOMMITTED").upper()
                        )
                    ) for change in code_changes_list
                ]

                # for change in code_changes_list:
                #     print(change["file_path"])
                return bithub_service_pb2.ChatGPTCodeTaskResponse(
                    response=response_data["response"],
                    delta=bithub_service_pb2.Delta(
                        is_it_committed=delta.get("is_it_committed", False),
                        changes=bithub_service_pb2.CodeChanges(code_changes=converted_changes)
                    ),
                    needs_clarification=response_data.get("needs_clarification", False)
                )
                  
        # This is reached if no match is found
        return bithub_service_pb2.ChatGPTCodeTaskResponse(needs_clarification=True)    
    
    # 4. Virtual Pair Programming
    def VirtualPairProgramming(self, request_iterator, context):
        for request in request_iterator:
            for entry in VIRTUAL_PAIR_PROGRAMMING_DATABASE.values():
                if (entry["request"]["repository_id"] == request.repository_id
                    and entry["request"]["issue_description"] == request.issue_description):
                    
                    response_data = entry["response"]
                    
                    conversation_entry = bithub_service_pb2.Conversation(
                         entries=[
                            bithub_service_pb2.Conversation.ConversationEntry(
                                speaker=entry["speaker"],
                                message=entry["message"],
                                timestamp=entry["timestamp"]
                            ) for entry in response_data["conversation"]
                        ]
                    )
                    print("added Conversation entry")
                    delta = bithub_service_pb2.ProposedDelta(
                        file_deltas=bithub_service_pb2.Delta(
                            is_it_committed=response_data["proposed_delta"]["file_deltas"]["is_it_committed"],
                            changes=bithub_service_pb2.CodeChanges(
                                code_changes=[
                                    bithub_service_pb2.CodeChange(
                                        file_path=change["file_path"],
                                        original_code=change["original_code"],
                                        modified_code=change["modified_code"],
                                        change_status=change["change_status"]
                                    ) for change in response_data["proposed_delta"]["file_deltas"]["changes"]
                                ]
                            )
                        )
                    )
                    
                    response = bithub_service_pb2.PairProgrammingResponse(
                        conversation=conversation_entry,
                        proposed_delta=delta,
                        plain_english_description=response_data["plain_english_description"]
                    )
                    
                    yield response

    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bithub_service_pb2_grpc.add_BithubServiceServicer_to_server(BithubServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
