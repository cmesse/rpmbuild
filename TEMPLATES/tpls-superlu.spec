Name:           tpls-%{tpls_flavor}-superlu
Version:        6.0.1
Release:        1%{?dist}
Summary:        Subroutines to solve sparse linear systems


License:        BSD
URL:            https://github.com/xiaoyeli/superlu
Source0:        https://github.com/xiaoyeli/superlu/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-metis
Requires:       tpls-%{tpls_flavor}-metis
AutoReqProv:   %{tpls_auto_req_prov}

%description
SuperLU contains a set of subroutines to solve a sparse linear system
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP).
The columns of A may be preordered before factorization; the
preordering for sparsity is completely separate from the factorization.



%prep
%setup -q -n superlu-%{version}

%build

cmake \
	-DCMAKE_INSTALL_PREFIX=%{tpls_prefix} \
	-DCMAKE_BUILD_TYPE="Release" \
%if "%{tpls_libs}" == "static"
    -DCMAKE_C_FLAGS="%{tpls_cflags} -DNDEBUG" \
    -DCMAKE_C_FLAGS_RELEASE="%{tpls_cflags} -DNDEBUG" \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -DNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{tpls_cxxflags} -DNDEBUG" \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags} -DNDEBUG" \
    -DCMAKE_Fortran_FLAGS_RELEASE="%{tpls_fcflags} -DNDEBUG" \
%else
    -DCMAKE_C_FLAGS="%{tpls_cflags} -fPIC -DNDEBUG" \
    -DCMAKE_C_FLAGS_RELEASE="%{tpls_cflags}  -fPIC -DNDEBUG" \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags} -fPIC -DNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{tpls_cxxflags} -fPIC -DNDEBUG" \
        -DCMAKE_Fortran_FLAGS="%{tpls_fcflags} -fPIC -DNDEBUG" \
    -DCMAKE_Fortran_FLAGS_RELEASE="%{tpls_fcflags} -fPIC -DNDEBUG" \
%endif
	-DCMAKE_INSTALL_LIBDIR=lib \
%if "%{tpls_gpu}" == "lapack"
	-DTPL_BLAS_LIBRARIES=%{tpls_blas} \
	-DTPL_BLAS_LIBRARIES=%{tpls_lapack} \
%else
	-DTPL_BLAS_LIBRARIES=%{mkl_linker_flags} \
	-DTPL_BLAS_LIBRARIES=%{mkl_linker_flags} \
%endif
	-DTPL_ENABLE_METISLIB=ON \
	-DTPL_METIS_INCLUDE_DIRS=%{tpls_prefix}/include \
%if "%{tpls-libs}" == "static"
	-DTPL_METIS_LIBRARIES=%{tpls_prefix}/lib/libmetis.a \
%else
	-DTPL_METIS_LIBRARIES=%{tpls_prefix}/lib/libmetis.so \
%endif
	-Denable_fortran=ON \
	-Denable_internal_blaslib=OFF \
	.

%make_build

# manually create shared libs
%{tpls_cc} -shared -o ./SRC/libsuperlu.so ./SRC/CMakeFiles/superlu.dir/*.o
%{tpls_fc} -shared -o ./FORTRAN/libsuperlu_fortran.so ./FORTRAN/CMakeFiles/superlu_fortran.dir/*.o

%check
make test

%install
%make_install
install ./SRC/libsuperlu.so %{buildroot}/%{tpls_prefix}/lib/
install ./FORTRAN/libsuperlu_fortran.so %{buildroot}/%{tpls_prefix}/lib/

%files
%{tpls_prefix}/include/slu_Cnames.h
%{tpls_prefix}/include/slu_cdefs.h
%{tpls_prefix}/include/slu_dcomplex.h
%{tpls_prefix}/include/slu_ddefs.h
%{tpls_prefix}/include/slu_scomplex.h
%{tpls_prefix}/include/slu_sdefs.h
%{tpls_prefix}/include/slu_util.h
%{tpls_prefix}/include/slu_zdefs.h
%{tpls_prefix}/include/superlu_config.fh
%{tpls_prefix}/include/superlu_config.h
%{tpls_prefix}/include/superlu_enum_consts.h
%{tpls_prefix}/include/supermatrix.h
%{tpls_prefix}/lib/cmake/superlu/superluConfig.cmake
%{tpls_prefix}/lib/cmake/superlu/superluConfigVersion.cmake
%{tpls_prefix}/lib/cmake/superlu/superluTargets-release.cmake
%{tpls_prefix}/lib/cmake/superlu/superluTargets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libsuperlu.a
%{tpls_prefix}/lib/libsuperlu_fortran.a
%exclude %{tpls_prefix}/lib/libsuperlu.so
%exclude %{tpls_prefix}/lib/libsuperlu_fortran.so
%{tpls_prefix}/lib/pkgconfig/superlu.pc
%else
%exclude %{tpls_prefix}/lib/libsuperlu.a
%exclude %{tpls_prefix}/lib/libsuperlu_fortran.a
%{tpls_prefix}/lib/libsuperlu.so
%{tpls_prefix}/lib/libsuperlu_fortran.so
%{tpls_prefix}/lib/pkgconfig/superlu.pc
%endif

%changelog
* Tue Dec 19 2023 Christian Messe <cmesse@lbl.gov> -6.0.1-1
- Initial Package