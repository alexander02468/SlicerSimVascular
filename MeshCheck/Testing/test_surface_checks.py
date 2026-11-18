
from MeshCheckLib.check import CheckStatus
import MeshCheckLib.surface_checks
import vtkmodules.vtkCommonCore
import vtkmodules.vtkIOXML

def load_vtp() -> vtkmodules.vtkCommonCore.vtkPolyData:
    reader =  vtkmodules.vtkIOXML.vtkXMLPolyDataReader()
    reader.SetFileName("Testing/fixtures/vascular_checker_all_faults.vtp")
    reader.Update()
    return reader.GetOutput()

def test_open_boundaries_check():
    vtp = load_vtp()

    check_result = MeshCheckLib.surface_checks.OpenBoundaryCheck.run(vtp, None)

    # for now, don't really do a deep VTP check, just make sure it's failed
    # TODO add a vtp to compare to as the evidence
    assert (check_result.check_status == CheckStatus.FAILED)
