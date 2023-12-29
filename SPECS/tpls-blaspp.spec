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
Name:           tpls-%{tpls_flavor}-blaspp
Version:        2023.11.05
Release:        1%{?dist}
Summary:        BLAS++: C++ API for Basic Linear Algebra Subprogram

License:        BSD
URL:            https://icl.utk.edu/slate/
Source0:        https://github.com/icl-utk-edu/blaspp/releases/download/v%{version}/blaspp-%{version}.tar.gz
Patch0:         blaspp_no_testsweep.patch
Patch1:         blaspp_fix_colors.patch
Patch2:         blaspp_fix_cuda_static.patch
Patch3:         blaspp_fix_cuda_shared.patch
Patch4:         blaspp_fix_rocm_shared.patch

BuildRequires:  tpls-%{tpls_flavor}-testsweeper
BuildRequires:  %{tpls_rpm_cxx} >= %{tpls_comp_minver}

%if "%{tpls-gpu}" == "cuda" 
BuildRequires: nvhpc-cuda-multi
Requires:      nvhpc-cuda-multi
%elif "%{tpls_gpu}" == "rocm"
BuildRequires: rocm-hip-sdk
BuildRequires: rocsolver-devel
BuildRequires: rocblas-devel
BuildRequires: hip-runtime-amd
Requires: rocm-hip-sdk
Requires: rocsolver-devel
Requires: rocblas-devel
Requires: hip-runtime-amd
%endif

%description
The Basic Linear Algebra Subprograms (BLAS) have been around for many
decades and serve as the de facto standard for performance-portable and
numerically robust implementation of essential linear algebra
functionality. Originally, they were written in Fortran, and later
furnished with a C API (CBLAS).

The objective of BLAS++ is to provide a convenient, performance
oriented API for development in the C++ language, that,
for the most part, preserves established conventions, while, at the
same time, takes advantages of modern C++ features, such as:
namespaces, templates, exceptions, etc.

BLAS++ is part of the SLATE project
(Software for Linear Algebra Targeting Exascale), which is funded by
the Department of Energy as part of its Exascale Computing Initiative
(ECP). Closely related to BLAS++ is the LAPACK++ project,
which provides a C++ API for LAPACK.

%prep


%setup -q -n blaspp-%{version}
%patch0 -p1
%patch1 -p1
%if "%{tpls_gpu}" == "cuda"
%if "%{tpls_libs}" == "static"
%patch2 -p1
%else
%patch3 -p1
%endif
%endif
%if "%{tpls_gpu}" == "rocm"
%patch4 -p1
%endif

sed -i 's|-O2||g' make.inc.in 
sed -i 's|@CXXFLAGS@|@CXXFLAGS@ %{tpls_cxxflags} -I%{tpls_prefix}/include|g' make.inc.in 
sed -i 's|@prefix@|%{tpls_prefix}|g' make.inc.in 
sed -i 's|@CXX@|%{tpls_cxx}|g' make.inc.in 
sed -i 's|@LDFLAGS@| @LDFLAGS@ %{tpls_ldflags}|g'  make.inc.in 
%if "%{tpls_libs}" == "static"
sed -i 's|static   =|static   = 1|g' make.inc.in 
%endif


%build

%{expand: %setup_tpls_env}

PATH=%{tpls_prefix}/bin:$PATH \
LDFLAGS="-L/opt/intel/oneapi/mkl/latest/lib -Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib"  \
%if "%{tpls_gpu}" == "cuda"
python3 configure.py blas=mkl gpu_backend=cuda 
%elseif "%{tpls_gpu}" == "rocm"
python3 configure.py blas=mkl gpu_backend=rocm 
%else
%if "%{tpls_libs}" == "static"
BLAS_LIBRARIES="%{tpls_prefix}/lib/libcblas.a %{tpls_prefix}/lib/libblas.a" python3 configure.py blas=generic gpu_backend=none
%else
LD_LIBRARY_PATH="%{tpls_prefix}/lib" LDFLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix} -lcblas -lblas" BLAS_LIBRARIES=%{tpls_blas_shared} python3 configure.py blas=generic gpu_backend=none
%endif
%endif

%if "%{tpls_compiler}" == "intel"
sed -i 's|-fopenmp|-qopenmp|g' make.inc
%endif
%if "%{tpls_compiler}" == "nvidia"
sed -i 's|-fopenmp|-mp|g' make.inc
%endif



%make_build

%check
LD_LIBRARY_PATH=%{tpls_ld_library_path} make %{?_smp_mflags} check

%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/include/blas.hh
%{tpls_prefix}/include/blas/asum.hh
%{tpls_prefix}/include/blas/axpy.hh
%{tpls_prefix}/include/blas/batch_common.hh
%{tpls_prefix}/include/blas/config.h
%{tpls_prefix}/include/blas/copy.hh
%{tpls_prefix}/include/blas/defines.h
%{tpls_prefix}/include/blas/device.hh
%{tpls_prefix}/include/blas/device_blas.hh
%{tpls_prefix}/include/blas/dot.hh
%{tpls_prefix}/include/blas/dotu.hh
%{tpls_prefix}/include/blas/flops.hh
%{tpls_prefix}/include/blas/fortran.h
%{tpls_prefix}/include/blas/gemm.hh
%{tpls_prefix}/include/blas/gemv.hh
%{tpls_prefix}/include/blas/ger.hh
%{tpls_prefix}/include/blas/geru.hh
%{tpls_prefix}/include/blas/hemm.hh
%{tpls_prefix}/include/blas/hemv.hh
%{tpls_prefix}/include/blas/her.hh
%{tpls_prefix}/include/blas/her2.hh
%{tpls_prefix}/include/blas/her2k.hh
%{tpls_prefix}/include/blas/herk.hh
%{tpls_prefix}/include/blas/iamax.hh
%{tpls_prefix}/include/blas/mangling.h
%{tpls_prefix}/include/blas/nrm2.hh
%{tpls_prefix}/include/blas/rot.hh
%{tpls_prefix}/include/blas/rotg.hh
%{tpls_prefix}/include/blas/rotm.hh
%{tpls_prefix}/include/blas/rotmg.hh
%{tpls_prefix}/include/blas/scal.hh
%{tpls_prefix}/include/blas/swap.hh
%{tpls_prefix}/include/blas/symm.hh
%{tpls_prefix}/include/blas/symv.hh
%{tpls_prefix}/include/blas/syr.hh
%{tpls_prefix}/include/blas/syr2.hh
%{tpls_prefix}/include/blas/syr2k.hh
%{tpls_prefix}/include/blas/syrk.hh
%{tpls_prefix}/include/blas/trmm.hh
%{tpls_prefix}/include/blas/trmv.hh
%{tpls_prefix}/include/blas/trsm.hh
%{tpls_prefix}/include/blas/trsv.hh
%{tpls_prefix}/include/blas/util.hh
%{tpls_prefix}/include/blas/wrappers.hh
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libblaspp.a
%else
%{tpls_prefix}/lib/libblaspp.so
%endif
%{tpls_prefix}/lib/pkgconfig/blaspp.pc

%changelog
* Tue Dec 12 2023 Christian Messe <cmesse@lbl.gov> - 2023.11.05-1
- Initial Package
