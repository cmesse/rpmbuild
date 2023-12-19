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

# patches for shared library
Patch0:  metis-libmetis.patch
Patch1:  metis-shared-GKlib.patch

# patches for static library
Patch2:  metis-static-GKlib-fixincludes.patch



BuildRequires:  cmake
BuildRequires: help2man
BuildRequires: chrpath
BuildRequires:  pcre2-devel
Requires:       pcre2


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
#%if "%{tpls_libs}" == "shared"
#%patch0 -p1
#%patch1 -p1
#%else
#%patch2 -p1
#%endif

%{expand: %setup_tpls_env}

%{tpls_compilers} make config \
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
make %{?_smp_mflags}

make install DESTDIR=%{buildoot}

cd parmetis-%{parmetis_version}
ln -s $(dirname $(pwd)) METIS
CC=mpicc \
CXX=mpicxx \
CFLAGS="${tpls_coptflags} -I%{tpls_prefix}/include" \
CXXFLAGS="${tpls_cxxoptflags} -I%{tpls_prefix}/include" \
%if "%{tpls_libs}" == "static"
LDFLAGS="%{tpls_prefix}/lib/libmpi.a" \
%else
LDFLAGS="%{tpls_prefix}/lib/libmpi.so %{tpls_ldflags} %{tpls_rpath}" \
%endif
%{tpls_compilers} cmake \
	-DGKLIB_PATH=$(dirname $(pwd))/GKlib \
	-DMETIS_PATH=$(dirname $(pwd)) \
	-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
	-DOPENMP=ON \
	.

make %{?_smp_mflags}

# manually create the shared file
%{tpls_cc} -shared -o ./libparmetis/libparmetis.so libparmetis/CMakeFiles/parmetis.dir/*.o


%install
%make_install


cd parmetis-%{parmetis_version}
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
%{tpls_prefix}/libparmetis.a
%else
%{tpls_prefix}/lib/libparmetis.so
%endif


%changelog
* Mon Dec 18 2023 Christian Messe <cmesse@lbl.gov> - 5.1.0-1
- Initial Package

