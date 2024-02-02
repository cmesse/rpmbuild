Name:           tpls-%{tpls_flavor}-strumpack
Version:        7.1.0
Release:        1%{?dist}
Summary:        STRUMPACK - STRUctured Matrix PACKage

License:        BSD-3-Clause
URL:            https://portal.nersc.gov/project/sparse/strumpack
Source0:        https://github.com/pghysels/STRUMPACK/archive/v%{version}.tar.gz
Patch0:         strumpack_no_scalapack_check.patch

BuildRequires:  %{tpls_rpm_cc}   >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_cxx}  >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_fc}   >= %{tpls_comp_minver}

%if "%{tpls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{tpls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{tpls_comp_minver}
%endif

BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  tpls-%{tpls_flavor}-metis
BuildRequires:  tpls-%{tpls_flavor}-parmetis
BuildRequires:  tpls-%{tpls_flavor}-scotch
BuildRequires:  tpls-%{tpls_flavor}-zfp
BuildRequires:  tpls-%{tpls_flavor}-butterflypack


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

%if "%{tpls_gpu}" == "cuda"
BuildRequires: nvhpc-cuda-multi
Requires:      nvhpc-cuda-multi
BuildRequires:  tpls-%{tpls_flavor}-slate
Requires:  tpls-%{tpls_flavor}-slate
%elif "%{tpls_gpu}" == "rocm"
BuildRequires: rocm-hip-sdk
BuildRequires: rocsolver-devel
BuildRequires: rocblas-devel
BuildRequires: hip-runtime-amd
Requires: rocm-hip-sdk
Requires: rocsolver-devel
Requires: rocblas-devel
Requires: hip-runtime-amd
BuildRequires:  tpls-%{tpls_flavor}-slate
Requires:  tpls-%{tpls_flavor}-slate
%endif

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
BuildRequires:  tpls-%{tpls_flavor}-scalapack
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-scalapack
%else
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%endif
BuildRequires:  xz-devel
Requires:       xz

%description
STRUMPACK - STRUctured Matrix PACKage - is a software library providing linear algebra routines and linear system solvers for sparse and for dense rank-structured linear systems. Many large dense matrices are rank structured, meaning they exhibit some kind of low-rank property, for instance in hierarchically defined sub-blocks. In sparse direct solvers based on LU factorization, the LU factors can often also be approximated well using rank-structured matrix compression, leading to robust preconditioners. The sparse solver in STRUMPACK can also be used as an exact direct solver, in which case it functions similarly as for instance SuperLU or Superlu_Dist. The STRUMPACK sparse direct solver delivers good performance and distributed memory scalability and provides excellent CUDA support.

%prep
%setup -q -n STRUMPACK-%{version}
%if "%{tpls_gpu}" == "cuda"
%patch0 -p1
%elif "%{tpls_gpu}" == "rocm"
%patch0 -p1
%endif

%if "%{tpls_gpu}" == "cuda"
%if "%{tpls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas_static.a -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{tpls_prefix}/lib/liblapackpp.a %{tpls_prefix}/lib/libblaspp.a  %{tpls_cudamath}/lib64/libcusolver_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{tpls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{tpls_cudamath}/lib64/libcublas.so -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{tpls_prefix}/lib/liblapackpp.so %{tpls_prefix}/lib/libblaspp.so %{tpls_cudamath}/lib64/libcusolver.so|g" CMakeLists.txt
%endif
%endif

%build
%{tpls_env} \
%if "%{tpls_gpu}" == "lapack"
LDFLAGS="%{tpls_scalapack} %{tpls_lapack} %{tpls_blas} %{tpls_mpilib}" \
%else
LDFLAGS="%{tpls_mkl_mpi_linker_flags} %{tpls_mpilib}" \
%endif
%{tpls_cmake}  \
    -DBUILD_TESTING=OFF \
	-DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
%if "%{tpls_gpu}" == "cuda"
    -DCMAKE_C_FLAGS="%{tpls_cflags} -I%{tpls_prefix}/include/zfp -I%{tpls_cudamath}/include -I%{tpls_cuda}/include" \
    -DCMAKE_CXX_FLAGS="%{tpls_cflags} -I%{tpls_prefix}/include/zfp -I%{tpls_cudamath}/include -I%{tpls_cuda}/include" \
