%define scls_oflags -O3

Name:           scls-%{scls_flavor}-strumpack
Version:        7.1.0
Release:        1%{?dist}
Summary:        linear algebra routines and linear system solvers for sparse and for dense rank-structured linear systems.

License:        BSD-3-Clause
URL:            https://portal.nersc.gov/project/sparse/strumpack
Source0:        https://github.com/pghysels/STRUMPACK/archive/v%{version}.tar.gz
Patch0:         strumpack_no_scalapack_check.patch

BuildRequires:  %{scls_rpm_cc}   >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_cxx}  >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_fc}   >= %{scls_comp_minver}

%if "%{scls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{scls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{scls_comp_minver}
%endif

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  scls-%{scls_flavor}-metis
BuildRequires:  scls-%{scls_flavor}-parmetis
BuildRequires:  scls-%{scls_flavor}-scotch
BuildRequires:  scls-%{scls_flavor}-zfp
BuildRequires:  scls-%{scls_flavor}-butterflypack


%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
BuildRequires:  scls-%{scls_flavor}-slate
Requires:       scls-%{scls_flavor}-slate
%endif

%if "%{scls_math}" == "lapack"
BuildRequires:  scls-%{scls_flavor}-blas
BuildRequires:  scls-%{scls_flavor}-lapack
BuildRequires:  scls-%{scls_flavor}-scalapack
Requires:       scls-%{scls_flavor}-blas
Requires:       scls-%{scls_flavor}-lapack
Requires:       scls-%{scls_flavor}-scalapack
%else
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%endif

BuildRequires:  libquadmath
BuildRequires:  libquadmath-devel
Requires:       libquadmath
BuildRequires:  xz
BuildRequires:  xz-devel
Requires:       xz

%description
STRUMPACK - STRUctured Matrix PACKage - is a software library providing linear algebra routines and linear system solvers for sparse and for dense rank-structured linear systems. Many large dense matrices are rank structured, meaning they exhibit some kind of low-rank property, for instance in hierarchically defined sub-blocks. In sparse direct solvers based on LU factorization, the LU factors can often also be approximated well using rank-structured matrix compression, leading to robust preconditioners. The sparse solver in STRUMPACK can also be used as an exact direct solver, in which case it functions similarly as for instance SuperLU or Superlu_Dist. The STRUMPACK sparse direct solver delivers good performance and distributed memory scalability and provides excellent CUDA support.

%prep
%setup -q -n STRUMPACK-%{version}
%patch0 -p1

%if "%{scls_libs}" == "static"
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart_static.a|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas_static.a -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{scls_prefix}/lib/liblapackpp.a %{scls_prefix}/lib/libblaspp.a  %{scls_cudamath}/lib64/libcusolver_static.a|g" CMakeLists.txt
%else
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart.so|g" CMakeLists.txt
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas.so -llzma -lbz2 -lz|g" CMakeLists.txt
    sed -i "s|CUDA::cusolver|%{scls_prefix}/lib/liblapackpp.so %{scls_prefix}/lib/libblaspp.so %{scls_cudamath}/lib64/libcusolver.so|g" CMakeLists.txt
%endif

%if "%{scls_mpi}" != "openmpi"
    sed -i 's| --oversubscribe ||g' .ci_tests.sh
    sed -i 's|set(OVERSUBSCRIBEFLAG "--oversubscribe")|set(OVERSUBSCRIBEFLAG "")|g' test/CMakeLists.txt
%endif

%build
%{scls_env} \
%if "%{scls_math}" == "lapack"
LDFLAGS="%{scls_scalapack} %{scls_lapack} %{scls_blas} %{scls_mpilibs}" \
%else
LDFLAGS="%{scls_mkl_mpi_linker_flags} %{scls_mpilibs}" \
%endif
%{scls_cmake}  \
    -DBUILD_TESTING=ON \
	-DCMAKE_C_COMPILER=%{scls_mpicc} \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
%if "%{scls_math}" == "cuda"
    -DSTRUMPACK_USE_CUDA=ON \
    -DCMAKE_CUDA_COMPILER=%{scls_nvcc} \
    -DCMAKE_CUDA_FLAGS="%{scls_nvccflags}" \
	-DCMAKE_CUDA_ARCHITECTURES="%{scls_cuda_architectures}" \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags} -I%{scls_prefix}/include/zfp -I%{scls_cudamath}/include -I%{scls_cuda}/include" \
    -DCMAKE_CXX_FLAGS="%{scls_cflags} %{scls_oflags} -I%{scls_prefix}/include/zfp -I%{scls_cudamath}/include -I%{scls_cuda}/include" \
%else
    -DSTRUMPACK_USE_CUDA=OFF \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags} -I%{scls_prefix}/include/zfp" \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags} -I%{scls_prefix}/include/zfp" \
