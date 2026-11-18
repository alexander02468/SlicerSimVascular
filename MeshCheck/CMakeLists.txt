set(MODULE_NAME MeshCheck)

set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  MeshCheckTesting/__init__.py
  MeshCheckTesting/${MODULE_NAME}Test.py
  )

slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  WITH_GENERIC_TESTS
  )

if(BUILD_TESTING)
  slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)
endif()
