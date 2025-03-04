# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mapreduce.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fmapreduce.proto\"\x1f\n\x08\x43\x65ntroid\x12\x13\n\x0b\x63oordinates\x18\x01 \x03(\x01\"0\n\tDataPoint\x12\x13\n\x0b\x63\x65ntroid_id\x18\x01 \x01(\x05\x12\x0e\n\x06points\x18\x02 \x03(\x01\"\xc5\x01\n\x0eMapTaskRequest\x12\x11\n\tmapper_id\x18\x01 \x01(\x05\x12\x13\n\x0bnum_mappers\x18\x02 \x01(\x05\x12\x14\n\x0cnum_reducers\x18\x03 \x01(\x05\x12\x16\n\x0enum_iterations\x18\x04 \x01(\x05\x12\x17\n\x0finput_file_path\x18\x05 \x01(\t\x12\x13\n\x0bstart_index\x18\x06 \x01(\x05\x12\x11\n\tend_index\x18\x07 \x01(\x05\x12\x1c\n\tcentroids\x18\x08 \x03(\x0b\x32\t.Centroid\".\n\x0bMapResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"p\n\x11ReduceTaskRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x13\n\x0bnum_mappers\x18\x02 \x01(\x05\x12\x14\n\x0cnum_reducers\x18\x03 \x01(\x05\x12\x1c\n\tcentroids\x18\x04 \x03(\x0b\x32\t.Centroid\"T\n\x12ReduceTaskResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1c\n\tcentroids\x18\x03 \x03(\x0b\x32\t.Centroid\"-\n\x17ReceiveKeyValuesRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\"L\n\x18ReceiveKeyValuesResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x1f\n\x0b\x64\x61ta_points\x18\x02 \x03(\x0b\x32\n.DataPoint2\xbb\x01\n\x0fKMeansMapReduce\x12(\n\x07MapTask\x12\x0f.MapTaskRequest\x1a\x0c.MapResponse\x12\x35\n\nReduceTask\x12\x12.ReduceTaskRequest\x1a\x13.ReduceTaskResponse\x12G\n\x10ReceiveKeyValues\x12\x18.ReceiveKeyValuesRequest\x1a\x19.ReceiveKeyValuesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mapreduce_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CENTROID']._serialized_start=19
  _globals['_CENTROID']._serialized_end=50
  _globals['_DATAPOINT']._serialized_start=52
  _globals['_DATAPOINT']._serialized_end=100
  _globals['_MAPTASKREQUEST']._serialized_start=103
  _globals['_MAPTASKREQUEST']._serialized_end=300
  _globals['_MAPRESPONSE']._serialized_start=302
  _globals['_MAPRESPONSE']._serialized_end=348
  _globals['_REDUCETASKREQUEST']._serialized_start=350
  _globals['_REDUCETASKREQUEST']._serialized_end=462
  _globals['_REDUCETASKRESPONSE']._serialized_start=464
  _globals['_REDUCETASKRESPONSE']._serialized_end=548
  _globals['_RECEIVEKEYVALUESREQUEST']._serialized_start=550
  _globals['_RECEIVEKEYVALUESREQUEST']._serialized_end=595
  _globals['_RECEIVEKEYVALUESRESPONSE']._serialized_start=597
  _globals['_RECEIVEKEYVALUESRESPONSE']._serialized_end=673
  _globals['_KMEANSMAPREDUCE']._serialized_start=676
  _globals['_KMEANSMAPREDUCE']._serialized_end=863
# @@protoc_insertion_point(module_scope)