%endif
    -DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags}" \
    -DSTRUMPACK_USE_HIP=OFF \
    -DTPL_ENABLE_SLATE=ON \
    -DSTRUMPACK_USE_SYCL=OFF \
    -DSTRUMPACK_USE_MPI=ON \
    -DTPL_ENABLE_BPACK=ON \
    -DTPL_ENABLE_PARMETIS=ON \
    -DTPL_ENABLE_SCOTCH=ON \
    -DTPL_ENABLE_PTSCOTCH=ON \
    -DTPL_ENABLE_ZFP=ON \
%if "%{scls_libs}" == "shared"
%if "%{scls_math}" == "lapack"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -llzma -lbz2 -lz" \
%endif
%if "%{scls_math}" == "cuda"
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
%endif
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
%endif
%else
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
%endif
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
%endif
%endif
%endif
%if "%{scls_index_size}" == "32"
    -DSTRUMPACK_USE_BLAS64=OFF \
%else
    -DSTRUMPACK_USE_BLAS64=ON \
%endif
    .

# fix the cuda settings
%if "%{scls_math}" == "cuda"
%{scls_cmake}  \
    -DCMAKE_CUDA_ARCHITECTURES="61;70;75;80;86" \
    -DCMAKE_C_FLAGS="%{scls_cflags} -I%{scls_prefix}/include/zfp -I%{scls_cudamath}/include -I%{scls_cuda}/include" \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} -I%{scls_prefix}/include/zfp -I%{scls_cudamath}/include -I%{scls_cuda}/include" \
    -DCMAKE_CUDA_FLAGS="-I%{scls_cudamath}/include -I%{scls_cuda}/include" \
    -DSTRUMPACK_USE_CUDA=ON \
    -DTPL_ENABLE_SLATE=ON \
    -Dblaspp_DIR=%{scls_prefix}/lib/cmake/blaspp \
    -Dlapackpp_DIR=%{scls_prefix}/lib/cmake/lapackpp \
    -Dslate_DIR=%{scls_prefix}/lib/cmake/slate \
    .
%endif

%make_build

%if "%{scls_libs}" == "shared"
%{scls_cxx} %{scls_ldflags} -shared -o libstrumpack.so -Wl,--build-id $(find ./CMakeFiles/strumpack.dir -name *.o)
%endif

#%check
#%make_build test

%install
%make_install

%if "%{scls_libs}" == "shared"
install -m 755 libstrumpack.so %{buildroot}%{scls_prefix}/lib
%endif

%files
%{scls_prefix}/include/BLR
%{scls_prefix}/include/HODLR
%{scls_prefix}/include/HSS
%{scls_prefix}/include/SparseSolverBase.hpp
%{scls_prefix}/include/StrumpackConfig.hpp
%{scls_prefix}/include/StrumpackConfig.h
%{scls_prefix}/include/StrumpackFortranCInterface.h
%{scls_prefix}/include/StrumpackOptions.hpp
%{scls_prefix}/include/StrumpackParameters.hpp
%{scls_prefix}/include/StrumpackSparseSolver.h
%{scls_prefix}/include/StrumpackSparseSolver.hpp
%{scls_prefix}/include/StrumpackSparseSolverMPIDist.hpp
%{scls_prefix}/include/StrumpackSparseSolverMixedPrecisionMPIDist.hpp
%{scls_prefix}/include/clustering/Clustering.hpp
%{scls_prefix}/include/clustering/NeighborSearch.hpp
%{scls_prefix}/include/dense
%{scls_prefix}/include/iterative
%{scls_prefix}/include/kernel
%{scls_prefix}/include/misc
%{scls_prefix}/include/python/STRUMPACKKernel.py
%{scls_prefix}/include/sparse
%{scls_prefix}/include/structured
%{scls_prefix}/include/strumpack.mod
%{scls_prefix}/include/strumpack_dense.mod
%{scls_prefix}/lib/cmake/STRUMPACK
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libstrumpack.a
%else
%exclude %{scls_prefix}/lib/libstrumpack.a
%{scls_prefix}/lib/libstrumpack.so
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 7.0.1-1
- Initial Package