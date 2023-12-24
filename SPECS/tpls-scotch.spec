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

cmake \
 	 -DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
 	 -DBUILD_LIBESMUMPS=ON \
 	 -DBUILD_LIBSCOTCHMETIS=ON \
 	 -DBUILD_PTSCOTCH=ON \
 	 -DCMAKE_BUILD_TYPE=Release \
 	 -DINTSIZE=%{tpls_int} \
 	 -DCMAKE_C_COMPILER=%{tpls_mpicc} \
 	 -DCMAKE_C_FLAGS="%{tpls_cflags}" \
 	 -DCMAKE_C_FLAGS_RELEASE=-DNDEBUG \
 	 -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	 -DCMAKE_CXX_COMPILER=%{tpls_mpicxx} \
 	 -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
 	 -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
 	 -DCMAKE_Fortran_COMPILER="%{tpls_mpifort}" \
 	 -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
 	 -DCMAKE_Fortran_FLAGS_RELEASE=-DNDEBUG \
 	 -DINSTALL_METIS_HEADERS=OFF \
 	 -DMPIEXEC_MAX_NUMPROCS=%{tpls_maxprocs}
	
#%make_build
%make_build

# build the static libraries
%if "%{tpls_libs}" == "shared"
echo "Building shared libraries"

for l in esmumps ptesmumps; do
    %{tpls_mpicc} -shared -o ./lib/lib${l}.so ./src/esmumps/CMakeFiles/${l}.dir/*.o
done

for l in ptscotch ptscotcherr ptscotcherrexit scotch scotcherr scotcherrexit; do
    echo $l 
    %{tpls_mpicc} -shared -o ./lib/lib${l}.so ./src/libscotch/CMakeFiles/${l}.dir/*.o
done

for l in ptscotchparmetisv3 scotchmetisv3 scotchmetisv5; do
    %{tpls_mpicc} -shared -o ./lib/lib${l}.so ./src/libscotchmetis/CMakeFiles/${l}.dir/*.o
done

%endif


#%check
cd src
LD_LIBRARY_PATH=$(dirname $(pwd))/lib  FC=%{tpls_fc}  make %{?_smp_mflags} check


%install
%if "%{tpls_libs}" == "shared"
mkdir -p %{buildroot}/%{tpls_prefix}/lib/
install -m 755 ./lib/*.so %{buildroot}/%{tpls_prefix}/lib/
%endif

cd src
%make_install

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
%exclude %{tpls_prefix}/lib/libesmumps.a
%exclude %{tpls_prefix}/lib/libptesmumps.a
%exclude %{tpls_prefix}/lib/libptscotch.a
%exclude %{tpls_prefix}/lib/libptscotcherr.a
%exclude %{tpls_prefix}/lib/libptscotcherrexit.a
%exclude %{tpls_prefix}/lib/libptscotchparmetisv3.a
%exclude %{tpls_prefix}/lib/libscotch.a
%exclude %{tpls_prefix}/lib/libscotcherr.a
%exclude %{tpls_prefix}/lib/libscotcherrexit.a
%exclude %{tpls_prefix}/lib/libscotchmetisv3.a
%exclude %{tpls_prefix}/lib/libscotchmetisv5.a
%{tpls_prefix}/lib/libesmumps.so
%{tpls_prefix}/lib/libptesmumps.so
%{tpls_prefix}/lib/libptscotch.so
%{tpls_prefix}/lib/libptscotcherr.so
%{tpls_prefix}/lib/libptscotcherrexit.so
%{tpls_prefix}/lib/libptscotchparmetisv3.so
%{tpls_prefix}/lib/libscotch.so
%{tpls_prefix}/lib/libscotcherr.so
%{tpls_prefix}/lib/libscotcherrexit.so
%{tpls_prefix}/lib/libscotchmetisv3.so
%{tpls_prefix}/lib/libscotchmetisv5.so
%endif
%changelog
* Mon Dec 18 2023 Christian Messe <cmesse@lbl.gov> - 7.0.4-1
- Initial Package
