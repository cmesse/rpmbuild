%define scls_oflags -O2

Name:           scls-%{scls_flavor}-suitesparse
Version:        7.6.0
Release:        1%{?dist}
Summary:        A collection of sparse matrix libraries

License:        (LGPLv2+ or BSD) and LGPLv2+ and GPLv2+
URL:            http://faculty.cse.tamu.edu/davis/suitesparse.html
Source0:        https://github.com/DrTimothyAldenDavis/SuiteSparse/archive/refs/tags/v%{version}.tar.gz


BuildRequires:  %{scls_rpm_cc}   >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_cxx}  >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_fc}   >= %{scls_comp_minver}

%if "%{scls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{scls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{scls_comp_minver}
%endif

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  scls-%{scls_flavor}-gmp
BuildRequires:  scls-%{scls_flavor}-mpfr
BuildRequires:  scls-%{scls_flavor}-metis
Requires:  scls-%{scls_flavor}-gmp
Requires:  scls-%{scls_flavor}-mpfr
Requires:  scls-%{scls_flavor}-metis

%description
suitesparse is a collection of libraries for computations involving sparse
matrices.  The package includes the following libraries:
  AMD                 approximate minimum degree ordering
  BTF                 permutation to block triangular form (beta)
  CAMD                constrained approximate minimum degree ordering
  COLAMD              column approximate minimum degree ordering
  CCOLAMD             constrained column approximate minimum degree ordering
  CHOLMOD             sparse Cholesky factorization
  CSparse             a concise sparse matrix package
  CXSparse            CSparse extended: complex matrix, int and long int support
  KLU                 sparse LU factorization, primarily for circuit simulation
  LDL                 a simple LDL factorization
  SQPR                a multithread, multifrontal, rank-revealing sparse QR
                      factorization method
  UMFPACK             sparse LU factorization
  SuiteSparse_config  configuration file for all the above packages.
  RBio                read/write files in Rutherford/Boeing format

%prep
%setup -q -n SuiteSparse-%{version}

%build

%{expand: %setup_scls_env}


%{scls_env} %scls_cmake  \
	-DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_fc} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
%if "%{scls_math}" == "lapack"
	-DBLA_VENDOR="Generic" \
%elif "%{scls_cc}" == "nvc"
	-DBLA_VENDOR="NVHPC" \
%elif "%{scls_index_size}" == "32"
	-DBLA_VENDOR="Intel10_64lp" \
%else
	-DBLA_VENDOR="Intel10_64ilp" \
%endif
%if "%{scls_libs}" == "static"
	-DBLA_STATIC=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DBUILD_STATIC_LIBS=ON \
%else
	-DBLA_STATIC=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_STATIC_LIBS=OFF \
%if "%{scls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif
%endif
%if "%{scls_math}" != "cuda"
	-DSUITESPARSE_USE_CUDA=OFF \
%else
	-DSUITESPARSE_USE_CUDA=ON \
%endif
%if "%{scls_index_size}" == "32"
	-DSUITESPARSE_USE_64BIT_BLAS=OFF \
%else
	-DSUITESPARSE_USE_64BIT_BLAS=ON \
%endif
	-DBUILD_TESTING=ON \
	.

%make_build

%check
%if "%{scls_math}" == "lapack"
%make_build test
%else
LD_LIBRARY_PATH=%{scls_ld_library_path} %make_build test
%endif

%install
%make_install
%{scls_remove_la_files}

