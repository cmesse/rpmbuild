Name:           tpls-%{tpls_flavor}-arpack
Version:        3.9.1
Release:        1%{?dist}
Summary:	    Fortran 77 subroutines for solving large scale eigenvalue problems

License:        BSD
URL:            https://github.com/opencollab/arpack-ng
Source0:        arpack-ng-%{version}.tar.gz 



%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
%endif

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
echo PWD
pwd

%if "%{tpls_compiler}" == "intel"
if [ "$SETVARS_COMPLETED" != "1" ]; then
	source /opt/intel/oneapi/setvars.sh intel64
fi
%elif "%{tpls_gpu}" != "lapack"
if [ "$SETVARS_COMPLETED" != "1" ]; then
	source /opt/intel/oneapi/setvars.sh intel64
fi
%endif


CC=%{tpls_cc} \
CXX=%{tpls_cxx} \
FC=%{tpls_fc} \
CFLAGS="%{tpls_coptflags}" \
CXXFLAGS="%{tpls_coptflags}" \
FCFLAGS="%{tpls_coptflags}" \
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
%{tpls_prefix}/lib64/libarpack.so
%{tpls_prefix}/lib64/libarpack.so.2
%{tpls_prefix}/lib64/libarpack.so.2.1.0
%{tpls_prefix}/lib64/pkgconfig/arpack.pc

%changelog
* Thu Dec 14 2023 Christian Messe <cmesse@lbl.gov> - 3.9.1-1
- Initial package.
