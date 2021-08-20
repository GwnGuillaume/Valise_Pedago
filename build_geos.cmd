REM This script is called from appveyor.yml

if exist %GEOS_INSTALL% (
  echo Using cached %GEOS_INSTALL%
) else (
  echo Building %GEOS_INSTALL%

  cd C:\projects

  curl -fsSO http://download.osgeo.org/geos/geos-%GEOS_VERSION%.tar.bz2
  "C:\Program Files\7-Zip\7z.exe" x geos-%GEOS_VERSION%.tar.bz2
  "C:\Program Files\7-Zip\7z.exe" x geos-%GEOS_VERSION%.tar
  cd geos-%GEOS_VERSION% || exit /B 5

  pip install ninja
  cmake --version

REM  mkdir build
REM  cd build
REM  cmake -GNinja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=%GEOS_INSTALL% .. || exit /B 1
REM  cmake --build . --config Release || exit /B 2
REM  ctest . --config Release || exit /B 3
REM  cmake --install . --config Release || exit /B 4
REM  cd ..
  mkdir build
  cd build
  cmake -GNinja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=%GEOS_INSTALL% .. || exit /B 1
  cmake --build . --config Release || exit /B 2
  REM disable ctest because of issue with GEOS 3.9.0
  REM see https://trac.osgeo.org/geos/ticket/1081
  REM ctest . --config Release || exit /B 3
  cmake --install . --config Release || exit /B 4
  cd ..
)
