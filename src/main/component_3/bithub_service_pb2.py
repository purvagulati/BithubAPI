# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bithub_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x62ithub_service.proto\x12\x06\x62ithub\"E\n\x05\x44\x65lta\x12\x16\n\x0eis_it_commited\x18\x01 \x01(\x08\x12$\n\x07\x63hanges\x18\x02 \x01(\x0b\x32\x13.bithub.CodeChanges\"z\n\nCodeChange\x12\x11\n\tfile_path\x18\x01 \x01(\t\x12\x15\n\roriginal_code\x18\x02 \x01(\t\x12\x15\n\rmodified_code\x18\x03 \x01(\t\x12+\n\rchange_status\x18\x04 \x01(\x0e\x32\x14.bithub.ChangeStatus\"7\n\x0b\x43odeChanges\x12(\n\x0c\x63ode_changes\x18\x01 \x03(\x0b\x32\x12.bithub.CodeChange\"3\n\rProposedDelta\x12\"\n\x0b\x66ile_deltas\x18\x01 \x01(\x0b\x32\r.bithub.Delta\"W\n\x04\x45\x64it\x12\x11\n\tfile_path\x18\x01 \x01(\t\x12\x13\n\x0bline_number\x18\x02 \x01(\x05\x12\x13\n\x0b\x62\x65\x66ore_edit\x18\x03 \x01(\t\x12\x12\n\nafter_edit\x18\x04 \x01(\t\"$\n\x05\x45\x64its\x12\x1b\n\x05\x65\x64its\x18\x01 \x03(\x0b\x32\x0c.bithub.Edit\"1\n\x0b\x46ileContent\x12\x11\n\tfile_path\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"7\n\x11RepositoryContent\x12\"\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x13.bithub.FileContent\"\x9c\x01\n\nStackTrace\x12-\n\x06\x66rames\x18\x01 \x03(\x0b\x32\x1d.bithub.StackTrace.StackFrame\x1a_\n\nStackFrame\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x13\n\x0bline_number\x18\x02 \x01(\x05\x12\x13\n\x0bmethod_name\x18\x03 \x01(\t\x12\x14\n\x0c\x63ode_context\x18\x04 \x01(\t\"\x91\x01\n\x0c\x43onversation\x12\x37\n\x07\x65ntries\x18\x01 \x03(\x0b\x32&.bithub.Conversation.ConversationEntry\x1aH\n\x11\x43onversationEntry\x12\x0f\n\x07speaker\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\t\"]\n\x14PRDescriptionRequest\x12\x15\n\rrepository_id\x18\x01 \x01(\x05\x12.\n\x11\x63ommitted_changes\x18\x02 \x01(\x0b\x32\x13.bithub.CodeChanges\"2\n\x15PRDescriptionResponse\x12\x19\n\x11\x64raft_description\x18\x01 \x01(\t\"\x9c\x01\n\x18SmartAutocompleteRequest\x12\x35\n\x12repository_content\x18\x01 \x01(\x0b\x32\x19.bithub.RepositoryContent\x12$\n\x07\x63hanges\x18\x02 \x01(\x0b\x32\x13.bithub.CodeChanges\x12#\n\x0crecent_edits\x18\x03 \x01(\x0b\x32\r.bithub.Edits\":\n\x19SmartAutocompleteResponse\x12\x1d\n\x15\x63ompletion_suggestion\x18\x01 \x01(\t\"\xc9\x01\n\x16\x43hatGPTCodeTaskRequest\x12\x18\n\x10task_description\x18\x01 \x01(\t\x12\x15\n\rrepository_id\x18\x02 \x01(\x05\x12.\n\x11\x63ommitted_changes\x18\x03 \x01(\x0b\x32\x13.bithub.CodeChanges\x12\x30\n\x13uncommitted_changes\x18\x04 \x01(\x0b\x32\x13.bithub.CodeChanges\x12\x1c\n\x14\x63urrent_file_context\x18\x05 \x01(\t\"f\n\x17\x43hatGPTCodeTaskResponse\x12\x10\n\x08response\x18\x01 \x01(\t\x12\x1c\n\x05\x64\x65lta\x18\x02 \x01(\x0b\x32\r.bithub.Delta\x12\x1b\n\x13needs_clarification\x18\x03 \x01(\x08\"\x9f\x01\n\x16PairProgrammingRequest\x12\x15\n\rrepository_id\x18\x01 \x01(\x05\x12*\n\rexisting_code\x18\x02 \x01(\x0b\x32\x13.bithub.CodeChanges\x12\'\n\x0bstack_trace\x18\x03 \x01(\x0b\x32\x12.bithub.StackTrace\x12\x19\n\x11issue_description\x18\x04 \x01(\t\"\x97\x01\n\x17PairProgrammingResponse\x12*\n\x0c\x63onversation\x18\x01 \x01(\x0b\x32\x14.bithub.Conversation\x12-\n\x0eproposed_delta\x18\x02 \x01(\x0b\x32\x15.bithub.ProposedDelta\x12!\n\x19plain_english_description\x18\x03 \x01(\t*:\n\x0c\x43hangeStatus\x12\x0f\n\x0bUNCOMMITTED\x10\x00\x12\r\n\tCOMMITTED\x10\x01\x12\n\n\x06PUSHED\x10\x02\x32\xee\x02\n\rBithubService\x12Q\n\x12WritePRDescription\x12\x1c.bithub.PRDescriptionRequest\x1a\x1d.bithub.PRDescriptionResponse\x12X\n\x11SmartAutocomplete\x12 .bithub.SmartAutocompleteRequest\x1a!.bithub.SmartAutocompleteResponse\x12Q\n\x0e\x43hatGPTForCode\x12\x1e.bithub.ChatGPTCodeTaskRequest\x1a\x1f.bithub.ChatGPTCodeTaskResponse\x12]\n\x16VirtualPairProgramming\x12\x1e.bithub.PairProgrammingRequest\x1a\x1f.bithub.PairProgrammingResponse(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bithub_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CHANGESTATUS']._serialized_start=1869
  _globals['_CHANGESTATUS']._serialized_end=1927
  _globals['_DELTA']._serialized_start=32
  _globals['_DELTA']._serialized_end=101
  _globals['_CODECHANGE']._serialized_start=103
  _globals['_CODECHANGE']._serialized_end=225
  _globals['_CODECHANGES']._serialized_start=227
  _globals['_CODECHANGES']._serialized_end=282
  _globals['_PROPOSEDDELTA']._serialized_start=284
  _globals['_PROPOSEDDELTA']._serialized_end=335
  _globals['_EDIT']._serialized_start=337
  _globals['_EDIT']._serialized_end=424
  _globals['_EDITS']._serialized_start=426
  _globals['_EDITS']._serialized_end=462
  _globals['_FILECONTENT']._serialized_start=464
  _globals['_FILECONTENT']._serialized_end=513
  _globals['_REPOSITORYCONTENT']._serialized_start=515
  _globals['_REPOSITORYCONTENT']._serialized_end=570
  _globals['_STACKTRACE']._serialized_start=573
  _globals['_STACKTRACE']._serialized_end=729
  _globals['_STACKTRACE_STACKFRAME']._serialized_start=634
  _globals['_STACKTRACE_STACKFRAME']._serialized_end=729
  _globals['_CONVERSATION']._serialized_start=732
  _globals['_CONVERSATION']._serialized_end=877
  _globals['_CONVERSATION_CONVERSATIONENTRY']._serialized_start=805
  _globals['_CONVERSATION_CONVERSATIONENTRY']._serialized_end=877
  _globals['_PRDESCRIPTIONREQUEST']._serialized_start=879
  _globals['_PRDESCRIPTIONREQUEST']._serialized_end=972
  _globals['_PRDESCRIPTIONRESPONSE']._serialized_start=974
  _globals['_PRDESCRIPTIONRESPONSE']._serialized_end=1024
  _globals['_SMARTAUTOCOMPLETEREQUEST']._serialized_start=1027
  _globals['_SMARTAUTOCOMPLETEREQUEST']._serialized_end=1183
  _globals['_SMARTAUTOCOMPLETERESPONSE']._serialized_start=1185
  _globals['_SMARTAUTOCOMPLETERESPONSE']._serialized_end=1243
  _globals['_CHATGPTCODETASKREQUEST']._serialized_start=1246
  _globals['_CHATGPTCODETASKREQUEST']._serialized_end=1447
  _globals['_CHATGPTCODETASKRESPONSE']._serialized_start=1449
  _globals['_CHATGPTCODETASKRESPONSE']._serialized_end=1551
  _globals['_PAIRPROGRAMMINGREQUEST']._serialized_start=1554
  _globals['_PAIRPROGRAMMINGREQUEST']._serialized_end=1713
  _globals['_PAIRPROGRAMMINGRESPONSE']._serialized_start=1716
  _globals['_PAIRPROGRAMMINGRESPONSE']._serialized_end=1867
  _globals['_BITHUBSERVICE']._serialized_start=1930
  _globals['_BITHUBSERVICE']._serialized_end=2296
# @@protoc_insertion_point(module_scope)
