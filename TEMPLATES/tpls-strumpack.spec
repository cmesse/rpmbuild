Name:           tpls-%{tpls_flavor}-strumpack
Version:        7.1.0
Release:        1%{?dist}
Summary:        STRUMPACK - STRUctured Matrix PACKage

License:        BSD-3-Clause
URL:            https://portal.nersc.gov/project/sparse/strumpack
Source0:        https://github.com/pghysels/STRUMPACK/archive/v%{version}.tar.gz

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
%endif

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
BuildRequires:  tpls-%{tpls_flavor}-scalapack
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-scalapack
%else
BuildRequires:  intel-oneapi-mpi-mkl
BuildRequires:  intel-oneapi-mpi-mkl-devel
Requires:       intel-oneapi-mpi-mkl
%endif

%description
STRUMPACK - STRUctured Matrix PACKage - is a software library providing linear algebra routines and linear system solvers for sparse and for dense rank-structured linear systems. Many large dense matrices are rank structured, meaning they exhibit some kind of low-rank property, for instance in hierarchically defined sub-blocks. In sparse direct solvers based on LU factorization, the LU factors can often also be approximated well using rank-structured matrix compression, leading to robust preconditioners. The sparse solver in STRUMPACK can also be used as an exact direct solver, in which case it functions similarly as for instance SuperLU or Superlu_Dist. The STRUMPACK sparse direct solver delivers good performance and distributed memory scalability and provides excellent CUDA support.

%prep
%setup -q -n STRUMPACK-%{version}

%build
%{tpls_env} %tpls_cmake  \
	-DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags} -I%{tpls_prefix}/include/zfp" \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -I%{tpls_prefix}/include/zfp" \
    -DCMAKE_Fortran_COMPILER=%{tpls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
%if "%{tpls_gpu}" == "lapack"
    -DSTRUMPACK_USE_CUDA=OFF \
    -DSTRUMPACK_USE_HIP=OFF \
    -DTPL_ENABLE_SLATE=OFF \
%elif "%{tpls_gpu}" == "cuda"
    -DSTRUMPACK_USE_CUDA=ON \
    -DSTRUMPACK_USE_HIP=OFF \
    -DTPL_ENABLE_SLATE=ON \
%elif "%{tpls_gpu}" == "rocm"
    -DSTRUMPACK_USE_CUDA=OFF \
    -DSTRUMPACK_USE_HIP=ON \
    -DTPL_ENABLE_SLATE=ON \
%endif
    -DSTRUMPACK_USE_SYCL=OFF \
    -DSTRUMPACK_USE_MPI=ON \
    -DTPL_ENABLE_BPACK=ON \
    -DTPL_ENABLE_PARMETIS=ON \
    -DTPL_ENABLE_SCOTCH=ON \
    -DTPL_ENABLE_PTSCOTCH=ON \
    -DTPL_ENABLE_ZFP=ON \
%if "%{tpls_int}" == "32"
    -DSTRUMPACK_USE_BLAS64=OFF \
%else
    -DSTRUMPACK_USE_BLAS64=ON \
%endif
    .

%make_build

#%check
#%make_build test

%install
%make_install

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
%{tpls_prefix}/include/dense/ACA.hpp
%{tpls_prefix}/include/dense/BACA.hpp
%{tpls_prefix}/include/dense/BLACSGrid.hpp
%{tpls_prefix}/include/dense/BLASLAPACKOpenMPTask.hpp
%{tpls_prefix}/include/dense/BLASLAPACKWrapper.hpp
%{tpls_prefix}/include/dense/DenseMatrix.hpp
%{tpls_prefix}/include/dense/DistributedMatrix.hpp
%{tpls_prefix}/include/dense/DistributedVector.hpp
%{tpls_prefix}/include/dense/ScaLAPACKWrapper.hpp
%{tpls_prefix}/include/iterative/IterativeSolvers.hpp
%{tpls_prefix}/include/iterative/IterativeSolversMPI.hpp
%{tpls_prefix}/include/kernel/Kernel.h
%{tpls_prefix}/include/kernel/Kernel.hpp
%{tpls_prefix}/include/kernel/KernelRegression.hpp
%{tpls_prefix}/include/kernel/Metrics.hpp
%{tpls_prefix}/include/misc/MPIWrapper.hpp
%{tpls_prefix}/include/misc/RandomWrapper.hpp
%{tpls_prefix}/include/misc/TaskTimer.hpp
%{tpls_prefix}/include/misc/Tools.hpp
%{tpls_prefix}/include/misc/Triplet.hpp
%{tpls_prefix}/include/python/STRUMPACKKernel.py
%{tpls_prefix}/include/sparse/CSRGraph.hpp
%{tpls_prefix}/include/sparse/CSRMatrix.hpp
%{tpls_prefix}/include/sparse/CSRMatrixMPI.hpp
%{tpls_prefix}/include/sparse/CompressedSparseMatrix.hpp
%{tpls_prefix}/include/structured/ClusterTree.hpp
%{tpls_prefix}/include/structured/StructuredMatrix.h
%{tpls_prefix}/include/structured/StructuredMatrix.hpp
%{tpls_prefix}/include/structured/StructuredMatrixMPI.h
%{tpls_prefix}/include/structured/StructuredOptions.hpp
%{tpls_prefix}/include/strumpack.mod
%{tpls_prefix}/include/strumpack_dense.mod
%{tpls_prefix}/lib/cmake/STRUMPACK
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libstrumpack.a
%else
%{tpls_prefix}/lib/libstrumpack.so
%{tpls_prefix}/lib/libstrumpack.so.*
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 7.0.1-1
- Initial Package