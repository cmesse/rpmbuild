%global metis_version 5.1.0
%global parmetis_version 4.0.3

Name:           tpls-%{tpls_flavor}-metis
Version:        %{metis_version}
Release:        1%{?dist}
Summary:        Serial Graph Partitioning and Fill-reducing Matrix Ordering

License:        ASL 2.0 and BSD and LGPLv2+
URL:            http://glaros.dtc.umn.edu/gkhome/views/metis
Source0:        http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-%{version}.tar.gz
Source1:        http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/parmetis-%{parmetis_version}.tar.gz

# patch for 64 bit integers
Patch0: metis-width-datatype.patch 

# patches for shared library
Patch1:  metis-libmetis.patch
Patch2:  metis-shared-GKlib.patch

# patches for static library
Patch3:  metis-static-GKlib-fixincludes.patch



BuildRequires:  cmake
BuildRequires: help2man
BuildRequires: chrpath
BuildRequires:  pcre2-devel
Requires:       pcre2
AutoReqProv:   %{tpls_auto_req_prov}

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

AutoReqProv:    %{tpls_auto_req_prov}

%description
METIS is a set of serial programs for partitioning graphs, 
partitioning finite element meshes, and producing fill reducing 
orderings for sparse matrices. 
The algorithms implemented in METIS are based on the multilevel 
recursive-bisection, multilevel k-way, and multi-constraint 
partitioning schemes developed in our lab.
METIS is distributed with OpenMP support.

%package -n tpls-%{tpls_flavor}-parmetis
Release:        1%{?dist}
Version:        %{parmetis_version}
License:        ASL 2.0 and BSD and LGPLv2+
Summary:        ParMETIS - Parallel Graph Partitioning and Fill-reducing Matrix Ordering
Requires:       tpls-%{tpls_flavor}-metis == %{metis_version}
AutoReqProv:   %{tpls_auto_req_prov}

%description  -n tpls-%{tpls_flavor}-parmetis
ParMETIS is an MPI-based parallel library that implements a variety of
algorithms for partitioning unstructured graphs, meshes, and for
computing fill-reducing orderings of sparse matrices. ParMETIS extends
the functionality provided by METIS and includes routines that are
especially suited for parallel AMR computations and large scale
numerical simulations. The algorithms implemented in ParMETIS are
based on the parallel multilevel k-way graph-partitioning, adaptive
repartitioning, and parallel multi-constrained partitioning schemes
developed at the Karzpis Lab, University of Minesota.

%prep

%setup -q -n metis-%{metis_version}
tar xvf %{SOURCE1}
%if "%{tpls_intsize}" == "64"
%patch0 -p1
%endif

#%if "%{tpls_libs}" == "shared"
#%patch1 -p1
#%patch2 -p1
#%else
#%patch3 -p1
#%endif


%{setup_tpls_env}

make config \
    prefix=%{tpls_prefix} \
    debug=0 \
    assert=0 \
    assert2=0 \
    gdb=0 \
    gprof=0 \
    openmp=1 \
%if "%{tpls_libs}" == "static"
    shared=0 \
%else
    shared=1 \
%endif


%build

pushd build/Linux-x86_64

%{tpls_compilers} cmake \
%if "%{tpls_libs}" == "static"
    -DCMAKE_C_FLAGS="%{tpls_cflags} -DNDEBUG" \
    -DCMAKE_C_FLAGS_RELEASE="%{tpls_cflags} -DNDEBUG" \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -DNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{tpls_cxxflags} -DNDEBUG" \
%else
    -DCMAKE_C_FLAGS="%{tpls_cflags} -fPIC -DNDEBUG" \
    -DCMAKE_C_FLAGS_RELEASE="%{tpls_cflags}  -fPIC -DNDEBUG" \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -fPIC -DNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{tpls_cxxflags} -fPIC -DNDEBUG" \
%endif
	-DOPENMP=ON \
	.
popd

pushd parmetis-%{parmetis_version}

ln -s $(dirname $(pwd)) METIS

CC=%{tpls_mpicc} \
CXX=%{tpls_mpicxx} \
FC=%{tpls_mpifort} \
%if "%{tpls_libs}" == "static"
LDFLAGS="%{tpls_prefix}/lib/libmpi.a" \
%else
LDFLAGS="%{tpls_prefix}/lib/libmpi.so %{tpls_ldflags}" \
%endif
cmake \
    -DCMAKE_C_FLAGS="%{tpls_cflags} -DNDEBUG" \
    -DCMAKE_C_FLAGS_RELEASE="%{tpls_cflags} -DNDEBUG" \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -DNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{tpls_cxxflags} -DNDEBUG" \
	-DGKLIB_PATH=$(dirname $(pwd))/GKlib \
	-DMETIS_PATH=$(dirname $(pwd)) \
	-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
	-DOPENMP=ON \
	.
popd

make %{?_smp_mflags}

pushd parmetis-%{parmetis_version}
make %{?_smp_mflags}

# manually create the shared file
%{tpls_cc} -shared -o ./libparmetis/libparmetis.so libparmetis/CMakeFiles/parmetis.dir/*.o
popd



%install

%make_install

pushd parmetis-%{parmetis_version}
%make_install

%if "%{tpls_libs}" == "shared"
install -m 755 ./libparmetis/libparmetis.so %{buildroot}/%{tpls_prefix}/lib
rm -v %{buildroot}/%{tpls_prefix}/lib/libparmetis.a
%endif

%{tpls_remove_la_files}

%files
%{tpls_prefix}/bin/cmpfillin
%{tpls_prefix}/bin/gpmetis
%{tpls_prefix}/bin/graphchk
%{tpls_prefix}/bin/m2gmetis
%{tpls_prefix}/bin/mpmetis
%{tpls_prefix}/bin/ndmetis
%{tpls_prefix}/include/metis.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libmetis.a
%else
%{tpls_prefix}/lib/libmetis.so
%endif

%files -n tpls-%{tpls_flavor}-parmetis
%{tpls_prefix}/bin/mtest
%{tpls_prefix}/bin/parmetis
%{tpls_prefix}/bin/pometis
%{tpls_prefix}/bin/ptest
%{tpls_prefix}/include/parmetis.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libparmetis.a
%else
%{tpls_prefix}/lib/libparmetis.so
%endif


%changelog
* Tue Dec 19 2023 Christian Messe <cmesse@lbl.gov> - 5.1.0-1
- Initial Package

