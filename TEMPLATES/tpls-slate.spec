%global major_version 2023
%global minor_version 11
%global patch_version 05

Name:           tpls-%{tpls_flavor}-slate
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        1%{?dist}
Summary:        Basic linear algebra for distributed memory systems
License:        BSD-3-Clause
URL:            https://icl.bitbucket.io/slate/
Source0:        https://github.com/icl-utk-edu/slate/releases/download/v%{version}/slate-%{version}.tar.gz
Patch0:         slate_cmake.patch

%if   "%{tpls_mpi}" == "openmpi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%endif

%if "%{tpls_gpu}" == "rocm"
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
%else
BuildRequires: intel-oneapi-mkl
BuildRequires: intel-oneapi-mkl-devel
Requires:      intel-oneapi-mkl
%endif


BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  tpls-%{tpls_flavor}-testsweeper
BuildRequires:  tpls-%{tpls_flavor}-blaspp
BuildRequires:  tpls-%{tpls_flavor}-lapackpp

Requires:  tpls-%{tpls_flavor}-testsweeper
Requires:  tpls-%{tpls_flavor}-blaspp
Requires:  tpls-%{tpls_flavor}-lapackpp

%description
Software for Linear Algebra Targeting Exascale (SLATE) is being developed as part of the Exascale Computing Project (ECP), which is a joint project of the U.S. Department of Energy's Office of Science and National Nuclear Security Administration (NNSA). SLATE will deliver fundamental dense linear algebra capabilities for current and upcoming distributed-memory systems, including GPU-accelerated systems as well as more traditional multi core-only systems.

SLATE will provide coverage of existing LAPACK and ScaLAPACK functionality, including parallel implementations of Basic Linear Algebra Subroutines (BLAS), linear systems solvers, least squares solvers, and singular value and eigenvalue solvers. In this respect, SLATE will serve as a replacement for LAPACK and ScaLAPACK, which, after two decades of operation, cannot be adequately retrofitted for modern, GPU-accelerated architectures.

SLATE is built on top of standards, such as MPI and OpenMP, and de facto-standard industry solutions such as NVIDIA CUDA and AMD HIP. SLATE also relies on high performance implementations of numerical kernels from vendor libraries, such as Intel MKL, IBM ESSL, NVIDIA cuBLAS, and AMD rocBLAS. SLATE interacts with these libraries through a layer of C++ APIs. This figure shows SLATE's position in the ECP software stack.




%if "%{tpls_compiler}" == "intel"
%if "%{tpls_libs}" == "static"
%define slate_mpi_ldflags -L%{tpls_prefix}/lib -L%{tpls_comproot}/lib
%else
%define slate_mpi_ldflags -L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib
%endif
%else
%if "%{tpls_libs}" == "static"
%define slate_mpi_ldflags -L%{tpls_prefix}/lib
%else
%define slate_mpi_ldflags -L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib
%endif
%endif

%if "%{tpls_gpu}" == "cuda"
%if "%{tpls_libs}" == "static"
%define slate_gpu_ldflags -L%{tpls_cuda}/lib64 -L%{tpls_cudamath}/lib64 %{tpls_cuda}/lib64/libcudart_static.a %{tpls_cudamath}/lib64/libcusolver_static.a
%else
%define slate_gpu_ldflags -L%{tpls_cuda}/lib64  -Wl,-rpath,%{tpls_cuda}/lib64 -L%{tpls_cudamath}/lib64 -Wl,-rpath,%{tpls_cudamath}/lib64 %{tpls_cuda}/lib64/libcudart.so %{tpls_cudamath}/lib64/libcusolver.so
%endif
%endif

%if "%{tpls_gpu}" == "rocm"
%if "%{tpls_libs}" == "static"
%define slate_gpu_ldflags -L/opt/rocm/lib -L%{tpls_mklroot}/lib
%else
%define slate_gpu_ldflags -L/opt/rocm/lib -Wl,-rpath,/opt/rocm/lib  -L%{tpls_mklroot}/lib -Wl,-rpath,%{tpls_mklroot}/lib
%endif
%endif

