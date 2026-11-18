# abstract base classes and other things that are used by all checks

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any
from vtkmodules.vtkCommonDataModel import vtkDataSet

@dataclass(frozen=True)
class CheckException(Exception):
    """
    Something goes wrong in the Check itself. This could be such as incorrect inputs.
    """
    message : str

class MeshType(Enum):
    SURFACE = auto()
    VOLUME = auto()

class CheckStatus(Enum):
    PASSED = auto()
    FAILED = auto()

@dataclass(frozen=True)
class CheckResult:
    """
    Represents the results for a single check. If no evidence is needed, then None can be returned (no evidence)
    """
    check_status : CheckStatus
    evidence : vtkDataSet | None


@dataclass(frozen=True)
class CheckDefinition:
    id : str
    mesh_type : MeshType
    param_types : tuple[type, ...] | None

@dataclass(frozen=True)
class Check(ABC):
    """
    Checks are required to declaratively define themselves through an instance of CheckDefinition
    """
    definition : CheckDefinition

    @classmethod
    @abstractmethod
    def run(cls, vtk_dataset : vtkDataSet, params : tuple[Any, ...] | None) -> CheckResult:
        ...

    @classmethod
    def validate_params(cls, params : tuple[Any, ...] | None) -> None:

        match cls.definition.param_types:
            case None:
                if params is not None:
                     raise CheckException("No parameters allowed in this check")
            case _:
                for (p, p_type) in zip(params, cls.definition.param_types):
                            if not isinstance(p, p_type):
                                raise CheckException(f"{p} is not type: {p_type}")                

    