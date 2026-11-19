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


@dataclass(frozen=True)
class NonManifoldEdgeCheck(check.Check):
    """
    Checks for non-manifold edges (Edges that are shared by 3 polygons)

    """

    definition = check.CheckDefinition(
        id="Non-manifold Surface Check",
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
        featureEdges.BoundaryEdgesOff()
        featureEdges.FeatureEdgesOff()
        featureEdges.ManifoldEdgesOff()
        featureEdges.NonManifoldEdgesOn()
        featureEdges.ColoringOff()
        featureEdges.Update()

        if featureEdges.GetOutput().GetNumberOfCells() == 0:
            return check.CheckResult(check.CheckStatus.PASSED, None)
        else:
            return check.CheckResult(check.CheckStatus.FAILED, featureEdges.GetOutput())


@dataclass(frozen=True)
class IsolatedSurfaceCheck(check.Check):
    """
    Checks if there are any surfaces that are isolated using a connectivity filter. If there are multiple surfaces
    the surface IDs are numbered and labeled according to vtk.ConnectivityFilter
    """

    definition = check.CheckDefinition(
        id="Isolated Surface Check",
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

        connectivity = vtkFiltersCore.vtkConnectivityFilter()
        connectivity.SetInputData(vtk_dataset)
        connectivity.SetExtractionModeToAllRegions()
        connectivity.Update()
        match connectivity.GetNumberOfExtractedRegions():
            case 0:
                # Case where there is no connection is an invalid input, not a failed check
                raise check.CheckException(
                    "No connected regions detected, this check cannot be run"
                )
            case 1:
                return check.CheckResult(check.CheckStatus.PASSED, None)
            case _:
                return check.CheckResult(
                    check.CheckStatus.FAILED, connectivity.GetOutput()
                )
