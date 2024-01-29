Summary: C library for multiple-precision floating-point computations
Name: tpls-%{tpls_flavor}-mpfr
Version: 4.2.1
Release: 1%{?dist}

License: LGPL-3.0-or-later
URL: https://www.mpfr.org/
Source0: https://www.mpfr.org/%{name}-%{version}/mpfr-%{version}.tar.xz


BuildRequires: %tpls_rpm_cc  >= %{tpls_comp_minver}
BuildRequires: tpls-%{tpls_flavor}-gmp
BuildRequires: make
BuildRequires: texinfo

Requires: tpls-%{tpls_flavor}-gmp

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%prep
%setup -q -n mpfr-%{version}

%build
%{expand: %setup_tpls_env}

%{tpls_env} ./configure \
    --prefix=%{tpls_prefix} \
    --with-gmp-include=%{tpls_prefix}/include \
    --with-gmp-lib=%{tpls_prefix}/lib \
	--enable-thread-safe \
%if "%{tpls_libs}" == "static"
	--enable-static \
	--disable-shared
%else
	--disable-static \
	--enable-shared
%endif

%make_build

%check
%make_build check

%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/include/mpf2mpfr.h
%{tpls_prefix}/include/mpfr.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libmpfr.a
%else
%{tpls_prefix}/lib/libmpfr.so
%{tpls_prefix}/lib/libmpfr.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/mpfr.pc
%exclude %{tpls_prefix}/share


%changelog
* Mon Dec 11 2023 Christian Messe <cmesse@lbl.gov> - 4.2.1-1
- Initial Package
