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
Name:           tpls-%{tpls_flavor}-testsweeper
Version:        2023.11.05
Release:        1%{?dist}
Summary:        A C++ testing framework for parameter sweeps.

License:        BSD
URL:            https://github.com/icl-utk-edu/testsweeper
Source0:        https://github.com/icl-utk-edu/testsweeper/releases/download/v2023.11.05/testsweeper-%{version}.tar.gz
BuildRequires: make
BuildRequires: cmake

BuildRequires:      %{tpls_rpm_cc}  >= %{tpls_comp_minver}
BuildRequires:      %{tpls_rpm_cxx} >= %{tpls_comp_minver}

%description
TestSweeper is a C++ testing framework for parameter sweeps.
It handles parsing command line options, iterating over the test space,
and printing results. This simplifies test functions by allowing them to
concentrate on setting up and solving one problem at a time.

TestSweeper is part of the SLATE project
(Software for Linear Algebra Targeting Exascale), which is funded by
the Department of Energy as part of its Exascale Computing Initiative
(ECP).

%prep
%setup -q -n testsweeper-%{version}

%build
%{expand: %setup_tpls_env}

mkdir -p build && cd build && LDFLAGS="%{tpls_ldflags} %{tpls_rpath}" %{tpls_compilers} LD=%{tpls_cxx} cmake \
-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
-DCMAKE_CXX_COMPILER=%{tpls_cxx} \
-DCMAKE_INSTALL_LIBDIR=lib \
-Dbuild_tests=ON \
%if "%{tpls_libs}" == "static"
-DBUILD_SHARED_LIBS=OFF \
-DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
%else
-DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -fPIC" \
-DBUILD_SHARED_LIBS=ON \
%endif
..

%make_build

%check
cd  build && make test

%install
cd build && %make_install

%files
%{tpls_prefix}/include/testsweeper.hh
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperConfig.cmake
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperConfigVersion.cmake
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperTargets-noconfig.cmake
%{tpls_prefix}/lib/cmake/testsweeper/testsweeperTargets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libtestsweeper.a
%else
%{tpls_prefix}/lib/libtestsweeper.so
%endif

%changelog
* Tue Dec 12 2023 Christian Messe <cmesse@lbl.gov> - 2023.11.05
- Initial package.

