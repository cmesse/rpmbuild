Name:           tpls-%{tpls_flavor}-scotch
Version:        7.0.4
Release:        1%{?dist}
Summary:        Graph, mesh and hypergraph partitioning library

License:        CeCILL-C
URL:            https://www.labri.fr/perso/pelegrin/scotch/
Source0:        https://gitlab.inria.fr/scotch/scotch/-/archive/v%{version}/scotch-v%{version}.tar.bz2

# taken from debian
Patch1:         metis-header.patch
Patch2:         include_headers.patch
Patch3:         default_metis_v5.patch     


BuildRequires:  %{tpls_rpm_cc}  >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_fc}  >= %{tpls_comp_minver}
BuildRequires: make
BuildRequires: flex
BuildRequires: bison
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel

%if   "%{tpls_mpi}" == "openempi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
BuildRequires:  intel-oneapi-mpi
%endif

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-scalapack
%endif


AutoReqProv:   %{tpls_auto_req_prov}

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch libraries are packaged in the


%prep
%setup -q -n scotch-v%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%{expand: %setup_tpls_env}

pwd

%{tpls_env} \
CC=%{tpls_mpicc} \
CXX=%{tpls_mpicxx} \
FC=%{tpls_mpifort} \
%{tpls_cmake} . \
%if "%{tpls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%endif
 	-DBUILD_LIBESMUMPS=ON \
 	-DBUILD_LIBSCOTCHMETIS=ON \
 	-DBUILD_PTSCOTCH=ON \
 	-DINTSIZE=%{tpls_int} \
 	-DCMAKE_C_COMPILER=%{tpls_mpicc} \
 	-DCMAKE_C_FLAGS="%{tpls_cflags}" \
 	-DCMAKE_C_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_CXX_COMPILER=%{tpls_mpicxx} \
 	-DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
 	-DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_Fortran_COMPILER=%{tpls_mpifort} \
 	-DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
 	-DCMAKE_Fortran_FLAGS_RELEASE=-DNDEBUG \
 	-DINSTALL_METIS_HEADERS=OFF \
 	-DMPIEXEC_MAX_NUMPROCS=%{tpls_maxprocs} \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath,${I_MPI_ROOT}/lib -Wl,-rpath,${tpls_prefix}/lib -Wl,--build-id" \
%if "%{tpls_mpi}" == "intelmpi"
 	-DCMAKE_SHARED_LINKER_FLAGS="-Wl,-rpath,${I_MPI_ROOT}/lib -Wl,-rpath,${tpls_prefix}/lib -Wl,--build-id"
%else
 	-DCMAKE_SHARED_LINKER_FLAGS="-Wl,-rpath,${tpls_prefix}/lib -Wl,--build-id"
%endif

%make_build

# build the static libraries
%if "%{tpls_libs}" == "shared"
echo "Building shared libraries"

