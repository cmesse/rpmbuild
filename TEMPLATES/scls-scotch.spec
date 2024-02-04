%define scls_oflags -O2

Name:           scls-%{scls_flavor}-scotch
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


BuildRequires:  %{scls_rpm_cc}  >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_fc}  >= %{scls_comp_minver}
BuildRequires: make
BuildRequires: flex
BuildRequires: bison
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%if "%{scls_math}" == "lapack"
BuildRequires:  scls-%{scls_flavor}-scalapack
%endif




%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch libraries are packaged in the


%prep
%setup -q -n scotch-v%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%{expand: %setup_scls_env}

pwd

%{scls_env} \
CC=%{scls_mpicc} \
CXX=%{scls_mpicxx} \
FC=%{scls_mpifort} \
%{scls_cmake} . \
%if "%{scls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%endif
 	-DBUILD_LIBESMUMPS=ON \
 	-DBUILD_LIBSCOTCHMETIS=OFF \
 	-DBUILD_PTSCOTCH=ON \
 	-DINTSIZE=%{scls_index_size} \
 	-DCMAKE_C_COMPILER=%{scls_mpicc} \
 	-DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
 	-DCMAKE_C_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
 	-DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
 	-DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
 	-DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
 	-DCMAKE_Fortran_FLAGS_RELEASE=-DNDEBUG \
 	-DINSTALL_METIS_HEADERS=OFF \
 	-DMPIEXEC_MAX_NUMPROCS=%{scls_maxprocs} \
 	-DTHREADS=OFF \
%if "%{scls_index_size}" == "32"
	-DINTSIZE=32 \
%else
	-DINTSIZE=64 \
%endif
%if "%{scls_libs}" == "shared"
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath,${I_MPI_ROOT}/lib -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id" \
%if "%{scls_mpi}" == "intelmpi"
 	-DCMAKE_SHARED_LINKER_FLAGS="-Wl,-rpath,${I_MPI_ROOT}/lib -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id"
%else
 	-DCMAKE_SHARED_LINKER_FLAGS="-Wl,-rpath,${scls_prefix}/lib -Wl,--build-id"
%endif
%endif

%make_build

# build the static libraries
%if "%{scls_libs}" == "shared"
echo "Building shared libraries"

