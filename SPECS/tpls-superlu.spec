Name:           tpls-%{tpls_flavor}-superlu
Version:        6.0.1
Release:        1%{?dist}
Summary:        Subroutines to solve sparse linear systems


License:        BSD
URL:            https://github.com/xiaoyeli/superlu
Source0:        https://github.com/xiaoyeli/superlu/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-metis
Requires:       tpls-%{tpls_flavor}-metis

%description
SuperLU contains a set of subroutines to solve a sparse linear system
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP).
The columns of A may be preordered before factorization; the
preordering for sparsity is completely separate from the factorization.



%prep
%setup -q -n superlu-%{version}

%build

%{setup_tpls_env}

cmake \
	-DCMAKE-INSTALL-PREFIX=%{tpls_prefix} \
	-DCMAKE_BUILD_TYPE="Release" \
if "%{tpls_gpu} == "lapack"
	-DTPL_BLAS_LIBRARIES=%{tpls_blas} \
	-DTPL_BLAS_LIBRARIES=%{tpls_lapack} \
%else
	-DTPL_BLAS_LIBRARIES=%{mkl_linker_flags} \
	-DTPL_BLAS_LIBRARIES=%{mkl_linker_flags} \
%endif
	-DTPL_ENABLE_METISLIB=ON
	-DTPL_METIS_INCLUDE_DIRS=%{tpls_prefix}/include \
if "%{tpls-libs} == "static"
	-DTPL_METIS_LIBRARIES=%{tpls_prefix}/lib/libmetis.a \
%else
	-DTPL_METIS_LIBRARIES=%{tpls_prefix}/lib/libmetis.so \
%endif
	-Denable_fortran=ON \
	-Denable_internal_blaslib=OFF \
	.
	
%install


%files


%changelog
* [date] [packager] - [version]-1
- Initial package.
