
Summary: Numerical linear algebra package libraries
Name: tpls-%{tpls_flavor}-lapack
Version: 3.12.0
Release: 1%{?dist}
License: BSD
URL: http://www.netlib.org/lapack/
Source0: https://github.com/Reference-LAPACK/lapack/archive/v%{version}.tar.gz

BuildRequires:  %{tpls_rpm_fc}  >= %{tpls_comp_minver}

BuildRequires: gawk
BuildRequires: make
BuildRequires: tpls-%{tpls_flavor}-cmake

Requires:      %{tpls_rpm_fc}  >= %{tpls_comp_minver}
Requires:      tpls-%{tpls_flavor}-blas

%description
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran90 and built with gcc.
}


%package -n tpls-%{tpls_flavor}-blas
Summary: The Basic Linear Algebra Subprograms library

%description -n tpls-%{tpls_flavor}-blas
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra.


%package -n tpls-%{tpls_flavor}-cblas
Summary:        C interfaces for BLAS
Requires:       tpls-%{tpls_flavor}-blas

%description  -n tpls-%{tpls_flavor}-cblas
CBLAS, the C interface to the Basic Linear Algebra Subprograms (BLAS), 
is a standardized set of low-level routines that provide efficient
linear algebra operations, primarily for vector and matrix calculations.
Originally developed in FORTRAN for use in high-performance computing
BLAS has been fundamental in scientific computing and forms the backbone
of many complex numerical computing tasks. 
CBLAS is a C language interface to the BLAS library.

%package -n tpls-%{tpls_flavor}-lapacke
Requires:       tpls-%{tpls_flavor}-lapack  = %{version}
Summary: C Interface to Linear Algebra Package (LAPACK)

%description -n tpls-%{tpls_flavor}-lapacke
LAPACKE is the C language interface to the widely-used LAPACK library,
which is renowned for its comprehensive collection of algorithms for
solving various linear algebra problems. Originally developed for
Fortran, LAPACK's capabilities are essential in numerous scientific and
engineering applications, ranging from solving systems of linear equations
to eigenvalue problems and matrix factorizations.

LAPACKE provides a seamless and straightforward way for C and C++
programmers to integrate these powerful LAPACK routines into their
applications. It simplifies the process of calling LAPACK functions
from C/C++ code by handling the differences between the Fortran and
C calling conventions and data representations.

%prep

if [ "%{tpls_gpu}" != "lapack" ] || [ "%{tpls_compiler}" != "gnu" ]; then
    echo "Error: We only want to compile this library for tpls-gnu-lapack-* flavors!"
    exit 1
fi


%setup -q -n lapack-%{version}

%build
%{expand: %setup_tpls_env}

unset CFLAGS
unset CXXFLAGS
unset FCFLAGS
unset FFLAGS
%if "%{tpls_compiler}" == "gnu"
mkdir -p build && cd build && %{tpls_compilers} %{tpls_cmake} \
%else
mkdir -p build && cd build && LDFLAGS="%{tpls_comp_ldflags} %{tpls_comp_rpath}" %{tpls_compilers} %{tpls_cmake} \
%endif
-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
%if "%{tpls_compiler}" == "intel"
-DCMAKE_Fortran_COMPILER_ID="Intel" \
%if "%{tpls_libs}" == "static"
-DCMAKE_Fortran_FLAGS_RELEASE="%{tpls_fcflags} -assume protect_parens -recursive -diag-disable 10121" \
%else
-DCMAKE_Fortran_FLAGS_RELEASE="%{tpls_fcflags} -assume protect_parens -recursive  -fPIC -diag-disable 10121" \
%endif
%else
-DCMAKE_Fortran_COMPILER_ID="GNU" \
%if "%{tpls_libs}" == "static"
-DCMAKE_Fortran_FLAGS_RELEASE="%{tpls_fcflags} -frecursive" \
%else
-DCMAKE_Fortran_FLAGS_RELEASE="%{tpls_fcflags} -frecursive -fPIC " \
%endif
%endif
-DCBLAS=ON \
-DBLAS++=OFF \
-DXBLAS=ON \
-DLAPACKE=ON \
-DLAPACK++=OFF \
-DBUILD_INDEX64=OFF \
-DBUILD_INDEX64_EXT_API=OFF \
-DCMAKE_INSTALL_LIBDIR=lib \
-DBUILD_TESTING=ON \
%if "%{tpls_libs}" == "static"
-DBUILD_SHARED_LIBS=OFF \
%else
-DBUILD_SHARED_LIBS=ON \
%endif
..

