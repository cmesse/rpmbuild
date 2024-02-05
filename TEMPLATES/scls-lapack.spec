%define scls_oflags -O2

Summary: Numerical linear algebra package libraries
Name: scls-%{scls_flavor}-lapack
Version: 3.12.0
Release: 1%{?dist}
License: BSD
URL: http://www.netlib.org/lapack/
Source0: https://github.com/Reference-LAPACK/lapack/archive/v%{version}.tar.gz

BuildRequires:  %{scls_rpm_fc}  >= %{scls_comp_minver}

BuildRequires: gawk
BuildRequires: make
BuildRequires: scls-%{scls_flavor}-cmake

Requires:      %{scls_rpm_fc}  >= %{scls_comp_minver}
Requires:      scls-%{scls_flavor}-blas

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


%package -n scls-%{scls_flavor}-blas
Summary: The Basic Linear Algebra Subprograms library

%description -n scls-%{scls_flavor}-blas
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra.


%package -n scls-%{scls_flavor}-cblas
Summary:        C interfaces for BLAS
Requires:       scls-%{scls_flavor}-blas

%description  -n scls-%{scls_flavor}-cblas
CBLAS, the C interface to the Basic Linear Algebra Subprograms (BLAS), 
is a standardized set of low-level routines that provide efficient
linear algebra operations, primarily for vector and matrix calculations.
Originally developed in FORTRAN for use in high-performance computing
BLAS has been fundamental in scientific computing and forms the backbone
of many complex numerical computing tasks. 
CBLAS is a C language interface to the BLAS library.

%package -n scls-%{scls_flavor}-lapacke
Requires:       scls-%{scls_flavor}-lapack  = %{version}
Summary: C Interface to Linear Algebra Package (LAPACK)

%description -n scls-%{scls_flavor}-lapacke
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

if [ "%{scls_math}" != "lapack" ] || [ "%{scls_compiler}" != "gnu" ]; then
    echo "Error: We only want to compile this library for scls-gnu-lapack-* flavors!"
    exit 1
fi


%setup -q -n lapack-%{version}

%build
%{expand: %setup_scls_env}
%{scls_env}
unset CFLAGS
unset CXXFLAGS
unset FCFLAGS
unset FFLAGS
%if "%{scls_compiler}" == "gnu"
mkdir -p build && cd build && %{scls_env} %{scls_cmake} \
%else
mkdir -p build && cd build && LDFLAGS="%{scls_comp_ldflags} %{scls_comp_rpath}" %{scls_env} %{scls_cmake} \
%endif
	-DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_fc} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
%if "%{scls_compiler}" == "intel"
-DCMAKE_Fortran_COMPILER_ID="Intel" \
%if "%{scls_libs}" == "static"
-DCMAKE_Fortran_FLAGS_RELEASE="%{scls_fcflags} -assume protect_parens -recursive -diag-disable 10121 %{scls_oflags}" \
%else
-DCMAKE_Fortran_FLAGS_RELEASE="%{scls_fcflags} -assume protect_parens -recursive  -fPIC -diag-disable 10121 %{scls_oflags}" \
%endif
%else
-DCMAKE_Fortran_COMPILER_ID="GNU" \
%if "%{scls_libs}" == "static"
-DCMAKE_Fortran_FLAGS_RELEASE="%{scls_fcflags} -frecursive %{scls_oflags}" \
%else
-DCMAKE_Fortran_FLAGS_RELEASE="%{scls_fcflags} -frecursive -fPIC %{scls_oflags}" \
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
%if "%{scls_libs}" == "static"
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
%{scls_remove_la_files}

%files
%{scls_prefix}/lib/cmake/lapack-%{version}/lapack-config-version.cmake
%{scls_prefix}/lib/cmake/lapack-%{version}/lapack-config.cmake
%{scls_prefix}/lib/cmake/lapack-%{version}/lapack-targets-release.cmake
%{scls_prefix}/lib/cmake/lapack-%{version}/lapack-targets.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/liblapack.a
%{scls_prefix}/lib/libtmglib.a
%else
%{scls_prefix}/lib/liblapack.so
%{scls_prefix}/lib/liblapack.so.3
%{scls_prefix}/lib/liblapack.so.%{version}
%{scls_prefix}/lib/libtmglib.so
%{scls_prefix}/lib/libtmglib.so.3
%{scls_prefix}/lib/libtmglib.so.%{version}
%endif
%{scls_prefix}/lib/pkgconfig/lapack.pc

%files -n scls-%{scls_flavor}-blas
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libblas.a
%else
%{scls_prefix}/lib/libblas.so
%{scls_prefix}/lib/libblas.so.3
%{scls_prefix}/lib/libblas.so.%{version}
%endif
%{scls_prefix}/lib/pkgconfig/blas.pc

%files -n scls-%{scls_flavor}-cblas
%{scls_prefix}/include/cblas.h
%{scls_prefix}/include/cblas_64.h
%{scls_prefix}/include/cblas_f77.h
%{scls_prefix}/include/cblas_mangling.h
%{scls_prefix}/lib/cmake/cblas-%{version}/cblas-config-version.cmake
%{scls_prefix}/lib/cmake/cblas-%{version}/cblas-config.cmake
%{scls_prefix}/lib/cmake/cblas-%{version}/cblas-targets-release.cmake
%{scls_prefix}/lib/cmake/cblas-%{version}/cblas-targets.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libcblas.a
%else
%{scls_prefix}/lib/libcblas.so
%{scls_prefix}/lib/libcblas.so.3
%{scls_prefix}/lib/libcblas.so.%{version}
%endif
%{scls_prefix}/lib/pkgconfig/cblas.pc

%files -n scls-%{scls_flavor}-lapacke
%{scls_prefix}/include/lapack.h
%{scls_prefix}/include/lapacke.h
%{scls_prefix}/include/lapacke_config.h
%{scls_prefix}/include/lapacke_mangling.h
%{scls_prefix}/include/lapacke_utils.h
%{scls_prefix}/lib/cmake/lapacke-%{version}/lapacke-config-version.cmake
%{scls_prefix}/lib/cmake/lapacke-%{version}/lapacke-config.cmake
%{scls_prefix}/lib/cmake/lapacke-%{version}/lapacke-targets-release.cmake
%{scls_prefix}/lib/cmake/lapacke-%{version}/lapacke-targets.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/liblapacke.a
%else
%{scls_prefix}/lib/liblapacke.so
%{scls_prefix}/lib/liblapacke.so.3
%{scls_prefix}/lib/liblapacke.so.%{version}
%endif
%{scls_prefix}/lib/pkgconfig/lapacke.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.12.0-1
- Initial Package
