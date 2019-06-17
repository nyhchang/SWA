@echo off
set CUR_DIR=%cd%
set OSGEO4W64_ROOT=%CUR_DIR%\OSGeo4W64
call "%OSGEO4W64_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W64_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W64_ROOT%\bin\py3_env.bat"
path %OSGEO4W64_ROOT%\apps\qgis\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W64_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W64_ROOT%\apps\qgis\qtplugins;%OSGEO4W64_ROOT%\apps\qt5\plugins
set PYTHONPATH=%OSGEO4W64_ROOT%\apps\qgis\python;%PYTHONPATH%
echo Loading, please wait...
python SWA.py
exit