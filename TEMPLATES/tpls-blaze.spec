Name:           tpls-%{tpls_flavor}-blaze
Version:        3.8.2
Release:        1%{?dist}
Summary:        An high-performance C++ math library for dense and sparse arithmetic
License:        BSD
URL:            https://bitbucket.org/blaze-lib/blaze
Source0:        https://bitbucket.org/blaze-lib/blaze/downloads/blaze-%{version}.tar.gz

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
%endif


AutoReqProv:    %{tpls_auto_req_prov}

BuildRequires:  tpls-%{tpls_flavor}-cmake

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
%{expand: %setup_tpls_env}
%{tpls_env} \
%{tpls_cmake} . \
%if "%{tpls_gpu}" == "lapack"
	-DBLAS_LIBRARIES=%{tpls_blas} \
	-DLAPACK_LIBRARIES=%{tpls_lapack} \
%else
	-DBLAS_LIBRARIES="%{tpls_mkl_linker_flags}" \
	-DLAPACK_LIBRARIES="%{tpls_mkl_linker_flags}" \
%endif


%install
%make_install

%check
cd blazetest
./run

%files
%{tpls_prefix}/include/blaze/
%{tpls_prefix}/share/blaze/

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.8.2
- Initial Package
