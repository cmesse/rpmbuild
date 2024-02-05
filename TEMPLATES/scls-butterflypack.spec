%define scls_oflags -O2

Name:           scls-%{scls_flavor}-butterflypack
Version:        2.4.0
Release:        1%{?dist}
Summary:        rapid solving of large-scale dense linear systems

License:        BSD-3-Clause
URL:            https://github.com/liuyangzhuan/ButterflyPACK
Source0:        https://github.com/liuyangzhuan/ButterflyPACK/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  scls-%{scls_flavor}-arpack

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
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

%description
ButterflyPACK is a mathematical software for rapidly solving large-scale dense linear systems that exhibit off-diagonal rank-deficiency. These systems arise frequently from boundary element methods, or factorization phases in finite-difference/finite-element methods. ButterflyPACK relies on low-rank or butterfly formats under Hierarchical matrix, HODLR or other hierarchically nested frameworks to compress, factor and solve the linear system in quasi-linear time. The computationally most intensive phase, factorization, is accelerated via randomized linear algebras. The butterfly format, originally inspired by the butterfly data flow in fast Fourier Transform, is a linear algebra tool well-suited for compressing matrices arising from high-frequency wave equations or highly oscillatory integral operators. ButterflyPACK also provides preconditioned TFQMR iterative solvers.

ButterflyPACK is written in Fortran 2003, it also has C++ interfaces. ButterflyPACK supports hybrid MPI/OpenMP programming models. In addition, ButterflyPACK can be readily invoked from the software STRUMPACK for solving dense and sparse linear systems.

%prep
%setup -q -n ButterflyPACK-%{version}

%build
mkdir build && cd build
%{scls_env} %{scls_cmake}  \
    -DBUILD_TESTING=OFF \
	-DCMAKE_C_COMPILER=%{scls_mpicc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
    -DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
%if "%{scls_math}" == "lapack"
    -DTPL_BLAS_LIBRARIES=%{scls_blas} \
	-DTPL_LAPACK_LIBRARIES=%{scls_lapack} \
	-DTPL_SCALAPACK_LIBRARIES=%{scls_scalapack} \
%else
    -DTPL_BLAS_LIBRARIES="%{scls_mkl_linker_flags}" \
	-DTPL_LAPACK_LIBRARIES="%{scls_mkl_linker_flags}" \
	-DTPL_SCALAPACK_LIBRARIES="%{scls_mkl_mpi_linker_flags}" \
%endif
    -DTPL_ARPACK_LIBRARIES="%{scls_parpack};%{scls_arpack}" \
%if "%{scls_libs}" == "static"
    -DBUILD_SHARED_LIBS=OFF \
%else
    -DBUILD_SHARED_LIBS=ON \
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

make

%install
cd build
%make_install

%files
%{scls_prefix}/include/ButterflyPACK_config.fi
%{scls_prefix}/include/*ButterflyPACK_config.fi
%{scls_prefix}/include/*C_BPACK_wrapper.h
%{scls_prefix}/include/*_bpack_*.mod
%{scls_prefix}/include/*_bplus_*.mod
%{scls_prefix}/include/*_magma_utilities.mod
%{scls_prefix}/include/*_misc_*.mod
%{scls_prefix}/lib/EXAMPLE/ie*
%{scls_prefix}/lib/cmake/ButterflyPACK/butterflypack-*.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/lib*butterflypack.a
%else
%{scls_prefix}/lib/lib*butterflypack.so
%{scls_prefix}/lib/lib*butterflypack.so.*
%endif
%{scls_prefix}/lib/pkgconfig/butterflypack.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.4.0-1
- Initial Package
