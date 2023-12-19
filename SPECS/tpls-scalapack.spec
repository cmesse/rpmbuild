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

BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-openmpi

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

%{expand: %error_if_not_lapack}

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
    -DCMAKE_C_FLAGS="%{tpls_coptflags}" \
	-DCMAKE_Fortran_FLAGS="%{tpls_foptflags} -fallow-argument-mismatch" \
%if "%{tpls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \	
	-DBUILD_SHARED_LIBS=OFF \
	-DBLAS_LIBRARIES=%{tpls_blas_static} \
	-DLAPACK_LIBRARIES=%{tpls_lapack_static} \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBLAS_LIBRARIES=%{tpls_blas_shared} \
	-DLAPACK_LIBRARIES=%{tpls_lapack_shared} \
%endif
	-DUSE_OPTIMIZED_LAPACK_BLAS=OFF \
    -DBUILD_TESTING=OFF

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
%else
%{tpls_prefix}/lib/libscalapack.so
%{tpls_prefix}/lib/libscalapack.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/scalapack.pc


%changelog
* Thu Dec 14 2023 Christian Messe <cmesse@lbl.gov> - 2.2.0-1
- Initial package.
