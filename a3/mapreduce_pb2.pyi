from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Centroid(_message.Message):
    __slots__ = ("coordinates",)
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    coordinates: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, coordinates: _Optional[_Iterable[float]] = ...) -> None: ...

class DataPoint(_message.Message):
    __slots__ = ("centroid_id", "points")
    CENTROID_ID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    centroid_id: int
    points: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, centroid_id: _Optional[int] = ..., points: _Optional[_Iterable[float]] = ...) -> None: ...

class MapTaskRequest(_message.Message):
    __slots__ = ("mapper_id", "num_mappers", "num_reducers", "num_iterations", "input_file_path", "start_index", "end_index", "centroids")
    MAPPER_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_MAPPERS_FIELD_NUMBER: _ClassVar[int]
    NUM_REDUCERS_FIELD_NUMBER: _ClassVar[int]
    NUM_ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    INPUT_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    END_INDEX_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    mapper_id: int
    num_mappers: int
    num_reducers: int
    num_iterations: int
    input_file_path: str
    start_index: int
    end_index: int
    centroids: _containers.RepeatedCompositeFieldContainer[Centroid]
    def __init__(self, mapper_id: _Optional[int] = ..., num_mappers: _Optional[int] = ..., num_reducers: _Optional[int] = ..., num_iterations: _Optional[int] = ..., input_file_path: _Optional[str] = ..., start_index: _Optional[int] = ..., end_index: _Optional[int] = ..., centroids: _Optional[_Iterable[_Union[Centroid, _Mapping]]] = ...) -> None: ...

class MapResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ReduceTaskRequest(_message.Message):
    __slots__ = ("reducer_id", "num_mappers", "num_reducers", "centroids")
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_MAPPERS_FIELD_NUMBER: _ClassVar[int]
    NUM_REDUCERS_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    num_mappers: int
    num_reducers: int
    centroids: _containers.RepeatedCompositeFieldContainer[Centroid]
    def __init__(self, reducer_id: _Optional[int] = ..., num_mappers: _Optional[int] = ..., num_reducers: _Optional[int] = ..., centroids: _Optional[_Iterable[_Union[Centroid, _Mapping]]] = ...) -> None: ...

class ReduceTaskResponse(_message.Message):
    __slots__ = ("success", "message", "centroids")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    centroids: _containers.RepeatedCompositeFieldContainer[Centroid]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., centroids: _Optional[_Iterable[_Union[Centroid, _Mapping]]] = ...) -> None: ...

class ReceiveKeyValuesRequest(_message.Message):
    __slots__ = ("reducer_id",)
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    def __init__(self, reducer_id: _Optional[int] = ...) -> None: ...

class ReceiveKeyValuesResponse(_message.Message):
    __slots__ = ("success", "data_points")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    data_points: _containers.RepeatedCompositeFieldContainer[DataPoint]
    def __init__(self, success: bool = ..., data_points: _Optional[_Iterable[_Union[DataPoint, _Mapping]]] = ...) -> None: ...
