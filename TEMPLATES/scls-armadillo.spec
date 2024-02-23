%define scls_oflags -O3

Name:           scls-%{scls_flavor}-armadillo
Version:        12.8.0
Release:        2%{?dist}
Summary:        Fast C++ matrix library with syntax similar to MATLAB and Octave

License:        ASL 2.0
URL:            http://arma.sourceforge.net/
Source:         http://sourceforge.net/projects/arma/files/armadillo-%{version}.tar.xz

BuildRequires:  scls-%{scls_flavor}-arpack
BuildRequires:  scls-%{scls_flavor}-superlu
BuildRequires:  scls-%{scls_flavor}-metis

%if   "%{scls_mpi}" == "openmpi"
BuildRequires:  scls-%{scls_flavor}-openmpi
Requires:       scls-%{scls_flavor}-openmpi
%elif "%{scls_mpi}" == "mpich"
BuildRequires:  scls-%{scls_flavor}-mpich
Requires:       scls-%{scls_flavor}-mpich
%elif "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%endif


%if "%{scls_math}" == "lapack"
BuildRequires:  scls-%{scls_flavor}-blas
BuildRequires:  scls-%{scls_flavor}-lapack
Requires:       scls-%{scls_flavor}-blas
Requires:       scls-%{scls_flavor}-lapack
%endif




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
%{expand: %setup_scls_env}
%{scls_env} \
%if "%{scls_math}" == "lapack"
unset MKLROOT
LDFLAGS="%{scls_ldflags} %{scls_metis} %{scls_lapack} %{scls_blas}" \
%else
LDFLAGS="%{scls_ldflags} %{scls_metis} %{scls_mkl_linker_flags}" \
%endif
%if "%{scls_compiler}" == "gnu"
LDFLAGS+=" -lgfortran" \
%endif
%{scls_cmake} . \
    -DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
%endif
	-DARPACK_LIBRARY=%{scls_arpack} \
	-DSuperLU_LIBRARY=%{scls_superlu} \
%if "%{scls_math}" == "lapack"
	-DBLAS_LIBRARY="%{scls_blas}" \
	-DLAPACK_LIBRARY="%{scls_lapack}" \
%endif
	-DALLOW_FLEXIBLAS_LINUX=OFF
	
%make_build

%check
%if "%{scls_math}" == "cuda"
LD_LIBRARY_PATH=%{scls_ld_library_path} make test
%endif

%install
%make_install
%{scls_remove_la_files}

%files
%{scls_prefix}/include/armadillo
%{scls_prefix}/include/armadillo_bits/
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libarmadillo.a
%else
%{scls_prefix}/lib/libarmadillo.so
%{scls_prefix}/lib/libarmadillo.so.*
%endif
%{scls_prefix}/lib/pkgconfig/armadillo.pc
%{scls_prefix}/share/Armadillo/CMake/ArmadilloConfig.cmake
%{scls_prefix}/share/Armadillo/CMake/ArmadilloConfigVersion.cmake
%{scls_prefix}/share/Armadillo/CMake/ArmadilloLibraryDepends-release.cmake
%{scls_prefix}/share/Armadillo/CMake/ArmadilloLibraryDepends.cmake


%changelog
* Thu Feb 15 2024 Christian Messe <cmesse@lbl.gov> - 12.8.0-2
- Update to version 12.8.0
- Do not link against MKL when in LAPACK flavor

* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 12.6.7-1
- Initial Package