%files
%{scls_prefix}/bin/suitesparse_mongoose
%{scls_prefix}/include/suitesparse
%{scls_prefix}/lib/cmake/AMD
%{scls_prefix}/lib/cmake/BTF
%{scls_prefix}/lib/cmake/CAMD
%{scls_prefix}/lib/cmake/CCOLAMD
%{scls_prefix}/lib/cmake/CHOLMOD
%{scls_prefix}/lib/cmake/COLAMD
%{scls_prefix}/lib/cmake/CXSparse
%{scls_prefix}/lib/cmake/GraphBLAS
%{scls_prefix}/lib/cmake/KLU
%{scls_prefix}/lib/cmake/KLU_CHOLMOD
%{scls_prefix}/lib/cmake/LAGraph
%{scls_prefix}/lib/cmake/LDL
%{scls_prefix}/lib/cmake/ParU
%{scls_prefix}/lib/cmake/RBio
%{scls_prefix}/lib/cmake/SPEX
%{scls_prefix}/lib/cmake/SPQR
%{scls_prefix}/lib/cmake/SuiteSparse
%{scls_prefix}/lib/cmake/UMFPACK
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libamd.a
%{scls_prefix}/lib/libbtf.a
%{scls_prefix}/lib/libcamd.a
%{scls_prefix}/lib/libccolamd.a
%{scls_prefix}/lib/libcholmod.a
%{scls_prefix}/lib/libcolamd.a
%{scls_prefix}/lib/libcxsparse.a
%{scls_prefix}/lib/libgraphblas.a
%{scls_prefix}/lib/libklu.a
%{scls_prefix}/lib/libklu_cholmod.a
%{scls_prefix}/lib/liblagraph.a
%{scls_prefix}/lib/liblagraphx.a
%{scls_prefix}/lib/libldl.a
%{scls_prefix}/lib/libparu.a
%{scls_prefix}/lib/librbio.a
%{scls_prefix}/lib/libspex.a
%{scls_prefix}/lib/libspqr.a
%{scls_prefix}/lib/libsuitesparse_mongoose.a
%{scls_prefix}/lib/libsuitesparseconfig.a
%{scls_prefix}/lib/libumfpack.a
%else
%{scls_prefix}/lib/libamd.so
%{scls_prefix}/lib/libamd.so.*
%{scls_prefix}/lib/libbtf.so
%{scls_prefix}/lib/libbtf.so.*
%{scls_prefix}/lib/libcamd.so
%{scls_prefix}/lib/libcamd.so.*
%{scls_prefix}/lib/libccolamd.so
%{scls_prefix}/lib/libccolamd.so.*
%{scls_prefix}/lib/libcholmod.so
%{scls_prefix}/lib/libcholmod.so.*
%{scls_prefix}/lib/libcolamd.so
%{scls_prefix}/lib/libcolamd.so.*
%{scls_prefix}/lib/libcxsparse.so
%{scls_prefix}/lib/libcxsparse.so.*
%{scls_prefix}/lib/libgraphblas.so
%{scls_prefix}/lib/libgraphblas.so.*
%{scls_prefix}/lib/libklu.so
%{scls_prefix}/lib/libklu.so.*
%{scls_prefix}/lib/libklu_cholmod.so
%{scls_prefix}/lib/libklu_cholmod.so.*
%{scls_prefix}/lib/liblagraph.so
%{scls_prefix}/lib/liblagraph.so.*
%{scls_prefix}/lib/liblagraphx.so
%{scls_prefix}/lib/liblagraphx.so.*
%{scls_prefix}/lib/libldl.so
%{scls_prefix}/lib/libldl.so.*
%{scls_prefix}/lib/libparu.so
%{scls_prefix}/lib/libparu.so.*
%{scls_prefix}/lib/librbio.so
%{scls_prefix}/lib/librbio.so.*
%{scls_prefix}/lib/libspex.so
%{scls_prefix}/lib/libspex.so.*
%{scls_prefix}/lib/libspqr.so
%{scls_prefix}/lib/libspqr.so.*
%{scls_prefix}/lib/libsuitesparse_mongoose.so
%{scls_prefix}/lib/libsuitesparse_mongoose.so.*
%{scls_prefix}/lib/libsuitesparseconfig.so
%{scls_prefix}/lib/libsuitesparseconfig.so.*
%{scls_prefix}/lib/libumfpack.so
%{scls_prefix}/lib/libumfpack.so.*
%endif
%{scls_prefix}/lib/pkgconfig/AMD.pc
%{scls_prefix}/lib/pkgconfig/BTF.pc
%{scls_prefix}/lib/pkgconfig/CAMD.pc
%{scls_prefix}/lib/pkgconfig/CCOLAMD.pc
%{scls_prefix}/lib/pkgconfig/CHOLMOD.pc
%{scls_prefix}/lib/pkgconfig/COLAMD.pc
%{scls_prefix}/lib/pkgconfig/CXSparse.pc
%{scls_prefix}/lib/pkgconfig/GraphBLAS.pc
%{scls_prefix}/lib/pkgconfig/KLU.pc
%{scls_prefix}/lib/pkgconfig/KLU_CHOLMOD.pc
%{scls_prefix}/lib/pkgconfig/LAGraph.pc
%{scls_prefix}/lib/pkgconfig/LDL.pc
%{scls_prefix}/lib/pkgconfig/ParU.pc
%{scls_prefix}/lib/pkgconfig/RBio.pc
%{scls_prefix}/lib/pkgconfig/SPEX.pc
%{scls_prefix}/lib/pkgconfig/SPQR.pc
%{scls_prefix}/lib/pkgconfig/SuiteSparse_Mongoose.pc
%{scls_prefix}/lib/pkgconfig/SuiteSparse_config.pc
%{scls_prefix}/lib/pkgconfig/UMFPACK.pc
%{scls_prefix}/lib/cmake/SuiteSparse_Mongoose
%{scls_prefix}/lib/cmake/SuiteSparse_config

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 7.5.1-1
- Initial Package
