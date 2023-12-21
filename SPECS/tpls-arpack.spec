Name:           tpls-%{tpls_flavor}-arpack
Version:        3.9.1
Release:        1%{?dist}
Summary:	    Fortran 77 subroutines for solving large scale eigenvalue problems

License:        BSD
URL:            https://github.com/opencollab/arpack-ng
Source0:       https://src.fedoraproject.org/lookaside/pkgs/arpack/arpack-ng-3.9.1.tar.gz/sha512/1ca590a8c4f75aa74402f9bd62e63851039687f4cb11afa8acb05fce1f22a512bff5fd1709ea85fdbea90b344fbbc01e3944c770b5ddc4d1aabc98ac334f78d2/arpack-ng-3.9.1.tar.gz

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
%end


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

pwd

CC=%{tpls_mpicc} \
CXX=%{tpls_mpicxx} \
FC=%{tpls_mpifort} \
CFLAGS="%{tpls_cflags}" \
CXXFLAGS="%{tpls_cflags}" \
FCFLAGS="%{tpls_cflags}" \
cmake \
	-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
%if "%{tpls_gpu}" == "lapack"
%if "%{tpls_libs}" == "static"
	-DBLAS_LIBRARIES=%{tpls_blas_static} \
	-DLAPACK_LIBRARIES=%{tpls_lapack_static} \
%else
	-DBLAS_LIBRARIES=%{tpls_blas_shared}  \
	-DLAPACK_LIBRARIES=%{tpls_lapack_shared}  \
%endif
%else
%if "%{tpls_libs}" == "static"
	-DBLAS_LIBRARIES="%{tpls_mkl_static}" \
	-DLAPACK_LIBRARIES="%{tpls_mkl_static}" \
%else
	-DBLAS_LIBRARIES="%{tpls_mkl_shared}" \
	-DLAPACK_LIBRARIES="%{tpls_mkl_shared}" \
%endif
	-DCMAKE_INSTALL_LIBDIR=lib \
	-DMPI=ON
%endif
.

%make_build

%check
%if "%{tpls_gpu}" == "lapack"
make %{?_smp_mflags} test
%else
LD_LIBRARY_PATH=%{tpls_mklroot}/lib make %{?_smp_mflags} test
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
%{tpls_prefix}/lib64/cmake/arpackng/arpackng-config-version.cmake
%{tpls_prefix}/lib64/cmake/arpackng/arpackng-config.cmake
%{tpls_prefix}/lib64/cmake/arpackng/arpackngTargets-release.cmake
%{tpls_prefix}/lib64/cmake/arpackng/arpackngTargets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib64/libarpack.a
%else
%{tpls_prefix}/lib64/libarpack.so
%{tpls_prefix}/lib64/libarpack.so.*
%endif
%{tpls_prefix}/lib64/pkgconfig/arpack.pc

%changelog
* Tue Dec 19 2023 Christian Messe <cmesse@lbl.gov> - 3.9.1-1
- Initial Package
