%global metis_version 5.1.0
%global parmetis_version 4.0.3
%define scls_oflags -O2

Name:           scls-%{scls_flavor}-metis
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

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires: help2man
BuildRequires: chrpath
BuildRequires:  pcre2-devel
Requires:       pcre2

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%description
METIS is a set of serial programs for partitioning graphs, 
partitioning finite element meshes, and producing fill reducing 
orderings for sparse matrices. 
The algorithms implemented in METIS are based on the multilevel 
recursive-bisection, multilevel k-way, and multi-constraint 
partitioning schemes developed in our lab.
METIS is distributed with OpenMP support.

%package -n scls-%{scls_flavor}-parmetis
Release:        1%{?dist}
Version:        %{parmetis_version}
License:        ASL 2.0 and BSD and LGPLv2+
Summary:        ParMETIS - Parallel Graph Partitioning and Fill-reducing Matrix Ordering
Requires:       scls-%{scls_flavor}-metis == %{metis_version}


%description  -n scls-%{scls_flavor}-parmetis
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
%if "%{scls_index_sizesize}" == "64"
%patch0 -p1
%endif

#%if "%{scls_libs}" == "shared"
#%patch1 -p1
#%patch2 -p1
#%else
#%patch3 -p1
#%endif


%{expand: %setup_scls_env}

make config \
    prefix=%{scls_prefix} \
    debug=0 \
    assert=0 \
    assert2=0 \
    gdb=0 \
    gprof=0 \
    openmp=1 \
%if "%{scls_libs}" == "static"
    shared=0 \
%else
    shared=1 \
%endif


%build

pushd build/Linux-x86_64

CC=%{scls_mpicc} \
CXX=%{scls_mpicxx} \
FC=%{scls_mpifort} \
%{scls_cmake} . \
	-DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags}}" \
    -DCMAKE_Fortran_COMPILER=%{scls_fc} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DSHARED=OFF \
    -DCMAKE_C_FLAGS_RELEASE="-DNDEBUG %{scls_oflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE="-DNDEBUG %{scls_oflags}" \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DSHARED=ON \
    -DCMAKE_C_FLAGS_RELEASE="-fPIC -DNDEBUG %{scls_oflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE="-fPIC -DNDEBUG %{scls_oflags}" \
%if "%{scls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif
%endif
	-DOPENMP=ON
popd

pushd parmetis-%{parmetis_version}

ln -s $(dirname $(pwd)) METIS

%{scls_env} \
CC=%{scls_mpicc} \
CXX=%{scls_mpicxx} \
FC=%{scls_mpifort} \
%if "%{scls_mpi}" == "openmpi"
%if "%{scls_libs}" == "static"
LDFLAGS="%{scls_prefix}/lib/libmpi.a" \
%else
LDFLAGS="%{scls_prefix}/lib/libmpi.so %{scls_ldflags}" \
%endif
%endif
%if "%{scls_mpi}" == "intelmpi"
%if "%{scls_libs}" == "static"
LDFLAGS="${I_MPI_ROOT}/lib/libmpi.a %{scls_ldflags}" \
%else
LDFLAGS="${I_MPI_ROOT}/lib/libmpi.so %{scls_ldflags}" \
%endif
%endif
%{scls_cmake} . \
    -DCMAKE_C_FLAGS="%{scls_cflags} -DNDEBUG" \
    -DCMAKE_C_FLAGS_RELEASE="%{scls_cflags} -DNDEBUG %{scls_oflags}" \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} -DNDEBUG %{scls_oflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{scls_cxxflags} -DNDEBUG %{scls_oflags}" \
	-DGKLIB_PATH=$(dirname $(pwd))/GKlib \
	-DMETIS_PATH=$(dirname $(pwd)) \
	-DOPENMP=ON \
%if "%{scls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%endif


make %{?_smp_mflags}

# manually create the shared file
%{scls_cc} -shared -o ./libparmetis/libparmetis.so libparmetis/CMakeFiles/parmetis.dir/*.o

%install

%make_install

pushd parmetis-%{parmetis_version}
%make_install

%if "%{scls_libs}" == "shared"
install -m 755 ./libparmetis/libparmetis.so %{buildroot}/%{scls_prefix}/lib
rm -v %{buildroot}/%{scls_prefix}/lib/libparmetis.a
%endif

%{scls_remove_la_files}

%files
%{scls_prefix}/bin/cmpfillin
%{scls_prefix}/bin/gpmetis
%{scls_prefix}/bin/graphchk
%{scls_prefix}/bin/m2gmetis
%{scls_prefix}/bin/mpmetis
%{scls_prefix}/bin/ndmetis
%{scls_prefix}/include/metis.h
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libmetis.a
%else
%{scls_prefix}/lib/libmetis.so
%endif

%files -n scls-%{scls_flavor}-parmetis
%{scls_prefix}/bin/mtest
%{scls_prefix}/bin/parmetis
%{scls_prefix}/bin/pometis
%{scls_prefix}/bin/ptest
%{scls_prefix}/include/parmetis.h
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libparmetis.a
%else
%{scls_prefix}/lib/libparmetis.so
%endif


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 5.1.0-1
- Initial Package

