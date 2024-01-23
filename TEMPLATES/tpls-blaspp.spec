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
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05-1
- Initial Package
