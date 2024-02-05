%define scls_oflags -O3

Name:           scls-%{scls_flavor}-superlu
Version:        6.0.1
Release:        1%{?dist}
Summary:        Subroutines to directly solve sparse linear systems


License:        BSD
URL:            https://github.com/xiaoyeli/superlu
Source0:        https://github.com/xiaoyeli/superlu/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  scls-%{scls_flavor}-metis
Requires:       scls-%{scls_flavor}-metis


%description
SuperLU contains a set of subroutines to solve a sparse linear system
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP).
The columns of A may be preordered before factorization; the
preordering for sparsity is completely separate from the factorization.



%prep
%setup -q -n superlu-%{version}

%build
%{expand: %setup_scls_env}
%{scls_env} \
%{scls_cmake} . \
%if "%{scls_libs}" == "static"
    -DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} -DNDEBUG" \
    -DCMAKE_C_FLAGS_RELEASE="%{scls_cflags} -DNDEBUG %{scls_oflags}" \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} -DNDEBUG %{scls_oflags}" \
    -DCMAKE_Fortran_FLAGS_RELEASE="%{scls_fcflags} -DNDEBUG %{scls_oflags}" \
    -DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
%else
    -DCMAKE_C_FLAGS="%{scls_cflags} -fPIC -DNDEBUG %{scls_oflags}" \
    -DCMAKE_C_FLAGS_RELEASE="%{scls_cflags}  -fPIC -DNDEBUG %{scls_oflags}" \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} -fPIC -DNDEBUG %{scls_oflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{scls_cxxflags} -fPIC -DNDEBUG %{scls_oflags}" \
    -DCMAKE_Fortran_FLAGS="%{scls_fcflags} -fPIC -DNDEBUG %{scls_oflags}" \
    -DCMAKE_Fortran_FLAGS_RELEASE="%{scls_fcflags} -fPIC -DNDEBUG " \
%endif
	-DCMAKE_INSTALL_LIBDIR=lib \
%if "%{scls_math}" == "lapack"
%if "%{scls_compiler}" == "gnu"
	-DTPL_BLAS_LIBRARIES="%{scls_lapack};%{scls_blas};-lgfortran" \
%else
	-DTPL_BLAS_LIBRARIES="%{scls_lapack};%{scls_blas}" \
%endif
%else
	-DBLAS_LIBRARIES="%{scls_mkl_linker_flags}" \
%endif
%if "%{scls_libs}" == "static"
%else
	-DCMAKE_SHARED_LINKER_FLAGS="%{scls_ldflags} %{scls_mkl_linker_flags}" \
	-DCMAKE_EXE_LINKER_FLAGS="%{scls_ldflags} %{scls_mkl_linker_flags}" \
%endif
	-DTPL_ENABLE_METISLIB=ON \
	-DTPL_METIS_INCLUDE_DIRS=%{scls_prefix}/include \
%if "%{scls_libs}" == "static"
	-DTPL_METIS_LIBRARIES=%{scls_prefix}/lib/libmetis.a \
%else
	-DTPL_METIS_LIBRARIES=%{scls_prefix}/lib/libmetis.so \
%endif
	-Denable_fortran=ON \
	-Denable_internal_blaslib=OFF \
	.

%make_build

# manually create shared libs
%if "%{scls_libs}" == "shared"
%{scls_cc} %{scls_ldflags} -shared -o ./SRC/libsuperlu.so ./SRC/CMakeFiles/superlu.dir/*.o
%{scls_fc} %{scls_ldflags} -shared -o ./FORTRAN/libsuperlu_fortran.so ./FORTRAN/CMakeFiles/superlu_fortran.dir/*.o
%endif

%check
make test

%install
%make_install

%if "%{scls_libs}" == "shared"
install ./SRC/libsuperlu.so %{buildroot}/%{scls_prefix}/lib/
install ./FORTRAN/libsuperlu_fortran.so %{buildroot}/%{scls_prefix}/lib/
%endif

%files
%{scls_prefix}/include/slu_Cnames.h
%{scls_prefix}/include/slu_cdefs.h
%{scls_prefix}/include/slu_dcomplex.h
%{scls_prefix}/include/slu_ddefs.h
%{scls_prefix}/include/slu_scomplex.h
%{scls_prefix}/include/slu_sdefs.h
%{scls_prefix}/include/slu_util.h
%{scls_prefix}/include/slu_zdefs.h
%{scls_prefix}/include/superlu_config.fh
%{scls_prefix}/include/superlu_config.h
%{scls_prefix}/include/superlu_enum_consts.h
%{scls_prefix}/include/supermatrix.h
%{scls_prefix}/lib/cmake/superlu/superluConfig.cmake
%{scls_prefix}/lib/cmake/superlu/superluConfigVersion.cmake
%{scls_prefix}/lib/cmake/superlu/superluTargets-release.cmake
%{scls_prefix}/lib/cmake/superlu/superluTargets.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libsuperlu.a
%{scls_prefix}/lib/libsuperlu_fortran.a
%{scls_prefix}/lib/pkgconfig/superlu.pc
%else
%exclude %{scls_prefix}/lib/libsuperlu.a
%exclude %{scls_prefix}/lib/libsuperlu_fortran.a
%{scls_prefix}/lib/libsuperlu.so
%{scls_prefix}/lib/libsuperlu_fortran.so
%{scls_prefix}/lib/pkgconfig/superlu.pc
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> -6.0.1-1
- Initial Package
