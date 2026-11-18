# MeshCheck

Mesh check is a module written to perform headless and interactive mesh checks for Surface meshes and Volume meshes. The checks themselves are designed to be not dependent on the Slicer runtime at all and can be tested independently using `pytest`.

## Current status

### Surface Checks

The following surface checks are included:

- Open boundary: Checks for edges that have only one face connected

## Future work

Future work and roadmap can be found at https://github.com/SimVascular/SlicerSimVascular/issues/15

Slicer integration is planned, but not yet implemented.