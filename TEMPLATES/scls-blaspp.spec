%define scls_oflags -O3

Name:           scls-%{scls_flavor}-blaspp
Version:        2023.11.05
Release:        1%{?dist}
Summary:        A C++ wrapper around CPU and GPU BLAS

License:        BSD
URL:            https://icl.utk.edu/slate/
Source0:        https://github.com/icl-utk-edu/blaspp/releases/download/v%{version}/blaspp-%{version}.tar.gz
Patch0:         blaspp_no_testsweep.patch
Patch1:         blaspp_fix_colors.patch

BuildRequires:  scls-%{scls_flavor}-testsweeper
BuildRequires:  %{scls_rpm_cxx} >= %{scls_comp_minver}

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%if "%{scls_math}" != "lapack"
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

%{expand: %setup_scls_env}

%if "%{scls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas.so|g" CMakeLists.txt
%endif

mkdir build && cd build
%{scls_env} \
%if "%{scls_math}" == "lapack"
LDFLAGS="%{scls_scalapack} %{scls_lapack} %{scls_blas}" \
%else
LDFLAGS="%{scls_mkl_linker_flags}" \
%endif
%if "%{scls_math}" == "cuda"
%if "%{scls_libs}" == "static"
LDFLAGS+=" -L%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64" \
%else
LDFLAGS+=" -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64" \
%endif
%endif
%{scls_cmake}  \
    -DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
    -DBUILD_SHARED_LIBS=OFF \
%else
    -DBUILD_SHARED_LIBS=ON \
%endif
    -Dbuild_tests=ON \
%if "%{scls_math}" == "lapack"
    -Dblas="generic" \
    -Dgpu_backend=none \
%elif "%{scls_math}"== "cuda"
    -Dblas="Intel MKL" \
    -Dgpu_backend=cuda \
    -DCMAKE_CUDA_COMPILER=%{scls_nvcc} \
    -DCMAKE_CUDA_FLAGS="%{scls_nvccflags}" \
	-DCMAKE_CUDA_ARCHITECTURES="%{scls_cuda_architectures}" \
%elif "%{scls_math}" == "mkl"
    -Dblas="Intel MKL" \
    -Dgpu_backend=none \
%endif
%if "%{scls_index_size}" == "32"
    -Dblas_int="int (LP64)" \
%else
    -Dblas_int="int64_t (ILP64)" \
%endif
%if "%{scls_libs}" == "shared"
%if "%{scls_math}" == "lapack"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%else
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib" \
%endif
%endif
%endif
    ..

%if "%{scls_math}" != "cuda"
sed -i 's|gpu_backend:STRING=cuda|gpu_backend:STRING=none|g' CMakeCache.txt
%{scls_cmake} . -Dgpu_backend:STRING=none
%endif

%make_build

%check
cd build
LD_LIBRARY_PATH=%{scls_ld_library_path} make %{?_smp_mflags} check

%install
cd build
%make_install
%{scls_remove_la_files}
%if "%{scls_libs}" == "static"
install -m 644 ./lib/libblaspp.a %{buildroot}%{scls_prefix}/lib ;
%endif

%files
%{scls_prefix}/include/blas.hh
%{scls_prefix}/include/blas/asum.hh
%{scls_prefix}/include/blas/axpy.hh
%{scls_prefix}/include/blas/batch_common.hh
%{scls_prefix}/include/blas/config.h
%{scls_prefix}/include/blas/copy.hh
%{scls_prefix}/include/blas/defines.h
%{scls_prefix}/include/blas/device.hh
%{scls_prefix}/include/blas/device_blas.hh
%{scls_prefix}/include/blas/dot.hh
%{scls_prefix}/include/blas/dotu.hh
%{scls_prefix}/include/blas/flops.hh
%{scls_prefix}/include/blas/fortran.h
%{scls_prefix}/include/blas/gemm.hh
%{scls_prefix}/include/blas/gemv.hh
%{scls_prefix}/include/blas/ger.hh
%{scls_prefix}/include/blas/geru.hh
%{scls_prefix}/include/blas/hemm.hh
%{scls_prefix}/include/blas/hemv.hh
%{scls_prefix}/include/blas/her.hh
%{scls_prefix}/include/blas/her2.hh
%{scls_prefix}/include/blas/her2k.hh
%{scls_prefix}/include/blas/herk.hh
%{scls_prefix}/include/blas/iamax.hh
%{scls_prefix}/include/blas/mangling.h
%{scls_prefix}/include/blas/nrm2.hh
%{scls_prefix}/include/blas/rot.hh
%{scls_prefix}/include/blas/rotg.hh
%{scls_prefix}/include/blas/rotm.hh
%{scls_prefix}/include/blas/rotmg.hh
%{scls_prefix}/include/blas/scal.hh
%{scls_prefix}/include/blas/swap.hh
%{scls_prefix}/include/blas/symm.hh
%{scls_prefix}/include/blas/symv.hh
%{scls_prefix}/include/blas/syr.hh
%{scls_prefix}/include/blas/syr2.hh
%{scls_prefix}/include/blas/syr2k.hh
%{scls_prefix}/include/blas/syrk.hh
%{scls_prefix}/include/blas/trmm.hh
%{scls_prefix}/include/blas/trmv.hh
%{scls_prefix}/include/blas/trsm.hh
%{scls_prefix}/include/blas/trsv.hh
%{scls_prefix}/include/blas/util.hh
%{scls_prefix}/include/blas/wrappers.hh
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libblaspp.a
%exclude %{scls_prefix}/lib/libblaspp.so
%else
%{scls_prefix}/lib/libblaspp.so
%endif
%{scls_prefix}/lib/cmake/blaspp

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05-1
- Initial Package
