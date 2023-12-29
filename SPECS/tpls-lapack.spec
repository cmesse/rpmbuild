#######################################################################
# FLAVOR SPECIFIC DEFINES                                             #
#######################################################################

%define tpls_flavor skylake-gnu-openmpi-lapack-static-32 

%define tpls_host skylake 
%define tpls_compiler gnu 
%define tpls_mpi openmpi 
%define tpls_gpu lapack 
%define tpls_libs static 
%define tpls_int 32 
%define tpls_comp_minver 11.4.1 

%define tpls_rpm_cc gcc 
%define tpls_rpm_cxx gcc-c++ 
%define tpls_rpm_fc gfortran 
%define tpls_auto_req_prov yes

# important paths
%define tpls_prefix /opt/tpls/skylake-gnu-openmpi-lapack-static-32 
%define tpls_includes /opt/tpls/skylake-gnu-openmpi-lapack-static-32/includes 
%define tpls_libdir /opt/tpls/skylake-gnu-openmpi-lapack-static-32/lib 
%define tpls_comproot /usr 
%define tpls_mklroot  /opt/intel/oneapi/mkl/latest 
%define tpls_cuda  /opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda 
%define tpls_rocm  /opt/rocm 
%define tpls_ld_library_path  /opt/tpls/skylake-gnu-openmpi-lapack-static-32/lib 

# compiler executables
%define tpls_cc gcc 
%define tpls_cxx g++ 
%define tpls_fc gfortran 
%define tpls_ar ar 
%define tpls_ld ld 
%define tpls_cpp ld -E 
%define tpls_cxxcpp ld -E 

# MPI wrappers
%define tpls_mpicc   /opt/tpls/skylake-gnu-openmpi-lapack-static-32/bin/mpicc
%define tpls_mpicxx  /opt/tpls/skylake-gnu-openmpi-lapack-static-32/bin/mpicxx 
%define tpls_mpifort /opt/tpls/skylake-gnu-openmpi-lapack-static-32/bin/mpifort 

# Compiler Flags
%define tpls_cflags   -O2 -m64 -fno-fast-math -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-openmpi-lapack-static-32/include
%define tpls_cxxflags   -O2 -m64 -fno-fast-math -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-openmpi-lapack-static-32/include
%define tpls_fcflags   -O2 -m64 -fno-fast-math -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-openmpi-lapack-static-32/include
%define tpls_ldflags    -L/opt/tpls/skylake-gnu-openmpi-lapack-static-32/lib
%define tpls_arflags   -cru
%define tpls_ompflag    -fopenmp

# the netlib reference implementations
%define tpls_blas   /opt/tpls/skylake-gnu-openmpi-lapack-static-32/libblas.a
%define tpls_lapack  /opt/tpls/skylake-gnu-openmpi-lapack-static-32/liblapack.a
%define tpls_scalapack /opt/tpls/skylake-gnu-openmpi-lapack-static-32/libscalapack.a

# the MKL setup
%define tpls_mkl_linker_flags    -Wl,--start-group /opt/intel/oneapi/mkl/latest/lib/libmkl_intel_lp64.a /opt/intel/oneapi/mkl/latest/lib/libmkl_gnu_thread.a /opt/intel/oneapi/mkl/latest/lib/libmkl_core.a -Wl,--end-group  -lgomp -lpthread -lm -ldl
%define tpls_mkl_mpi_linker_flags  /opt/intel/oneapi/mkl/latest/lib/libmkl_scalapack_lp64.a  -Wl,--start-group /opt/intel/oneapi/mkl/latest/lib/libmkl_intel_lp64.a /opt/intel/oneapi/mkl/latest/lib/libmkl_gnu_thread.a /opt/intel/oneapi/mkl/latest/lib/libmkl_core.a -Wl,--end-group /opt/intel/oneapi/mkl/latest/lib/libmkl_blacs_openmpi_lp64.a  -lgomp -lpthread -lm -ldl

########################################################################
# ENVIRONMENT SETUP                                                    #
########################################################################


%global setup_tpls_env \
# setup the Intel OneAPI \
if [ "%{tpls_gpu}" != "lapack" ]; then \
  if [ "$SETVARS_COMPLETED" != "1" ]; then \
    source /opt/intel/oneapi/setvars.sh intel64; \
  fi; \
fi; \
export LD=%{tpls_ld} \
export AR=%{tpls_ar} \
export CC=%{tpls_cc} \
export CPP="%{tpls_cc} -E" \
export CXXCPP="%{tpls_cxx} -E" \
export CXX=%{tpls_cxx} \
export FC=%{tpls_fc} \
export F77=%{tpls_fc} \
export FF=%{tpls_fc} \
export CFLAGS="%{tpls_cflags}" \
export CXXFLAGS="%{tpls_cxxflags}" \
export FFLAGS="%{tpls_fcflags}" \
export FCLAGS="%{tpls_fcflags}" \
# check if the compilers are in the path \
if [[ ":$PATH:" != *:%{tpls_comproot}/bin* ]]; then \
  export PATH="%{tpls_comproot}/bin:$PATH"; \
fi; \
# check if CUDA is used and in the path \
if [ "%{tpls_gpu}" == "cuda" ]; then \
  if [[ ":$PATH:" != *:%{tpls_cuda}/bin* ]]; then \
    export PATH="%{tpls_cuda}/bin:$PATH"; \
  fi; \
fi; \
# check if ROCM is used and in the path \
if [ "%{tpls_gpu}" == "rocm" ]; then \
  if [[ ":$PATH:" != *:%{tpls_rocm}/bin* ]]; then \
    export PATH="%{tpls_rocm}/bin:$PATH"; \
  fi; \
fi; \
# add the TPLS binary directory \
if [[ ":$PATH:" != *:%{tpls_prefix}/bin* ]]; then \
  export PATH="%{tpls_prefix}/bin:$PATH"; \
fi;
########################################################################
# AUTOMATIC MACROS                                                     #
########################################################################

%define tpls_maxprocs 64

%define tpls_compilers     \
	LD=%{tpls_ld}   \
	AR=%{tpls_ar}   \
	CC=%{tpls_cc}   \
	CXX=%{tpls_cxx} \
	FC=%{tpls_fc}   \
	FF=%{tpls_fc}   \
	F77=%{tpls_fc}

# fix the qversion bug in configure
%define tpls_remove_qversion    sed -i 's| -qversion||'g ./configure ;

# delete-la-tool
%define tpls_remove_la_files    find %{buildroot} -name '*.la' -delete

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
BuildRequires: cmake

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
mkdir -p build && cd build && %{tpls_compilers} cmake \
%else
mkdir -p build && cd build && LDFLAGS="%{tpls_comp_ldflags} %{tpls_comp_rpath}" %{tpls_compilers} cmake \
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
* Tue Dec 12 2023 Christian Messe <cmesse@lbl.gov> - 3.12.0-1
- Initial package.
