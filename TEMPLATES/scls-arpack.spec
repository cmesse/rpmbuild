%define scls_oflags -O3

Name:           scls-%{scls_flavor}-arpack
Version:        3.9.1
Release:        1%{?dist}
Summary:	    Fortran 77 subroutines for solving large scale eigenvalue problems

License:        BSD
URL:            https://github.com/opencollab/arpack-ng
Source0:       https://src.fedoraproject.org/lookaside/pkgs/arpack/arpack-ng-3.9.1.tar.gz/sha512/1ca590a8c4f75aa74402f9bd62e63851039687f4cb11afa8acb05fce1f22a512bff5fd1709ea85fdbea90b344fbbc01e3944c770b5ddc4d1aabc98ac334f78d2/arpack-ng-3.9.1.tar.gz

BuildRequires:  scls-%{scls_flavor}-cmake

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
ARPACK is a collection of Fortran 77 subroutines designed to solve large
scale eigenvalue problems.

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).

%prep
%setup -q -n arpack-ng-%{version}

%build

# Compiler Settings
%{expand: %setup_scls_env}
%{scls_env} \
CC=%{scls_mpicc} \
CXX=%{scls_mpicxx} \
FC=%{scls_mpifort} \
%{scls_cmake} \
	-DCMAKE_C_COMPILER=%{scls_mpicc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DCMAKE_Fortran_COMPILER=%{scls_mpifort} \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} %{scls_oflags}" \
    -DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
%if "%{scls_math}" == "lapack"
	-DBLAS_LIBRARIES=%{scls_blas} \
	-DLAPACK_LIBRARIES=%{scls_lapack} \
%else
	-DBLAS_LIBRARIES="%{scls_mkl_linker_flags}" \
	-DLAPACK_LIBRARIES="%{scls_mkl_linker_flags}" \
%endif
	-DMPI=ON \
%if "%{scls_index_size}" == "32"
	-DINTERFACE64=OFF \
%else
	-DINTERFACE64=ON \
%endif
%if "%{scls_libs}" == "static"
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DTESTS=OFF \
%else
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DTESTS=ON \
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mpiproot}/lib -Wl,-rpath,%{scls_mpiproot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mpiproot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif
%endif
    .

%make_build

%check
%if "%{scls_libs}" == "shared"
%if   "%{scls_math}"== "lapack"
PATH=%{scls_prefix}/bin:$PATH make %{?_smp_mflags} test
%else
LD_LIBRARY_PATH="%{scls_ld_library_path}" PATH=%{scls_prefix}/bin:$PATH make %{?_smp_mflags} test
%endif
%endif

%install
%make_install


%files
%{scls_prefix}/include/arpack/arpackdef.h
%{scls_prefix}/include/arpack/arpackicb.h
%{scls_prefix}/include/arpack/debug.h
%{scls_prefix}/include/arpack/debugF90.h
%{scls_prefix}/include/arpack/stat.h
%{scls_prefix}/include/arpack/statF90.h
%{scls_prefix}/lib/cmake/arpackng/arpackng-config-version.cmake
%{scls_prefix}/lib/cmake/arpackng/arpackng-config.cmake
%{scls_prefix}/lib/cmake/arpackng/arpackngTargets-release.cmake
%{scls_prefix}/lib/cmake/arpackng/arpackngTargets.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libarpack.a
%{scls_prefix}/lib/libparpack.a
%else
%{scls_prefix}/lib/libarpack.so
%{scls_prefix}/lib/libarpack.so.*
%{scls_prefix}/lib/libparpack.so
%{scls_prefix}/lib/libparpack.so.*
%endif
%{scls_prefix}/lib/pkgconfig/arpack.pc
%{scls_prefix}/lib/pkgconfig/parpack.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.9.1-1
- Initial Package
