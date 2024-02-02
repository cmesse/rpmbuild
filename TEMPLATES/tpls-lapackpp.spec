Name:           tpls-%{tpls_flavor}-lapackpp
Version:        2023.11.05
Release:        1%{?dist}
Summary:        LAPACK++: C++ API for the Linear Algebra Package

License:        BSD
URL:            https://icl.utk.edu/slate/
Source0:        https://github.com/icl-utk-edu/lapackpp/releases/download/v2023.11.05/lapackpp-%{version}.tar.gz
Patch0:         lapackpp_no_testsweep_and_blaspp.patch 
Patch1:         lapackpp_fix_colors.patch

BuildRequires:  tpls-%{tpls_flavor}-blaspp == %{version}
Requires:       tpls-%{tpls_flavor}-blaspp == %{version}

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-cblas
BuildRequires:  tpls-%{tpls_flavor}-lapack
BuildRequires:  tpls-%{tpls_flavor}-lapacke
Requires:  tpls-%{tpls_flavor}-blas
Requires:  tpls-%{tpls_flavor}-cblas
Requires:  tpls-%{tpls_flavor}-lapack
Requires:  tpls-%{tpls_flavor}-lapacke
%endif

%description
he Linear Algebra PACKage (LAPACK) is a standard software library for numerical linear algebra. It provides routines for solving systems of linear equations and linear least squares problems, eigenvalue problems, and singular value decomposition. It also includes routines to implement the associated matrix factorizations such as LU, QR, Cholesky, etc. LAPACK was originally written in FORTRAN 77, and moved to Fortran 90 in version 3.2 (2008). LAPACK provides routines for handling both real and complex matrices in both single and double precision.

The objective of LAPACK++ is to provide a convenient, performance oriented API for development in the C++ language, that, for the most part, preserves established conventions, while, at the same time, takes advantages of modern C++ features, such as: namespaces, templates, exceptions, etc.

%prep

%setup -q -n lapackpp-%{version}
%patch0 -p1
%patch1 -p1

%build

%{expand: %setup_tpls_env}

%if "%{tpls_gpu}" == "cuda"
%if "%{tpls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{tpls_cudamath}/lib64/libcusolver_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas.so|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{tpls_cudamath}/lib64/libcusolver.so|g" CMakeLists.txt
%endif
%elif "%{tpls_gpu}" == "rocm"
	sed -i "s|roc::rocblas|%{tpls_rocm}/lib/librocblas.so|g" CMakeLists.txt
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
    -DBLA_VENDOR="Generic" \
    -Dgpu_backend=none \
%else
%if "%{tpls_int}" == "32"
    -DBLA_VENDOR="Intel10_64lp" \
%else
    -DBLA_VENDOR="Intel10_64ilp" \
%endif
%if "%{tpls_gpu}"== "cuda"
    -Dgpu_backend=cuda \
    -Dbuild_tests=ON \
%elif "%{tpls_gpu}" == "rocm"
    -Dgpu_backend=hip \
    -Dbuild_tests=OFF \
%endif
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


%check
%if "%{tpls_gpu}" == "cuda"
LD_LIBRARY_PATH=%{tpls_ld_library_path}:%{tpls_mklroot}/lib make %{?_smp_mflags} check
%endif

%install
cd build
%make_install


%{tpls_remove_la_files}

%files
%{tpls_prefix}/include/lapack.hh
%{tpls_prefix}/include/lapack/*.h
%{tpls_prefix}/include/lapack/*.hh
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/liblapackpp.a
%exclude %{tpls_prefix}/lib/liblapackpp.so
%else
%{tpls_prefix}/lib/liblapackpp.so
%endif
%{tpls_prefix}/lib/cmake/lapackpp

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05-1
- Initial Package
