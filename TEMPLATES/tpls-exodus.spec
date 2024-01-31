%global major_version 2023
%global minor_version 11
%global patch_version 27
Name:           tpls-%{tpls_flavor}-exodus
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        1%{?dist}
Summary:        EXODUS is an advanced FE data file format

License:        BSD-3-Clause
URL:            https://github.com/sandialabs/seacas
Source0:        https://github.com/sandialabs/seacas/archive/refs/tags/v%{major_version}-%{minor_version}-%{patch_version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  tpls-%{tpls_flavor}-hdf5
BuildRequires:  tpls-%{tpls_flavor}-netcdf
BuildRequires:  tpls-%{tpls_flavor}-metis

Requires:       tpls-%{tpls_flavor}-hdf5
Requires:       tpls-%{tpls_flavor}-netcdf
Requires:       tpls-%{tpls_flavor}-metis

%if   "%{tpls_mpi}" == "openempi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
Requires:       intel-oneapi-mpi-devel
%endif

AutoReqProv:    %{tpls_auto_req_prov}

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

%{expand: %setup_tpls_env}
mkdir build && cd build
%{tpls_env} \
%{tpls_cmake} \
	-G "Unix Makefiles" \
    -DCMAKE_C_COMPILER=%{tpls_mpicc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
    -DCMAKE_Fortran_COMPILER=%{tpls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
    -DCMAKE_INSTALL_RPATH=%{tpls_prefix}/lib \
    -DSeacas_ENABLE_SEACASExodus=ON \
	-DSeacas_ENABLE_SEACASExodus_for=OFF \
	-DSeacas_ENABLE_SEACASExoIIv2for32=OFF \
	-DSeacas_ENABLE_TESTS=ON \
	-DSeacas_SKIP_FORTRANCINTERFACE_VERIFY_TEST=ON \
    -DSeacas_HIDE_DEPRECATED_CODE=ON \
    -DSeacas_ENABLE_Fortran=ON \
    -DHDF5_DIR=%{tpls_prefix} \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
	-DSEACASExodus_ENABLE_SHARED=OFF \
	-DSEACASExodus_ENABLE_STATIC=ON \
	-DCMAKE_STATIC_LINKER_FLAGS="-L%{tpls_prefix}/lib" \
%else
	-DBUILD_SHARED_LIBS=ON \
	-DSEACASExodus_ENABLE_SHARED=ON \
	-DSEACASExodus_ENABLE_STATIC=OFF \
%if "%{tpls_compiler}" == "intel"
%if "%{tpls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mpiproot}/lib -Wl,-rpath,%{tpls_mpiproot}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mpiproot}/lib -Wl,-rpath,%{tpls_mpiroot}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
%endif	
%endif
	-DTPL_ENABLE_Netcdf=ON \
	-DTPL_ENABLE_MPI=ON \
	-DTPL_ENABLE_Pthread=OFF \
	-DSEACASExodus_ENABLE_THREADSAFE:BOOL=OFF \
	-DNetCDF_ROOT=%{tpls_prefix} \
%if "%{tpls_mpi}" == "intelmpi"
	-DMPI_BIN_DIR=%{tpls_mpiroot}/bin \
%else
	-DMPI_BIN_DIR=%{tpls_prefix}/bin \
%endif
	-DHDF5_ROOT=%{tpls_prefix} \
	-DHDF5_NO_SYSTEM_PATHS=YES \
	..
	
%make_build

%install
cd build
%make_install

%files
%exclude %{tpls_prefix}/include/SeacasConfig.cmake
%{tpls_prefix}/include/Seacas_version_date.h
%{tpls_prefix}/include/exodusII.h
%{tpls_prefix}/include/exodusII_int.h
%{tpls_prefix}/include/exodusII_par.h
%{tpls_prefix}/include/exodus_config.h
%exclude %{tpls_prefix}/lib/cmake/SEACAS/SEACASConfig.cmake
%exclude %{tpls_prefix}/lib/cmake/SEACAS/SEACASTargets.cmake
%{tpls_prefix}/lib/cmake/SEACASExodus/SEACASExodusConfig.cmake
%{tpls_prefix}/lib/cmake/SEACASExodus/SEACASExodusTargets-release.cmake
%{tpls_prefix}/lib/cmake/SEACASExodus/SEACASExodusTargets.cmake
%exclude %{tpls_prefix}/lib/cmake/Seacas/SeacasConfig.cmake
%exclude %{tpls_prefix}/lib/cmake/Seacas/SeacasConfigVersion.cmake
%exclude %{tpls_prefix}/lib/exodus.py
%exclude %{tpls_prefix}/lib/exodus2.py
%exclude %{tpls_prefix}/lib/exodus3.py
%exclude %{tpls_prefix}/lib/exomerge.py
%exclude %{tpls_prefix}/lib/exomerge2.py
%exclude %{tpls_prefix}/lib/exomerge3.py
%exclude %{tpls_prefix}/lib/external_packages/DLlib/DLlibConfig.cmake
%exclude %{tpls_prefix}/lib/external_packages/DLlib/DLlibConfigVersion.cmake
%exclude %{tpls_prefix}/lib/external_packages/MPI/MPIConfig.cmake
%exclude %{tpls_prefix}/lib/external_packages/MPI/MPIConfigVersion.cmake
%exclude %{tpls_prefix}/lib/external_packages/Netcdf/NetcdfConfig.cmake
%exclude %{tpls_prefix}/lib/external_packages/Netcdf/NetcdfConfigVersion.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libexoIIv2c.a
%{tpls_prefix}/lib/libexoIIv2for.a
%{tpls_prefix}/lib/libexoIIv2for32.a
%{tpls_prefix}/lib/libexodus.a
%{tpls_prefix}/lib/libexodus.so
%{tpls_prefix}/lib/libexodus.so.*
%else
%{tpls_prefix}/lib/libexodus.so
%{tpls_prefix}/lib/libexodus.so.*
%endif
%exclude %{tpls_prefix}/lib/tests/exomerge_unit_test.e
%exclude %{tpls_prefix}/lib/tests/exomerge_unit_test.py
%exclude %{tpls_prefix}/lib/tests/test-assembly.exo
%exclude %{tpls_prefix}/lib/tests/test_exodus3.py


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.27-1
- Initial Package
