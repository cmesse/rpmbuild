Name:           tpls-%{tpls_flavor}-blaspp
Version:        2023.11.05
Release:        1%{?dist}
Summary:        BLAS++: C++ API for Basic Linear Algebra Subprogram

License:        BSD
URL:            https://icl.utk.edu/slate/
Source0:        https://github.com/icl-utk-edu/blaspp/releases/download/v%{version}/blaspp-%{version}.tar.gz
Patch0:         blaspp_no_testsweep.patch
Patch1:         blaspp_fix_colors.patch

BuildRequires:  tpls-%{tpls_flavor}-testsweeper
BuildRequires:  %{tpls_rpm_cxx} >= %{tpls_comp_minver}

%if "%{tpls-gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-cblas
BuildRequires:  tpls-%{tpls_flavor}-lapack
%elif "%{tpls-gpu}" == "cuda" 
BuildRequires: nvhpc-cuda-multi
Requires:      nvhpc-cuda-multi
BuildRequires: intel-oneapi-mkl
BuildRequires: intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%elif "%{tpls_gpu}" == "rocm"
AutoReqProv: no
BuildRequires: rocm-hip-sdk
BuildRequires: rocsolver-devel
BuildRequires: rocblas-devel
BuildRequires: hip-runtime-amd
Requires: rocm-hip-sdk
Requires: rocsolver-devel
Requires: rocblas-devel
Requires: hip-runtime-amd
Requires: hipblas
Requires: rocblas
BuildRequires: intel-oneapi-mkl
BuildRequires: intel-oneapi-mkl-devel
Requires:      intel-oneapi-mkl
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

%build

%{expand: %setup_tpls_env}

%if "%{tpls_gpu}" == "cuda"
%if "%{tpls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas.so|g" CMakeLists.txt
%endif
%elif "%{tpls_gpu}" == "rocm"
	sed -i "s|roc::rocblas|%{tpls_rocm}/lib/librocblas.so %{tpls_rocm}/lib/libhipblas.so %{tpls_rocm}/lib/libhsa-runtime64.so %{tpls_rocm}/lib/libamdhip64.so|g" CMakeLists.txt
%endif

mkdir build && cd build
%{tpls_env} \
%if "%{tpls_gpu}" == "lapack"
LDFLAGS="%{tpls_scalapack} %{tpls_lapack} %{tpls_blas}" \
%else
LDFLAGS="%{tpls_mkl_linker_flags}" \
%endif
%{tpls_cmake}  \
	-DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
%if "%{tpls_libs}" == "static"
    -DBUILD_SHARED_LIBS=OFF \
%else
    -DBUILD_SHARED_LIBS=ON \
%endif
%if "%{tpls_gpu}" == "lapack"
    -Dblas="generic" \
    -Dgpu_backend=none \
%elif "%{tpls_gpu}"== "cuda"
    -Dblas="Intel MKL" \
    -Dgpu_backend=cuda \
    -Dbuild_tests=ON \
%elif "%{tpls_gpu}" == "rocm"
    -Dblas="Intel MKL" \
    -Dgpu_backend=hip \
    -Dbuild_tests=OFF \
%endif
%if "%{tpls_int}" == "32"
    -Dblas_int="int (LP64)" \
%else
    -Dblas_int="int64_t (ILP64)" \
%endif
%if "%{tpls_gpu}" == "lapack"
%if "%{tpls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
%endif
%else
%if "%{tpls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mklroot}/lib -Wl,-rpath,%{tpls_mklroot}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mklroot}/lib -Wl,-rpath,%{tpls_mklroot}/lib  -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mklroot}/lib -Wl,-rpath,%{tpls_mklroot}/lib " \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mklroot}/lib -Wl,-rpath,%{tpls_mklroot}/lib " \
%endif
%endif
    ..

%make_build

%if "%{tpls_gpu}" == "cuda"
%check
cd build
LD_LIBRARY_PATH=%{tpls_ld_library_path} make %{?_smp_mflags} check
%endif

%install
cd build
%make_install
%{tpls_remove_la_files}
%if "%{tpls_libs}" == "static"
install -m 644 ./lib/libblaspp.a %{buildroot}%{tpls_prefix}/lib ;
%endif

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
%exclude %{tpls_prefix}/lib/libblaspp.so
%else
%{tpls_prefix}/lib/libblaspp.so
%endif
%{tpls_prefix}/lib/cmake/blaspp

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05-1
- Initial Package