%prep


if [ "%{tpls_gpu}" == "lapack" ]; then
    echo "Error: We only want to compile slate when using cuda or rocm"
    exit 1
fi

%setup -q -n slate-%{version}
%patch0 -p1

%build

%if "%{tpls_gpu}" == "cuda"
%if "%{tpls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas_static.a -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{tpls_cudamath}/lib64/libcusolver_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas.so -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{tpls_cudamath}/lib64/libcusolver.so|g" CMakeLists.txt
%endif
%elif "%{tpls_gpu}" == "rocm"
	sed -i "s|roc::rocblas|%{tpls_rocm}/lib/librocblas.so|g" CMakeLists.txt
%endif

mkdir build && cd build
%{tpls_env} \
%{tpls_cmake} \
	-G "Unix Makefiles" \
    -DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
    -DCMAKE_Fortran_COMPILER=%{tpls_fc} \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
    -DCMAKE_INSTALL_RPATH=%{tpls_prefix}/lib \
    -Dblaspp_DIR=%{tpls_prefix} \
	-DMKL_DIR=%{tpls_mklroot} \
	-DSCALAPACK_LIBRARIES="%{tpls_mkl_mpi_linker_flags}" \
%if "%{tpls_gpu}" == "lapack"
	-Dgpu_backend="none" \
%elif "%{tpls_gpu}" == "cuda"
	-Dgpu_backend="cuda" \
	-DCUDA_PATH=%{tpls_cuda} \
%elif "%{tpls_gpu}" == "rocm"
	-Dgpu_backend="hip" \
%endif
%if "%{tpls_compiler}" == "gnu"
%if "%{tpls_int}" == "32"
	-DMKL_INTERFACE_FULL="gf_lp64" \
%else
	-DMKL_INTERFACE_FULL="gf_ilp64" \
%endif
%elif "%{tpls_compiler}" == "intel"
%if "%{tpls_int}" == "32"
	-DMKL_INTERFACE_FULL="intel_lp64" \
%else
	-DMKL_INTERFACE_FULL="intel_ilp64" \
%endif
%elif "%{tpls_compiler}" == "nvidia"
%if "%{tpls_int}" == "32"
	-DMKL_INTERFACE_FULL="pgi_lp64" \
%else
	-DMKL_INTERFACE_FULL="pgi_ilp64" \
%endif
%endif
	-DMKL_MPI=%{tpls_mpi} \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_STATIC_LINKER_FLAGS="-L%{tpls_prefix}/lib" \
	-DMKL_LINK=static \
%else
	-DBUILD_SHARED_LIBS=ON \
	-DMKL_LINK=dynamic \
%if "%{tpls_gpu}" == "lapack"
	-DCMAKE_SHARED_LINKER_FLAGS="%{slate_mpi_ldflags}" \
	-DCMAKE_EXE_LINKER_FLAGS="%{slate_mpi_ldflags}" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="%{slate_gpu_ldflags} %{slate_mpi_ldflags}" \
	-DCMAKE_EXE_LINKER_FLAGS="%{slate_gpu_ldflags} %{slate_mpi_ldflags}" \
%endif
%endif
	-DMPI_CXX_COMPILER=%{tpls_mpicxx} \
%if "%{tpls_mpi}" == "intelmpi"
	-DMPIEXEC_EXECUTABLE=%{tpls_mpiroot}/bin/mpiexec \
%else
	-DMPIEXEC_EXECUTABLE=%{tpls_prefix}/bin/mpiexec  \
%endif
	..
	
%make_build

#%check
#cd build
#%make_build check

%install
cd build
%make_install

%files
%{tpls_prefix}/include/slate
%{tpls_prefix}/lib/cmake/slate
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libslate.a
%{tpls_prefix}/lib/libslate_lapack_api.a
%else
%{tpls_prefix}/lib/libslate.so
%{tpls_prefix}/lib/libslate_lapack_api.so
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.15-1
- Initial Package

