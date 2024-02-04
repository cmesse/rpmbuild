%define scls_oflags -O3

Name:           scls-%{scls_flavor}-scalapack
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

%if "%{scls_math}" == "lapack"
BuildRequires:  scls-%{scls_flavor}-blas
BuildRequires:  scls-%{scls_flavor}-lapack
Requires:       scls-%{scls_flavor}-blas
Requires:       scls-%{scls_flavor}-lapack
%endif

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%if "%{scls_math}" != "lapack"
BuildRequires: intel-oneapi-mkl
BuildRequires: intel-oneapi-mkl-devel
Requires:      intel-oneapi-mkl
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

%{expand: %setup_scls_env}

CC=%{scls_prefix}/bin/mpicc \
FC=%{scls_prefix}/bin/mpifort \
 cmake \
	-DCMAKE_INSTALL_PREFIX=%{scls_prefix} \
	-DMPI_BASE_DIR=%{scls_prefix} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
	-DCMAKE_Fortran_FLAGS="%{scls_fcflags} -fallow-argument-mismatch %{scls_oflags}" \
%if "%{scls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%endif
%if "%{scls_math}" == "lapack"
	-DBLAS_LIBRARIES=%{scls_blas} \
	-DLAPACK_LIBRARIES=%{scls_lapack} \
	-DUSE_OPTIMIZED_LAPACK_BLAS=OFF \
%else
	-DBLAS_LIBRARIES="%{scls_mkl_linker_flags}" \
	-DLAPACK_LIBRARIES="%{scls_mkl_linker_flags}" \
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
%{scls_prefix}/lib/cmake/scalapack-%{version}/scalapack-config-version.cmake
%{scls_prefix}/lib/cmake/scalapack-%{version}/scalapack-config.cmake
%{scls_prefix}/lib/cmake/scalapack-%{version}/scalapack-targets-noconfig.cmake
%{scls_prefix}/lib/cmake/scalapack-%{version}/scalapack-targets.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libscalapack.a
%exclude %{scls_prefix}/lib/libblas.a
%exclude %{scls_prefix}/lib/liblapack.a

%else
%{scls_prefix}/lib/libscalapack.so
%{scls_prefix}/lib/libscalapack.so.*
%exclude %{scls_prefix}/lib/libblas.so
%exclude %{scls_prefix}/lib/liblapack.so
%endif
%{scls_prefix}/lib/pkgconfig/scalapack.pc


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.2.0-1
- Initial package.
