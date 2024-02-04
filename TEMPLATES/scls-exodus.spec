%global major_version 2023
%global minor_version 11
%global patch_version 27

%define scls_oflags -O2

Name:           scls-%{scls_flavor}-exodus
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        1%{?dist}
Summary:        EXODUS is an advanced FE data file format

License:        BSD-3-Clause
URL:            https://github.com/sandialabs/seacas
Source0:        https://github.com/sandialabs/seacas/archive/refs/tags/v%{major_version}-%{minor_version}-%{patch_version}.tar.gz

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  scls-%{scls_flavor}-hdf5
BuildRequires:  scls-%{scls_flavor}-netcdf
BuildRequires:  scls-%{scls_flavor}-metis

Requires:       scls-%{scls_flavor}-hdf5
Requires:       scls-%{scls_flavor}-netcdf
Requires:       scls-%{scls_flavor}-metis

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

BuildRequires:  libcurl-devel
BuildRequires:  libcurl



%description
EXODUS is the successor of the widely used finite element (FE) data file format EXODUS (henceforth referred to as EXODUS I) developed by Mills-Curran and Flanagan. It continues the concept of a common database for multiple application codes (mesh generators, analysis codes, visualization software, etc.) rather than code-specific utilities, affording flexibility and robustness for both the application code developer and application code user. By using the EXODUS data model, a user inherits the flexibility of using a large array of application codes (including vendor-supplied codes) which access this common data file directly or via translators.

The uses of the EXODUS data model include the following:

	o Problem definition – mesh generation, specification of locations of boundary conditions and load application,
	o specification of material types.
	o Simulation – model input and results output.
	o Visualization – model verification, results postprocessing, data interrogation, and analysis tracking.


%prep
%setup -q -n seacas-%{major_version}-%{minor_version}-%{patch_version}

%build

# fisx shebangs
sed -i "s|#!/usr/bin/env python|#!/usr/bin/env python3|g" ./packages/seacas/scripts/tests/test_exodus3.py
sed -i "s|#!/usr/bin/env python|#!/usr/bin/env python3|g" ./packages/seacas/scripts/tests/exomerge_unit_test.py

%{expand: %setup_scls_env}
mkdir build && cd build
%{scls_env} \
LDFLAGS+=" -lcurl" \
%{scls_cmake} \
	-G "Unix Makefiles" \
    -DCMAKE_C_COMPILER=%{scls_mpicc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
    -DCMAKE_INSTALL_RPATH=%{scls_prefix}/lib \
    -DSeacas_ENABLE_SEACASExodus=ON \
	-DSeacas_ENABLE_SEACASExodus_for=OFF \
	-DSeacas_ENABLE_SEACASExoIIv2for32=OFF \
	-DSeacas_ENABLE_TESTS=ON \
	-DSeacas_SKIP_FORTRANCINTERFACE_VERIFY_TEST=ON \
    -DSeacas_HIDE_DEPRECATED_CODE=ON \
    -DSeacas_ENABLE_Fortran=ON \
    -DHDF5_DIR=%{scls_prefix} \
    -DBUILD_TESTING=OFF \
%if "%{scls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
	-DSEACASExodus_ENABLE_SHARED=OFF \
	-DSEACASExodus_ENABLE_STATIC=ON \
%else
	-DBUILD_SHARED_LIBS=ON \
	-DSEACASExodus_ENABLE_SHARED=ON \
	-DSEACASExodus_ENABLE_STATIC=OFF \
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mpiproot}/lib -Wl,-rpath,%{scls_mpiproot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mpiproot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif	
%endif
	-DTPL_ENABLE_Netcdf=ON \
	-DTPL_ENABLE_MPI=ON \
	-DTPL_ENABLE_Pthread=OFF \
	-DSEACASExodus_ENABLE_THREADSAFE:BOOL=OFF \
	-DNetCDF_ROOT=%{scls_prefix} \
%if "%{scls_mpi}" == "intelmpi"
	-DMPI_BIN_DIR=%{scls_mpiroot}/bin \
%else
	-DMPI_BIN_DIR=%{scls_prefix}/bin \
%endif
	-DHDF5_ROOT=%{scls_prefix} \
	-DHDF5_NO_SYSTEM_PATHS=YES \
	..

make

%install
cd build
%make_install

%files
%exclude %{scls_prefix}/include/SeacasConfig.cmake
%{scls_prefix}/include/Seacas_version_date.h
%{scls_prefix}/include/exodusII.h
%{scls_prefix}/include/exodusII_int.h
%{scls_prefix}/include/exodusII_par.h
%{scls_prefix}/include/exodus_config.h
%exclude %{scls_prefix}/lib/cmake/SEACAS/SEACASConfig.cmake
%exclude %{scls_prefix}/lib/cmake/SEACAS/SEACASTargets.cmake
%{scls_prefix}/lib/cmake/SEACASExodus/SEACASExodusConfig.cmake
%{scls_prefix}/lib/cmake/SEACASExodus/SEACASExodusTargets-release.cmake
%{scls_prefix}/lib/cmake/SEACASExodus/SEACASExodusTargets.cmake
%exclude %{scls_prefix}/lib/cmake/Seacas/SeacasConfig.cmake
%exclude %{scls_prefix}/lib/cmake/Seacas/SeacasConfigVersion.cmake
%exclude %{scls_prefix}/lib/external_packages/DLlib/DLlibConfig.cmake
%exclude %{scls_prefix}/lib/external_packages/DLlib/DLlibConfigVersion.cmake
%exclude %{scls_prefix}/lib/external_packages/MPI/MPIConfig.cmake
%exclude %{scls_prefix}/lib/external_packages/MPI/MPIConfigVersion.cmake
%exclude %{scls_prefix}/lib/external_packages/Netcdf/NetcdfConfig.cmake
%exclude %{scls_prefix}/lib/external_packages/Netcdf/NetcdfConfigVersion.cmake
%exclude %{scls_prefix}/lib/tests
%exclude %{scls_prefix}/lib/*.py
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libexodus.a
%exclude %{scls_prefix}/lib/libexoIIv2c.a
%else
%{scls_prefix}/lib/libexodus.so
%{scls_prefix}/lib/libexodus.so.*
%endif


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.27-1
- Initial Package
