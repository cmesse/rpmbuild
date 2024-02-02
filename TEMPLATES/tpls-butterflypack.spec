Name:           tpls-%{tpls_flavor}-butterflypack
Version:        2.4.0
Release:        1%{?dist}
Summary:        rapid solving of large-scale dense linear systems

License:        BSD-3-Clause
URL:            https://github.com/liuyangzhuan/ButterflyPACK
Source0:        https://github.com/liuyangzhuan/ButterflyPACK/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake

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

%description
ButterflyPACK is a mathematical software for rapidly solving large-scale dense linear systems that exhibit off-diagonal rank-deficiency. These systems arise frequently from boundary element methods, or factorization phases in finite-difference/finite-element methods. ButterflyPACK relies on low-rank or butterfly formats under Hierarchical matrix, HODLR or other hierarchically nested frameworks to compress, factor and solve the linear system in quasi-linear time. The computationally most intensive phase, factorization, is accelerated via randomized linear algebras. The butterfly format, originally inspired by the butterfly data flow in fast Fourier Transform, is a linear algebra tool well-suited for compressing matrices arising from high-frequency wave equations or highly oscillatory integral operators. ButterflyPACK also provides preconditioned TFQMR iterative solvers.

ButterflyPACK is written in Fortran 2003, it also has C++ interfaces. ButterflyPACK supports hybrid MPI/OpenMP programming models. In addition, ButterflyPACK can be readily invoked from the software STRUMPACK for solving dense and sparse linear systems.

%prep
%setup -q -n ButterflyPACK-%{version}

%build
mkdir build && cd build
%{tpls_env} %{tpls_cmake}  \
	-DCMAKE_C_COMPILER=%{tpls_mpicc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
    -DCMAKE_Fortran_COMPILER=%{tpls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
%if "%{tpls_gpu}" == "lapack"
    -DTPL_BLAS_LIBRARIES=%{tpls_blas} \
	-DTPL_LAPACK_LIBRARIES=%{tpls_lapack} \
	-DTPL_SCALAPACK_LIBRARIES=%{tpls_scalapack} \
%else
    -DTPL_BLAS_LIBRARIES="%{tpls_mkl_linker_flags}" \
	-DTPL_LAPACK_LIBRARIES="%{tpls_mkl_linker_flags}" \
	-DTPL_SCALAPACK_LIBRARIES="%{tpls_mkl_mpi_linker_flags}" \
%endif
    -DTPL_ARPACK_LIBRARIES=%{tpls_arpack} \
%if "%{tpls_libs}" == "static"
    -DBUILD_SHARED_LIBS=OFF \
%else
    -DBUILD_SHARED_LIBS=ON \
%endif
%if "%{tpls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib %{tpls_parpack} %{tpls_arpack}" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib %{tpls_parpack} %{tpls_arpack}" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib %{tpls_parpack} %{tpls_arpack}" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib %{tpls_parpack} %{tpls_arpack}" \
%endif
    ..

%if "%{tpls_compiler}" == "intel"
make
%else
%make_build
%endif

%install
cd build
%make_install

%files
%{tpls_prefix}/include/ButterflyPACK_config.fi
%{tpls_prefix}/include/*ButterflyPACK_config.fi
%{tpls_prefix}/include/*C_BPACK_wrapper.h
%{tpls_prefix}/include/*_bpack_*.mod
%{tpls_prefix}/include/*_bplus_*.mod
%{tpls_prefix}/include/*_magma_utilities.mod
%{tpls_prefix}/include/*_misc_*.mod
%{tpls_prefix}/lib/EXAMPLE/ie*
%{tpls_prefix}/lib/cmake/ButterflyPACK/butterflypack-*.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/lib*butterflypack.a
%else
%{tpls_prefix}/lib/lib*butterflypack.so
%{tpls_prefix}/lib/lib*butterflypack.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/butterflypack.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.4.0-1
- Initial Package
