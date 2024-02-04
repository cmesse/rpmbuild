%define scls_oflags -O3

Name:           scls-%{scls_flavor}-blaze
Version:        3.8.2
Release:        1%{?dist}
Summary:        A high-performance C++ math library for dense and sparse arithmetic
License:        BSD
URL:            https://bitbucket.org/blaze-lib/blaze
Source0:        https://bitbucket.org/blaze-lib/blaze/downloads/blaze-%{version}.tar.gz

%if "%{scls_math}" == "lapack"
BuildRequires:  scls-%{scls_flavor}-blas
BuildRequires:  scls-%{scls_flavor}-lapack
Requires:       scls-%{scls_flavor}-blas
Requires:       scls-%{scls_flavor}-lapack
%endif




BuildRequires:  scls-%{scls_flavor}-cmake

%description
Blaze is an open-source, high-performance C++ math library for dense and \
sparse arithmetic. With its state-of-the-art Smart Expression Template \
implementation Blaze combines the elegance and ease of use of a \
domain-specific language with HPC-grade performance, making it one of \
the most intuitive and fastest C++ math libraries available. \

%prep
%setup -q -n blaze-%{version}

%build

# Compiler Settings
%{expand: %setup_scls_env}
%{scls_env} \
%{scls_cmake} \
    -DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_math}" == "lapack"
	-DBLAS_LIBRARIES=%{scls_blas} \
	-DLAPACK_LIBRARIES=%{scls_lapack} \
%else
	-DBLAS_LIBRARIES="%{scls_mkl_linker_flags}" \
	-DLAPACK_LIBRARIES="%{scls_mkl_linker_flags}" \
%endif
    .


%install
%make_install

%check
cd blazetest
./run

%files
%{scls_prefix}/include/blaze/
%{scls_prefix}/share/blaze/

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.8.2
- Initial Package
