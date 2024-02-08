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

Patch4:         scotch-shared.patch

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

%if "%{scls_libs}" == "shared"
%patch4 -p1
%endif

%build

%{expand: %setup_scls_env}

pwd

%{scls_env} \
%{scls_cmake} \
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
 	-DCMAKE_C_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
 	-DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	-DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
%if "%{scls_compiler}" != "intel"
 	-DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
 	-DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
 	-DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
%elif "%{scls_libs}" == "static"
 	-DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
 	-DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
 	-DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
%else
 	-DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags} -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id" \
 	-DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags} -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id" \
 	-DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags} -Wl,-rpath,${scls_prefix}/lib -Wl,--build-id" \
%endif
 	-DCMAKE_Fortran_FLAGS_RELEASE=-DNDEBUG \
 	-DINSTALL_METIS_HEADERS=OFF \
 	-DMPIEXEC_MAX_NUMPROCS=%{scls_maxprocs} \
 	-DMPIEXEC_EXECUTABLE=%{scls_prefix}/bin/mpiexec \
 	-DTHREADS=OFF \
 	-DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
%if "%{scls_index_size}" == "32"
	-DINTSIZE=32 \
%else
	-DINTSIZE=64 \
%endif
%if "%{scls_libs}" == "shared"
%if "%{scls_math}" == "lapack"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%endif
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib" \
%endif
%endif
    .

%make_build



%check
LD_LIBRARY_PATH=$(pwd)/lib:%{scls_ld_library_path} make %{?_smp_mflags} test

%install
%make_install

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