# Loop for building esmumps and ptesmumps libraries
for l in esmumps ptesmumps; do
    echo "Building lib${l}.so"
    # Compile and link the library
    %{scls_mpicc} -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id -shared -o ./lib/lib${l}.so ./src/esmumps/CMakeFiles/${l}.dir/*.o
done

# Loop for building ptscotch libraries
for l in ptscotch ptscotcherr ptscotcherrexit scotch scotcherr scotcherrexit; do
    echo "Building lib${l}.so"
    # Compile and link the library
    %{scls_mpicc} -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id -shared -o ./lib/lib${l}.so ./src/libscotch/CMakeFiles/${l}.dir/*.o
done

# Loop for building scotchmetis libraries
#for l in ptscotchparmetisv3 scotchmetisv3 scotchmetisv5; do
#    echo "Building lib${l}.so"
#    # Compile and link the library
#    %{scls_mpicc} -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id -shared -o ./lib/lib${l}.so ./src/libscotchmetis/CMakeFiles/${l}.dir/*.o
#done

%endif


# dgpart timeout
%check
%if "%{scls_compiler}" == "gnu"
%make_build test
%else
 LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/lib  FC=%{scls_mpifort}  make %{?_smp_mflags} test
%endif


%install
%make_install

%if "%{scls_libs}" == "shared"
mkdir -p %{buildroot}/%{scls_prefix}/lib/
install -m 755 ./lib/*.so %{buildroot}/%{scls_prefix}/lib/
%endif

%files
%{scls_prefix}/bin/acpl
%{scls_prefix}/bin/amk_ccc
%{scls_prefix}/bin/amk_fft2
%{scls_prefix}/bin/amk_grf
%{scls_prefix}/bin/amk_hy
%{scls_prefix}/bin/amk_m2
%{scls_prefix}/bin/amk_p2
%{scls_prefix}/bin/atst
%{scls_prefix}/bin/dggath
%{scls_prefix}/bin/dgmap
%{scls_prefix}/bin/dgord
%{scls_prefix}/bin/dgscat
%{scls_prefix}/bin/dgtst
%{scls_prefix}/bin/gbase
%{scls_prefix}/bin/gcv
%{scls_prefix}/bin/gmap
%{scls_prefix}/bin/gmk_hy
%{scls_prefix}/bin/gmk_m2
%{scls_prefix}/bin/gmk_m3
%{scls_prefix}/bin/gmk_msh
%{scls_prefix}/bin/gmk_ub2
%{scls_prefix}/bin/gmtst
%{scls_prefix}/bin/gord
%{scls_prefix}/bin/gotst
%{scls_prefix}/bin/gscat
%{scls_prefix}/bin/gtst
%{scls_prefix}/bin/mcv
%{scls_prefix}/bin/mmk_m2
%{scls_prefix}/bin/mmk_m3
%{scls_prefix}/bin/mord
%{scls_prefix}/bin/mtst
%{scls_prefix}/include/esmumps.h
%{scls_prefix}/include/ptscotch.h
%{scls_prefix}/include/ptscotchf.h
%{scls_prefix}/include/scotch.h
%{scls_prefix}/include/scotchf.h
%{scls_prefix}/lib/cmake/scotch
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libesmumps.a
%{scls_prefix}/lib/libptesmumps.a
%{scls_prefix}/lib/libptscotch.a
%{scls_prefix}/lib/libptscotcherr.a
%{scls_prefix}/lib/libptscotcherrexit.a
%{scls_prefix}/lib/libscotch.a
%{scls_prefix}/lib/libscotcherr.a
%{scls_prefix}/lib/libscotcherrexit.a
%else
%{scls_prefix}/lib/libesmumps.so
%{scls_prefix}/lib/libptesmumps.so
%{scls_prefix}/lib/libptscotch.so
%{scls_prefix}/lib/libptscotch.so.*
%{scls_prefix}/lib/libptscotcherr.so
%{scls_prefix}/lib/libptscotcherrexit.so
%{scls_prefix}/lib/libscotch.so
%{scls_prefix}/lib/libscotch.so.*
%{scls_prefix}/lib/libscotcherr.so
%{scls_prefix}/lib/libscotcherrexit.so
%endif
%{scls_prefix}/man/man1/acpl.1
%{scls_prefix}/man/man1/amk_ccc.1
%{scls_prefix}/man/man1/amk_grf.1
%{scls_prefix}/man/man1/atst.1
%{scls_prefix}/man/man1/dgmap.1
%{scls_prefix}/man/man1/dgord.1
%{scls_prefix}/man/man1/dgscat.1
%{scls_prefix}/man/man1/dgtst.1
%{scls_prefix}/man/man1/gbase.1
%{scls_prefix}/man/man1/gcv.1
%{scls_prefix}/man/man1/gdump.1
%{scls_prefix}/man/man1/gmap.1
%{scls_prefix}/man/man1/gmk_hy.1
%{scls_prefix}/man/man1/gmk_m2.1
%{scls_prefix}/man/man1/gmk_msh.1
%{scls_prefix}/man/man1/gmtst.1
%{scls_prefix}/man/man1/gord.1
%{scls_prefix}/man/man1/gotst.1
%{scls_prefix}/man/man1/gout.1
%{scls_prefix}/man/man1/gtst.1
%{scls_prefix}/man/man1/mcv.1
%{scls_prefix}/man/man1/mmk_m2.1
%{scls_prefix}/man/man1/mord.1
%{scls_prefix}/man/man1/mtst.1

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 7.0.4-1
- Initial Package
