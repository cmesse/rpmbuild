%define scls_oflags -O3

Name:           scls-%{scls_flavor}-sundials
Version:        6.7.0
Release:        1%{?dist}
Summary:        Nonlinear and DIfferential/ALgebraic Equation Solvers

License:        BSD-3-Clause

URL:            https://www.llnl.gov/casc/sundials/
Source0:        https://github.com/LLNL/sundials/releases/download/v%{version}/sundials-%{version}.tar.gz

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%if "%{scls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{scls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{scls_comp_minver}
%endif

BuildRequires:  scls-%{scls_flavor}-suitesparse
Requires:       scls-%{scls_flavor}-suitesparse

%description
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.

SUNDIALS was implemented with the goal of providing robust time integrators
and nonlinear solvers that can easily be incorporated into existing simulation
codes. The primary design goals were to require minimal information from the
user, allow users to easily supply their own data structures underneath the
solvers, and allow for easy incorporation of user-supplied linear solvers and
preconditioners.

%package examples
Summary:       Example files for SUNDIALS
Requires:      scls-%{scls_flavor}-sundials == %{version}

%description examples
Example files for SUNDIALS


%prep
%setup -q -n sundials-%{version}

%build

%if "%{scls_libs}" == "static"
for f in ./CMakeLists.txt ./cmake/tpl/FindMAGMA.cmake ./cmake/SUNDIALSConfig.cmake.in ./src/sunlinsol/cusolversp/CMakeLists.txt ./src/sunmatrix/cusparse/CMakeLists.txt ; do
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart_static.a|g" $f
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas_static.a|g" $f
    sed -i "s|CUDA::cusolver|%{scls_cudamath}/lib64/libcusolver_static.a|g" $f
    sed -i "s|CUDA::cusparse|%{scls_cudamath}/lib64/libcusparse_static.a|g" $f
done
%else
for f in ./CMakeLists.txt ./cmake/tpl/FindMAGMA.cmake ./cmake/SUNDIALSConfig.cmake.in ./src/sunlinsol/cusolversp/CMakeLists.txt ./src/sunmatrix/cusparse/CMakeLists.txt ; do
    sed -i "s|CUDA::cudart|%{scls_cuda}/lib64/libcudart.so|g"  $f
    sed -i "s|CUDA::cublas|%{scls_cudamath}/lib64/libcublas.so|g"  $f
    sed -i "s|CUDA::cusolver|%{scls_cudamath}/lib64/libcusolver.so|g" $f
    sed -i "s|CUDA::cusparse|%{scls_cudamath}/lib64/libcusparse.so|g" $f
done
%endif

%{expand: %setup_scls_env}

mkdir build && cd build
%{scls_env} \
LDFLAGS+="%{scls_strumpack} %{scls_slate}  %{scls_sbutterflypack} %{scls_dbutterflypack} %{scls_zbutterflypack} %{scls_cbutterflypack} %{scls_zfp}  %{scls_ptscotch} %{scls_ptscotcherr} %{scls_ptscotcherrexit} %{scls_scotch} %{scls_scotcherr} %{scls_scotcherrexit} %{scls_parmetis} %{scls_metis}" \
%{scls_cmake} \
	-DCMAKE_C_COMPILER=%{scls_mpicc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%endif
%if "%{scls_math}" == "cuda"
    -DENABLE_CUDA=ON \
	-DCMAKE_CUDA_COMPILER=%{scls_nvcc} \
%if "%{scls_compiler}" == "intel"
	-DCMAKE_CUDA_FLAGS="%{scls_nvccflags} -allow-unsupported-compiler" \
%else
	-DCMAKE_CUDA_FLAGS="%{scls_nvccflags}" \
%endif   "%{scls_nvccflags}" \
	-DCMAKE_CUDA_ARCHITECTURES="%{scls_cuda_architectures}" \
%endif
    -DSUNDIALS_INSTALL_CMAKEDIR=lib/cmake/sundials \
    -DENABLE_MPI=ON \
    -DENABLE_OPENMP=ON \
    -DENABLE_PETSC=OFF \
    -DENABLE_KLU=ON  \
    -DEXAMPLES_ENABLE_C=ON \
    -DEXAMPLES_ENABLE_CXX=ON \
    -DEXAMPLES_INSTALL=ON \
    -DEXAMPLES_INSTALL_PATH=%{scls_prefix}/share/sundials \
%if "%{scls_index_size}" == "32"
    -DSUNDIALS_INDEX_SIZE=32 \
%else
    -DSUNDIALS_INDEX_SIZE=64 \
%if "%{scls_math}" != "lapack"
    -DENABLE_ONEMKL=ON \
%endif
%endif
    -DSUNDIALS_TEST_UNITTESTS=ON \
%if "%{scls_libs}" == "shared"
%if "%{scls_math}" == "lapack"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{scls_scotch} %{scls_slate}  -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib %{scls_scotch} %{scls_slate}  -llzma -lbz2 -lz" \
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
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib  -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64 -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
%endif
%else
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib  -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_mpiroot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib % -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib  -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib -llzma -lbz2 -lz" \
%endif
%else
    -DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mklroot}/lib -Wl,-rpath,%{scls_mklroot}/lib -llzma -lbz2 -lz" \
%endif
%endif
%endif
%endif
    -DKLU_INCLUDE_DIR=%{scls_prefix}/include/suitesparse \
%if "%{scls_libs}" == "static"
    -DKLU_LIBRARY=%{scls_prefix}/lib/libklu.a \
%else
    -DKLU_LIBRARY=%{scls_prefix}/lib/libklu.so \
%endif
    ..

%make_build

%check
cd build
%make_build test

%install
cd build
%make_install

%files
%{scls_prefix}/include/arkode
%{scls_prefix}/include/cvode
%{scls_prefix}/include/cvodes
%{scls_prefix}/include/ida
%{scls_prefix}/include/idas
%{scls_prefix}/include/kinsol
%{scls_prefix}/include/nvector
%{scls_prefix}/include/sunadaptcontroller
%{scls_prefix}/include/sundials
%{scls_prefix}/include/sundials
%{scls_prefix}/include/sunlinsol
%{scls_prefix}/include/sunmatrix
%{scls_prefix}/include/sunmemory
%{scls_prefix}/include/sunnonlinsol
%{scls_prefix}/lib/cmake/sundials
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libsundials_*.a
%else
%{scls_prefix}/lib/libsundials_*.so
%{scls_prefix}/lib/libsundials_*.so.*
%endif

%files examples
%{scls_prefix}/share/sundials

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 6.7.0-1
- Initial Package

