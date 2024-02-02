Name:           tpls-%{tpls_flavor}-armadillo
Version:        12.6.7
Release:        1%{?dist}
Summary:        Fast C++ matrix library with syntax similar to MATLAB and Octave

License:        ASL 2.0
URL:            http://arma.sourceforge.net/
Source:         http://sourceforge.net/projects/arma/files/armadillo-%{version}.tar.xz

BuildRequires:  tpls-%{tpls_flavor}-arpack
BuildRequires:  tpls-%{tpls_flavor}-superlu
BuildRequires:  tpls-%{tpls_flavor}-metis

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
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
%endif


AutoReqProv:    %{tpls_auto_req_prov}

%description
Armadillo is a C++ linear algebra library (matrix maths)
aiming towards a good balance between speed and ease of use.
Integer, floating point and complex numbers are supported,
as well as a subset of trigonometric and statistics functions.
Various matrix decompositions are provided through optional
integration with LAPACK and ATLAS libraries.
A delayed evaluation approach is employed (during compile time)
to combine several operations into one and reduce (or eliminate)
the need for temporaries. This is accomplished through recursive
templates and template meta-programming.
This library is useful if C++ has been decided as the language
of choice (due to speed and/or integration capabilities), rather
than another language like Matlab or Octave.

%prep
%setup -q -n armadillo-%{version}

%build

# Compiler Settings
%{expand: %setup_tpls_env}
%{tpls_env} \
%if "%{tpls_gpu}" == "lapack"
LDFLAGS="%{tpls_ldflags} %{tpls_metis} %{tpls_lapack} %{tpls_blas}" \
%else
LDFLAGS="%{tpls_ldflags} %{tpls_metis} %{tpls_mkl_linker_flags}" \
%endif
%if "%{tpls_compiler}" == "gnu"
LDFLAGS+=" -lgfortran" \
%endif
%{tpls_cmake} . \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
%endif
	-DARPACK_LIBRARY=%{tpls_arpack} \
	-DSuperLU_LIBRARY=%{tpls_superlu} \
%if "%{tpls_gpu}" == "lapack"
	-DBLAS_LIBRARY="%{tpls_blas}" \
	-DLAPACK_LIBRARY="%{tpls_lapack}" \
%endif
	-DALLOW_FLEXIBLAS_LINUX=OFF
	
%make_build

%check
LD_LIBRARY_PATH=%{tpls_ld_library_path} make test


%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/include/armadillo
%{tpls_prefix}/include/armadillo_bits/
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libarmadillo.a
%else
%{tpls_prefix}/lib/libarmadillo.so
%{tpls_prefix}/lib/libarmadillo.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/armadillo.pc
%{tpls_prefix}/share/Armadillo/CMake/ArmadilloConfig.cmake
%{tpls_prefix}/share/Armadillo/CMake/ArmadilloConfigVersion.cmake
%{tpls_prefix}/share/Armadillo/CMake/ArmadilloLibraryDepends-release.cmake
%{tpls_prefix}/share/Armadillo/CMake/ArmadilloLibraryDepends.cmake


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 12.6.7
- Initial Package