make %{?_smp_mflags}

%check
cd build && make %{?_smp_mflags} test

%install
cd build && %make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/lib/cmake/lapack-%{version}/lapack-config-version.cmake
%{tpls_prefix}/lib/cmake/lapack-%{version}/lapack-config.cmake
%{tpls_prefix}/lib/cmake/lapack-%{version}/lapack-targets-release.cmake
%{tpls_prefix}/lib/cmake/lapack-%{version}/lapack-targets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/liblapack.a
%{tpls_prefix}/lib/libtmglib.a
%else
%{tpls_prefix}/lib/liblapack.so
%{tpls_prefix}/lib/liblapack.so.3
%{tpls_prefix}/lib/liblapack.so.%{version}
%{tpls_prefix}/lib/libtmglib.so
%{tpls_prefix}/lib/libtmglib.so.3
%{tpls_prefix}/lib/libtmglib.so.%{version}
%endif
%{tpls_prefix}/lib/pkgconfig/lapack.pc

%files -n tpls-%{tpls_flavor}-blas
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libblas.a
%else
%{tpls_prefix}/lib/libblas.so
%{tpls_prefix}/lib/libblas.so.3
%{tpls_prefix}/lib/libblas.so.%{version}
%endif
%{tpls_prefix}/lib/pkgconfig/blas.pc

%files -n tpls-%{tpls_flavor}-cblas
%{tpls_prefix}/include/cblas.h
%{tpls_prefix}/include/cblas_64.h
%{tpls_prefix}/include/cblas_f77.h
%{tpls_prefix}/include/cblas_mangling.h
%{tpls_prefix}/lib/cmake/cblas-%{version}/cblas-config-version.cmake
%{tpls_prefix}/lib/cmake/cblas-%{version}/cblas-config.cmake
%{tpls_prefix}/lib/cmake/cblas-%{version}/cblas-targets-release.cmake
%{tpls_prefix}/lib/cmake/cblas-%{version}/cblas-targets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libcblas.a
%else
%{tpls_prefix}/lib/libcblas.so
%{tpls_prefix}/lib/libcblas.so.3
%{tpls_prefix}/lib/libcblas.so.%{version}
%endif
%{tpls_prefix}/lib/pkgconfig/cblas.pc

%files -n tpls-%{tpls_flavor}-lapacke
%{tpls_prefix}/include/lapack.h
%{tpls_prefix}/include/lapacke.h
%{tpls_prefix}/include/lapacke_config.h
%{tpls_prefix}/include/lapacke_mangling.h
%{tpls_prefix}/include/lapacke_utils.h
%{tpls_prefix}/lib/cmake/lapacke-%{version}/lapacke-config-version.cmake
%{tpls_prefix}/lib/cmake/lapacke-%{version}/lapacke-config.cmake
%{tpls_prefix}/lib/cmake/lapacke-%{version}/lapacke-targets-release.cmake
%{tpls_prefix}/lib/cmake/lapacke-%{version}/lapacke-targets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/liblapacke.a
%else
%{tpls_prefix}/lib/liblapacke.so
%{tpls_prefix}/lib/liblapacke.so.3
%{tpls_prefix}/lib/liblapacke.so.%{version}
%endif
%{tpls_prefix}/lib/pkgconfig/lapacke.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.12.0-1
- Initial Package
