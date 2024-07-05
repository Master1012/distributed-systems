# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\":\n\x08LogEntry\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x11\n\toperation\x18\x02 \x01(\t\x12\r\n\x05index\x18\x03 \x01(\x05\"d\n\x0fRequestVoteArgs\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x14\n\x0c\x63\x61ndidate_id\x18\x02 \x01(\x05\x12\x16\n\x0elast_log_index\x18\x03 \x01(\x05\x12\x15\n\rlast_log_term\x18\x04 \x01(\x05\"O\n\x10RequestVoteReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x14\n\x0cvote_granted\x18\x02 \x01(\x08\x12\x17\n\x0fremaining_lease\x18\x03 \x01(\x05\"\xaf\x01\n\x11\x41ppendEntriesArgs\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x11\n\tleader_id\x18\x02 \x01(\x05\x12\x16\n\x0eprev_log_index\x18\x03 \x01(\x05\x12\x15\n\rprev_log_term\x18\x04 \x01(\x05\x12\x1a\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\t.LogEntry\x12\x15\n\rleader_commit\x18\x06 \x01(\x05\x12\x17\n\x0fremaining_lease\x18\x07 \x01(\x05\"3\n\x12\x41ppendEntriesReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\"\"\n\x0fServeClientArgs\x12\x0f\n\x07Request\x18\x01 \x01(\t\"C\n\x10ServeClientReply\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\t\x12\x10\n\x08LeaderID\x18\x02 \x01(\t\x12\x0f\n\x07Success\x18\x03 \x01(\x08\x32\xae\x01\n\x04Raft\x12\x34\n\x0bRequestVote\x12\x10.RequestVoteArgs\x1a\x11.RequestVoteReply\"\x00\x12:\n\rAppendEntries\x12\x12.AppendEntriesArgs\x1a\x13.AppendEntriesReply\"\x00\x12\x34\n\x0bServeClient\x12\x10.ServeClientArgs\x1a\x11.ServeClientReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_LOGENTRY']._serialized_start=14
  _globals['_LOGENTRY']._serialized_end=72
  _globals['_REQUESTVOTEARGS']._serialized_start=74
  _globals['_REQUESTVOTEARGS']._serialized_end=174
  _globals['_REQUESTVOTEREPLY']._serialized_start=176
  _globals['_REQUESTVOTEREPLY']._serialized_end=255
  _globals['_APPENDENTRIESARGS']._serialized_start=258
  _globals['_APPENDENTRIESARGS']._serialized_end=433
  _globals['_APPENDENTRIESREPLY']._serialized_start=435
  _globals['_APPENDENTRIESREPLY']._serialized_end=486
  _globals['_SERVECLIENTARGS']._serialized_start=488
  _globals['_SERVECLIENTARGS']._serialized_end=522
  _globals['_SERVECLIENTREPLY']._serialized_start=524
  _globals['_SERVECLIENTREPLY']._serialized_end=591
  _globals['_RAFT']._serialized_start=594
  _globals['_RAFT']._serialized_end=768
# @@protoc_insertion_point(module_scope)
