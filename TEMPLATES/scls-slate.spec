%global major_version 2023
%global minor_version 11
%global patch_version 05

%define scls_oflags -O3

Name:           scls-%{scls_flavor}-slate
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        1%{?dist}
Summary:        Basic linear algebra for distributed memory systems
License:        BSD-3-Clause
URL:            https://icl.bitbucket.io/slate/
Source0:        https://github.com/icl-utk-edu/slate/releases/download/v%{version}/slate-%{version}.tar.gz
Patch0:         slate_cmake.patch

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

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

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  scls-%{scls_flavor}-testsweeper
BuildRequires:  scls-%{scls_flavor}-blaspp
BuildRequires:  scls-%{scls_flavor}-lapackpp

Requires:  scls-%{scls_flavor}-testsweeper
Requires:  scls-%{scls_flavor}-blaspp
Requires:  scls-%{scls_flavor}-lapackpp

%description
Software for Linear Algebra Targeting Exascale (SLATE) is being developed as part of the Exascale Computing Project (ECP), which is a joint project of the U.S. Department of Energy's Office of Science and National Nuclear Security Administration (NNSA). SLATE will deliver fundamental dense linear algebra capabilities for current and upcoming distributed-memory systems, including GPU-accelerated systems as well as more traditional multi core-only systems.

SLATE will provide coverage of existing LAPACK and ScaLAPACK functionality, including parallel implementations of Basic Linear Algebra Subroutines (BLAS), linear systems solvers, least squares solvers, and singular value and eigenvalue solvers. In this respect, SLATE will serve as a replacement for LAPACK and ScaLAPACK, which, after two decades of operation, cannot be adequately retrofitted for modern, GPU-accelerated architectures.

SLATE is built on top of standards, such as MPI and OpenMP, and de facto-standard industry solutions such as NVIDIA CUDA and AMD HIP. SLATE also relies on high performance implementations of numerical kernels from vendor libraries, such as Intel MKL, IBM ESSL, NVIDIA cuBLAS, and AMD rocBLAS. SLATE interacts with these libraries through a layer of C++ APIs. This figure shows SLATE's position in the ECP software stack.




%if "%{scls_compiler}" == "intel"
%if "%{scls_libs}" == "static"
%define slate_mpi_ldflags -L%{scls_prefix}/lib -L%{scls_comproot}/lib
%else
%define slate_mpi_ldflags -L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib
%endif
%else
%if "%{scls_libs}" == "static"
%define slate_mpi_ldflags -L%{scls_prefix}/lib
%else
%define slate_mpi_ldflags -L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib
%endif
%endif

%if "%{scls_math}" == "cuda"
%if "%{scls_libs}" == "static"
%define slate_math_libs %{scls_cuda}/lib64/libcudart_static.a %{scls_cudamath}/lib64/libcusolver_static.a
%define slate_math_ldflags -L%{scls_cuda}/lib64 -L%{scls_cudamath}/lib64
%else
%define slate_math_libs %{scls_cuda}/lib64/libcudart.so %{scls_cudamath}/lib64/libcusolver.so
%define slate_math_ldflags -L%{scls_cuda}/lib64  -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64
%endif
%endif

%prep

%setup -q -n slate-%{version}
%patch0 -p1

%build

%if "%{scls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas_static.a -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{scls_cudamath}/lib64/libcusolver_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas.so -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{scls_cudamath}/lib64/libcusolver.so|g" CMakeLists.txt
%endif

sed -i "s|-O3 |%{scls_oflags} |g" GNUmakefile

mkdir build && cd build
%{scls_env} \
%{scls_cmake} \
	-G "Unix Makefiles" \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags}" \
    -DCMAKE_INSTALL_RPATH=%{scls_prefix}/lib \
    -Dblaspp_DIR=%{scls_prefix} \
%if "%{scls_math}" == "lapack"
	-DSCALAPACK_LIBRARIES="%{scls_scalapack};%{scls_lapack};%{scls_blas};%{scls_mpilib}" \
%else
	-DSCALAPACK_LIBRARIES="%{scls_mkl_mpi_linker_flags}" \
%endif
	-Dgpu_backend="none" \
	-DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
%if "%{scls_libs}" == "static"
%if "%{scls_math}" != "lapack"
	-DMKL_MPI=%{scls_mpi} \
%endif
%else
%if "%{scls_math}" == "lapack"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%else
%if "%{scls_math}" == "mkl"
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
%else
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{slate_math_ldflags} %{slate_math_libs} -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{slate_math_ldflags} %{slate_math_libs} -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{slate_math_ldflags} %{slate_math_libs} -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{slate_math_ldflags} %{slate_math_libs} -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{slate_math_ldflags} %{slate_math_libs} -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{slate_math_ldflags} %{slate_math_libs} -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib" \
%endif
%endif
%endif
%endif
	..

sed -i 's|-O3 |%{scls_oflags} |g' CMakeCache.txt

%if "%{scls_math}" != "cuda"
sed -i 's|gpu_backend:STRING=cuda|gpu_backend:STRING=none|g' CMakeCache.txt
%{scls_cmake} ..
%else
sed -i 's|find_package( CUDAToolkit|# find_package( CUDAToolkit|g' ../CMakeLists.txt
sed -i 's|CUDAToolkit_FOUND|True|g' ../CMakeLists.txt
sed -i 's|slate testsweeper|slate slate_lapack_api testsweeper |g' ../unit_test/CMakeLists.txt
%{scls_cmake} \
	-Dgpu_backend=cuda \
	-DCUDA_PATH=%{scls_cuda} \
    -DCMAKE_CUDA_COMPILER=%{scls_nvcc} \
    -DCMAKE_CUDA_FLAGS="%{scls_nvccflags}" \
	-DCMAKE_CUDA_ARCHITECTURES="%{scls_cuda_architectures}" \
	 ..
%endif

%make_build

#%check # causes a timeout in heev
#cd build
#LD_LIBRARY_PATH=%{scls_ld_library_path} %make_build check

%install
cd build
%make_install

%files
%{scls_prefix}/include/slate
%{scls_prefix}/lib/cmake/slate
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libslate.a
%{scls_prefix}/lib/libslate_lapack_api.a
%else
%{scls_prefix}/lib/libslate.so
%{scls_prefix}/lib/libslate_lapack_api.so
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.15-1
- Initial Package

