from MeshCheckLib.check import CheckStatus
import MeshCheckLib.surface_checks
import vtkmodules.vtkCommonCore
import vtkmodules.vtkIOXML
from pathlib import Path


def load_vtp() -> vtkmodules.vtkCommonCore.vtkPolyData:
    fixture_path = Path(__file__).parent / "fixtures/vascular_checker_all_faults.vtp"
    if not fixture_path.exists():
        raise FileExistsError

    reader = vtkmodules.vtkIOXML.vtkXMLPolyDataReader()
    reader.SetFileName(fixture_path.as_posix())
    reader.Update()
    return reader.GetOutput()


def test_open_edges_check():
    vtp = load_vtp()

    check_result = MeshCheckLib.surface_checks.OpenEdgeCheck.run(vtp, None)

    # for now, don't really do a deep VTP check, just make sure it's failed
    # TODO add a vtp to compare to as the evidence
    assert check_result.check_status == CheckStatus.FAILED


def test_non_manifold_edge_check():
    vtp = load_vtp()

    check_result = MeshCheckLib.surface_checks.NonManifoldEdgeCheck.run(vtp, None)

    # for now, don't really do a deep VTP check, just make sure it's failed
    # TODO add a vtp to compare to as the evidence
    assert check_result.check_status == CheckStatus.FAILED


def test_isolated_surface_check():
    vtp = load_vtp()

    check_result = MeshCheckLib.surface_checks.IsolatedSurfaceCheck.run(vtp, None)

    # for now, don't really do a deep VTP check, just make sure it's failed
    # TODO add a vtp to compare to as the evidence
    assert check_result.check_status == CheckStatus.FAILED