%else
    -DCMAKE_C_FLAGS="%{tpls_cflags} -I%{tpls_prefix}/include/zfp" \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -I%{tpls_prefix}/include/zfp" \
%endif
    -DCMAKE_Fortran_COMPILER=%{tpls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
    -DSTRUMPACK_USE_CUDA=OFF \
    -DSTRUMPACK_USE_HIP=OFF \
    -DTPL_ENABLE_SLATE=OFF \
    -DSTRUMPACK_USE_SYCL=OFF \
    -DSTRUMPACK_USE_MPI=ON \
    -DTPL_ENABLE_BPACK=ON \
    -DTPL_ENABLE_PARMETIS=ON \
    -DTPL_ENABLE_SCOTCH=ON \
    -DTPL_ENABLE_PTSCOTCH=ON \
    -DTPL_ENABLE_ZFP=ON \
%if "%{tpls_libs}" == "shared"
%if "%{tpls_compiler}" == "intel"
%if "%{tpls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mpiroot}/lib -Wl,-rpath,%{tpls_mpiroot}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mpiroot}/lib -Wl,-rpath,%{tpls_mpiroot}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
%endif
%endif
%if "%{tpls_int}" == "32"
    -DSTRUMPACK_USE_BLAS64=OFF \
%else
    -DSTRUMPACK_USE_BLAS64=ON \
%endif
    .

# fix the cuda settings
%if "%{tpls_gpu}" == "cuda"
%{tpls_cmake}  \
    -DCMAKE_CUDA_ARCHITECTURES="61;70;75;80;86" \
    -DCMAKE_C_FLAGS="%{tpls_cflags} -I%{tpls_prefix}/include/zfp -I%{tpls_cudamath}/include -I%{tpls_cuda}/include" \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -I%{tpls_prefix}/include/zfp -I%{tpls_cudamath}/include -I%{tpls_cuda}/include" \
    -DCMAKE_CUDA_FLAGS="-I%{tpls_cudamath}/include -I%{tpls_cuda}/include" \
    -DSTRUMPACK_USE_CUDA=ON \
    -DTPL_ENABLE_SLATE=ON \
    -Dblaspp_DIR=%{tpls_prefix}/lib/cmake/blaspp \
    -Dlapackpp_DIR=%{tpls_prefix}/lib/cmake/lapackpp \
    -Dslate_DIR=%{tpls_prefix}/lib/cmake/slate \
    .
%endif

%make_build

%if "%{tpls_libs}" == "shared"
%{tpls_cxx} -shared -o libstrumpack.so -Wl,--build-id $(find ./CMakeFiles/strumpack.dir -name *.o)
%endif

#%check
#%make_build test

%install
%make_install

%if "%{tpls_libs}" == "shared"
install -m 755 libstrumpack.so %{buildroot}%{tpls_prefix}/lib
%endif

%files
%{tpls_prefix}/include/BLR
%{tpls_prefix}/include/HODLR
%{tpls_prefix}/include/HSS
%{tpls_prefix}/include/SparseSolverBase.hpp
%{tpls_prefix}/include/StrumpackConfig.hpp
%{tpls_prefix}/include/StrumpackConfig.h
%{tpls_prefix}/include/StrumpackFortranCInterface.h
%{tpls_prefix}/include/StrumpackOptions.hpp
%{tpls_prefix}/include/StrumpackParameters.hpp
%{tpls_prefix}/include/StrumpackSparseSolver.h
%{tpls_prefix}/include/StrumpackSparseSolver.hpp
%{tpls_prefix}/include/StrumpackSparseSolverMPIDist.hpp
%{tpls_prefix}/include/StrumpackSparseSolverMixedPrecisionMPIDist.hpp
%{tpls_prefix}/include/clustering/Clustering.hpp
%{tpls_prefix}/include/clustering/NeighborSearch.hpp
%{tpls_prefix}/include/dense
%{tpls_prefix}/include/iterative
%{tpls_prefix}/include/kernel
%{tpls_prefix}/include/misc
%{tpls_prefix}/include/python/STRUMPACKKernel.py
%{tpls_prefix}/include/sparse
%{tpls_prefix}/include/structured
%{tpls_prefix}/include/strumpack.mod
%{tpls_prefix}/include/strumpack_dense.mod
%{tpls_prefix}/lib/cmake/STRUMPACK
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libstrumpack.a
%else
%exclude %{tpls_prefix}/lib/libstrumpack.a
%{tpls_prefix}/lib/libstrumpack.so
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 7.0.1-1
- Initial Package