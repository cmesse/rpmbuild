Name:           tpls-%{tpls_flavor}-scalapack
Version:        2.2.0
Release:        1%{?dist}
Summary:        A subset of LAPACK routines redesigned for heterogeneous computing

License:        Public Domain
URL:            http://www.netlib.org/scalapack/
Source0:        https://github.com/Reference-ScaLAPACK/scalapack/archive/refs/tags/v%{version}.tar.gz

Patch1: scalapack-2.2-fix-version.patch
Patch2: scalapack-2.2-set-CMAKE_POSITION_INDEPENDENT_CODE.patch
Patch3: scalapack-2.2.0-fix57.patch
Patch4: scalapack-cblas.patch
#Patch5: scalapack-mpi.patch

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
%endif

%if   "%{tpls_mpi}" == "openmpi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%endif

%description
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

%prep

%setup -q -n scalapack-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch5 -p1

%build

%{expand: %setup_tpls_env}

CC=%{tpls_prefix}/bin/mpicc \
FC=%{tpls_prefix}/bin/mpifort \
 cmake \
	-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
	-DMPI_BASE_DIR=%{tpls_prefix} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
	-DCMAKE_Fortran_FLAGS="%{tpls_fcflags} -fallow-argument-mismatch" \
%if "%{tpls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%endif
%if "%{tpls_gpu}" == "lapack"
	-DBLAS_LIBRARIES=%{tpls_blas} \
	-DLAPACK_LIBRARIES=%{tpls_lapack} \
	-DUSE_OPTIMIZED_LAPACK_BLAS=OFF \
%else
	-DBLAS_LIBRARIES="%{tpls_mkl_linker_flags}" \
	-DLAPACK_LIBRARIES="%{tpls_mkl_linker_flags}" \
%endif
    -DSCALAPACK_BUILD_TESTS=OFF \
    .

%make_build

# not doing tests as they fail on many machines
#%check
#make test
 
%install
%make_install

%files
%{tpls_prefix}/lib/cmake/scalapack-%{version}/scalapack-config-version.cmake
%{tpls_prefix}/lib/cmake/scalapack-%{version}/scalapack-config.cmake
%{tpls_prefix}/lib/cmake/scalapack-%{version}/scalapack-targets-noconfig.cmake
%{tpls_prefix}/lib/cmake/scalapack-%{version}/scalapack-targets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libscalapack.a
%exclude %{tpls_prefix}/lib/libblas.a
%exclude %{tpls_prefix}/lib/liblapack.a

%else
%{tpls_prefix}/lib/libscalapack.so
%{tpls_prefix}/lib/libscalapack.so.*
%exclude %{tpls_prefix}/lib/libblas.so
%exclude %{tpls_prefix}/lib/liblapack.so
%endif
%{tpls_prefix}/lib/pkgconfig/scalapack.pc


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.2.0-1
- Initial package.