# Loop for building esmumps and ptesmumps libraries
for l in esmumps ptesmumps; do
    echo "Building lib${l}.so"
    # Compile and link the library
    %{tpls_mpicc} -Wl,-rpath,${tpls_prefix}/lib -Wl,--build-id -shared -o ./lib/lib${l}.so ./src/esmumps/CMakeFiles/${l}.dir/*.o
done

# Loop for building ptscotch libraries
for l in ptscotch ptscotcherr ptscotcherrexit scotch scotcherr scotcherrexit; do
    echo "Building lib${l}.so"
    # Compile and link the library
    %{tpls_mpicc} -Wl,-rpath,${tpls_prefix}/lib -Wl,--build-id -shared -o ./lib/lib${l}.so ./src/libscotch/CMakeFiles/${l}.dir/*.o
done

# Loop for building scotchmetis libraries
for l in ptscotchparmetisv3 scotchmetisv3 scotchmetisv5; do
    echo "Building lib${l}.so"
    # Compile and link the library
    %{tpls_mpicc} -Wl,-rpath,${tpls_prefix}/lib -Wl,--build-id -shared -o ./lib/lib${l}.so ./src/libscotchmetis/CMakeFiles/${l}.dir/*.o
done

%endif


%check # dgpart timeout with intel
# LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/lib  FC=%{tpls_mpifort}  make %{?_smp_mflags} test


%install
%make_install

%if "%{tpls_libs}" == "shared"
mkdir -p %{buildroot}/%{tpls_prefix}/lib/
install -m 755 ./lib/*.so %{buildroot}/%{tpls_prefix}/lib/
%endif

%files
%{tpls_prefix}/bin/acpl
%{tpls_prefix}/bin/amk_ccc
%{tpls_prefix}/bin/amk_fft2
%{tpls_prefix}/bin/amk_grf
%{tpls_prefix}/bin/amk_hy
%{tpls_prefix}/bin/amk_m2
%{tpls_prefix}/bin/amk_p2
%{tpls_prefix}/bin/atst
%{tpls_prefix}/bin/dggath
%{tpls_prefix}/bin/dgmap
%{tpls_prefix}/bin/dgord
%{tpls_prefix}/bin/dgscat
%{tpls_prefix}/bin/dgtst
%{tpls_prefix}/bin/gbase
%{tpls_prefix}/bin/gcv
%{tpls_prefix}/bin/gmap
%{tpls_prefix}/bin/gmk_hy
%{tpls_prefix}/bin/gmk_m2
%{tpls_prefix}/bin/gmk_m3
%{tpls_prefix}/bin/gmk_msh
%{tpls_prefix}/bin/gmk_ub2
%{tpls_prefix}/bin/gmtst
%{tpls_prefix}/bin/gord
%{tpls_prefix}/bin/gotst
%{tpls_prefix}/bin/gscat
%{tpls_prefix}/bin/gtst
%{tpls_prefix}/bin/mcv
%{tpls_prefix}/bin/mmk_m2
%{tpls_prefix}/bin/mmk_m3
%{tpls_prefix}/bin/mord
%{tpls_prefix}/bin/mtst
%{tpls_prefix}/include/esmumps.h
%{tpls_prefix}/include/ptscotch.h
%{tpls_prefix}/include/ptscotchf.h
%{tpls_prefix}/include/scotch.h
%{tpls_prefix}/include/scotchf.h
%{tpls_prefix}/lib/cmake/scotch/SCOTCHConfig.cmake
%{tpls_prefix}/lib/cmake/scotch/SCOTCHConfigVersion.cmake
%{tpls_prefix}/lib/cmake/scotch/esmumpsTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/esmumpsTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/ptesmumpsTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/ptesmumpsTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotchTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotchTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotcherrTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotcherrTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotcherrexitTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotcherrexitTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotchparmetisTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/ptscotchparmetisTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/scotchTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/scotchTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/scotcherrTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/scotcherrTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/scotcherrexitTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/scotcherrexitTargets.cmake
%{tpls_prefix}/lib/cmake/scotch/scotchmetisTargets-release.cmake
%{tpls_prefix}/lib/cmake/scotch/scotchmetisTargets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libesmumps.a
%{tpls_prefix}/lib/libptesmumps.a
%{tpls_prefix}/lib/libptscotch.a
%{tpls_prefix}/lib/libptscotcherr.a
%{tpls_prefix}/lib/libptscotcherrexit.a
%{tpls_prefix}/lib/libptscotchparmetisv3.a
%{tpls_prefix}/lib/libscotch.a
%{tpls_prefix}/lib/libscotcherr.a
%{tpls_prefix}/lib/libscotcherrexit.a
%{tpls_prefix}/lib/libscotchmetisv3.a
%{tpls_prefix}/lib/libscotchmetisv5.a
%else
%{tpls_prefix}/lib/libesmumps.so
%{tpls_prefix}/lib/libptesmumps.so
%{tpls_prefix}/lib/libptscotch.so
%{tpls_prefix}/lib/libptscotch.so.*
%{tpls_prefix}/lib/libptscotcherr.so
%{tpls_prefix}/lib/libptscotcherrexit.so
%{tpls_prefix}/lib/libptscotchparmetisv3.so
%{tpls_prefix}/lib/libscotch.so
%{tpls_prefix}/lib/libscotch.so.*
%{tpls_prefix}/lib/libscotcherr.so
%{tpls_prefix}/lib/libscotcherrexit.so
%{tpls_prefix}/lib/libscotchmetisv3.so
%{tpls_prefix}/lib/libscotchmetisv5.so
%endif

%{tpls_prefix}/man/man1/acpl.1
%{tpls_prefix}/man/man1/amk_ccc.1
%{tpls_prefix}/man/man1/amk_grf.1
%{tpls_prefix}/man/man1/atst.1
%{tpls_prefix}/man/man1/dgmap.1
%{tpls_prefix}/man/man1/dgord.1
%{tpls_prefix}/man/man1/dgscat.1
%{tpls_prefix}/man/man1/dgtst.1
%{tpls_prefix}/man/man1/gbase.1
%{tpls_prefix}/man/man1/gcv.1
%{tpls_prefix}/man/man1/gdump.1
%{tpls_prefix}/man/man1/gmap.1
%{tpls_prefix}/man/man1/gmk_hy.1
%{tpls_prefix}/man/man1/gmk_m2.1
%{tpls_prefix}/man/man1/gmk_msh.1
%{tpls_prefix}/man/man1/gmtst.1
%{tpls_prefix}/man/man1/gord.1
%{tpls_prefix}/man/man1/gotst.1
%{tpls_prefix}/man/man1/gout.1
%{tpls_prefix}/man/man1/gtst.1
%{tpls_prefix}/man/man1/mcv.1
%{tpls_prefix}/man/man1/mmk_m2.1
%{tpls_prefix}/man/man1/mord.1
%{tpls_prefix}/man/man1/mtst.1

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 7.0.4-1
- Initial Package
