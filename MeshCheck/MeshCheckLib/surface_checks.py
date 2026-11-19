"""
Surface checks

"""

from dataclasses import dataclass
from typing import Any

import vtkmodules.vtkCommonDataModel as vtkCommonDataModel
import vtkmodules.vtkFiltersCore as vtkFiltersCore

from . import check


@dataclass(frozen=True)
class OpenEdgeCheck(check.Check):
    """
    Checks for open edges, i.e. edges that are connected only on one face.

    """

    definition = check.CheckDefinition(
        id="Open Boundary Surface Check",
        mesh_type=check.MeshType.SURFACE,
        param_types=None,
    )

    @classmethod
    def run(cls, vtk_dataset, params: tuple[Any] | None) -> check.CheckResult:
        cls.validate_params(params)
        if not isinstance(vtk_dataset, vtkCommonDataModel.vtkPolyData):
            raise check.CheckException(
                f"vtk of type {type(vtk_dataset)} is not of type vtkPolyData"
            )
        featureEdges = vtkFiltersCore.vtkFeatureEdges()
        featureEdges.SetInputData(vtk_dataset)
        featureEdges.BoundaryEdgesOn()
        featureEdges.FeatureEdgesOff()
        featureEdges.ManifoldEdgesOff()
        featureEdges.NonManifoldEdgesOff()
        featureEdges.ColoringOff()
        featureEdges.Update()

        if featureEdges.GetOutput().GetNumberOfCells() == 0:
            return check.CheckResult(check.CheckStatus.PASSED, None)
        else:
            return check.CheckResult(check.CheckStatus.FAILED, featureEdges.GetOutput())
