Name:           tpls-%{tpls_flavor}-arpack
Version:        3.9.1
Release:        1%{?dist}
Summary:	    Fortran 77 subroutines for solving large scale eigenvalue problems

License:        BSD
URL:            https://github.com/opencollab/arpack-ng
Source0:       https://src.fedoraproject.org/lookaside/pkgs/arpack/arpack-ng-3.9.1.tar.gz/sha512/1ca590a8c4f75aa74402f9bd62e63851039687f4cb11afa8acb05fce1f22a512bff5fd1709ea85fdbea90b344fbbc01e3944c770b5ddc4d1aabc98ac334f78d2/arpack-ng-3.9.1.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake

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
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
%endif


AutoReqProv:    %{tpls_auto_req_prov}

%description
ARPACK is a collection of Fortran 77 subroutines designed to solve large
scale eigenvalue problems.

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).

%prep
%setup -q -n arpack-ng-%{version}

%build

# Compiler Settings
%{expand: %setup_tpls_env}
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
%if "%{tpls_gpu}" == "lapack"
%if "%{tpls_libs}" == "static"
	-DBLAS_LIBRARIES=%{tpls_blas_static} \
	-DLAPACK_LIBRARIES=%{tpls_lapack_static} \
%else
	-DBLAS_LIBRARIES=%{tpls_blas_shared}  \
	-DLAPACK_LIBRARIES=%{tpls_lapack_shared}  \
%endif
%else
	-DBLAS_LIBRARIES="%{tpls_mkl_linker_flags}" \
	-DLAPACK_LIBRARIES="%{tpls_mkl_linker_flags}" \
%endif
	-DMPI=ON
%make_build

%check
%if "%{tpls_gpu}" == "lapack"
make %{?_smp_mflags} test
%else
LD_LIBRARY_PATH=${LD_LIBRARY_PATH} make %{?_smp_mflags} test
%endif

%install
%make_install


%files
%{tpls_prefix}/include/arpack/arpackdef.h
%{tpls_prefix}/include/arpack/arpackicb.h
%{tpls_prefix}/include/arpack/debug.h
%{tpls_prefix}/include/arpack/debugF90.h
%{tpls_prefix}/include/arpack/stat.h
%{tpls_prefix}/include/arpack/statF90.h
%{tpls_prefix}/lib/cmake/arpackng/arpackng-config-version.cmake
%{tpls_prefix}/lib/cmake/arpackng/arpackng-config.cmake
%{tpls_prefix}/lib/cmake/arpackng/arpackngTargets-release.cmake
%{tpls_prefix}/lib/cmake/arpackng/arpackngTargets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libarpack.a
%{tpls_prefix}/lib/libparpack.a
%else
%{tpls_prefix}/lib/libarpack.so
%{tpls_prefix}/lib/libarpack.so.*
%{tpls_prefix}/lib/libparpack.so
%{tpls_prefix}/lib/libparpack.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/arpack.pc
%{tpls_prefix}/lib/pkgconfig/parpack.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.9.1-1
- Initial Package
