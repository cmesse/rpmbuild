%define scls_oflags -O3

Name:           scls-%{scls_flavor}-lapackpp
Version:        2023.11.05
Release:        1%{?dist}
Summary:        C++ API for the Linear Algebra Package

License:        BSD
URL:            https://icl.utk.edu/slate/
Source0:        https://github.com/icl-utk-edu/lapackpp/releases/download/v2023.11.05/lapackpp-%{version}.tar.gz
Patch0:         lapackpp_no_testsweep_and_blaspp.patch 
Patch1:         lapackpp_fix_colors.patch

BuildRequires:  scls-%{scls_flavor}-blaspp == %{version}
Requires:       scls-%{scls_flavor}-blaspp == %{version}

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
he Linear Algebra PACKage (LAPACK) is a standard software library for numerical linear algebra. It provides routines for solving systems of linear equations and linear least squares problems, eigenvalue problems, and singular value decomposition. It also includes routines to implement the associated matrix factorizations such as LU, QR, Cholesky, etc. LAPACK was originally written in FORTRAN 77, and moved to Fortran 90 in version 3.2 (2008). LAPACK provides routines for handling both real and complex matrices in both single and double precision.

The objective of LAPACK++ is to provide a convenient, performance oriented API for development in the C++ language, that, for the most part, preserves established conventions, while, at the same time, takes advantages of modern C++ features, such as: namespaces, templates, exceptions, etc.

%prep

%setup -q -n lapackpp-%{version}
%patch0 -p1
%patch1 -p1
%define scls_oflags -O3
%build

%{expand: %setup_scls_env}

%if "%{scls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{scls_cudamath}/lib64/libcusolver_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas.so|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{scls_cudamath}/lib64/libcusolver.so|g" CMakeLists.txt
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
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
    -DBUILD_SHARED_LIBS=OFF \
%else
    -DBUILD_SHARED_LIBS=ON \
%endif
%if "%{scls_math}" == "lapack"
    -Dblas="generic" \
    -Dgpu_backend=none \
%elif "%{scls_math}"== "cuda"
    -Dblas="Intel MKL" \
    -Dgpu_backend=cuda \
    -DCMAKE_CUDA_COMPILER=%{scls_nvcc} \
    -DCMAKE_CUDA_FLAGS=%{scls_nvccflags} \
    -DCMAKE_CUDA_COMPILER=%{scls_nvcc} \
    -DCMAKE_CUDA_FLAGS="%{scls_nvccflags}" \
	-DCMAKE_CUDA_ARCHITECTURES="%{scls_cuda_architectures}" \
%elif "%{scls_math}" == "mkl"
    -Dblas="Intel MKL" \
    -Dgpu_backend=none \
%endif
%if "%{scls_index_size}" == "32"
    -DBLA_VENDOR="Intel10_64lp" \
%else
    -DBLA_VENDOR="Intel10_64ilp" \
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
LD_LIBRARY_PATH=%{scls_ld_library_path}:%{scls_mklroot}/lib make %{?_smp_mflags} check

%install
cd build
%make_install


%{scls_remove_la_files}

%files
%{scls_prefix}/include/lapack.hh
%{scls_prefix}/include/lapack/*.h
%{scls_prefix}/include/lapack/*.hh
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/liblapackpp.a
%exclude %{scls_prefix}/lib/liblapackpp.so
%else
%{scls_prefix}/lib/liblapackpp.so
%endif
%{scls_prefix}/lib/cmake/lapackpp

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05-1
- Initial Package
