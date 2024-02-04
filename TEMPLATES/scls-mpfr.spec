%define scls_oflags -O3

Summary: C library for multiple-precision floating-point computations
Name: scls-%{scls_flavor}-mpfr
Version: 4.2.1
Release: 1%{?dist}

License: LGPL-3.0-or-later
URL: https://www.mpfr.org/
Source0: https://www.mpfr.org/%{name}-%{version}/mpfr-%{version}.tar.xz


BuildRequires: %scls_rpm_cc  >= %{scls_comp_minver}
BuildRequires: scls-%{scls_flavor}-gmp
BuildRequires: make
BuildRequires: texinfo

Requires: scls-%{scls_flavor}-gmp

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%prep
%setup -q -n mpfr-%{version}

%build
%{expand: %setup_scls_env}
%{scls_env} \
CFLAGS+=" %{scls_oflags}"  \
CXXFLAGS+=" %{scls_oflags}"  \
./configure \
    --prefix=%{scls_prefix} \
    --with-gmp-include=%{scls_prefix}/include \
    --with-gmp-lib=%{scls_prefix}/lib \
	--enable-thread-safe \
%if "%{scls_libs}" == "static"
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
%{scls_remove_la_files}

%files
%{scls_prefix}/include/mpf2mpfr.h
%{scls_prefix}/include/mpfr.h
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libmpfr.a
%else
%{scls_prefix}/lib/libmpfr.so
%{scls_prefix}/lib/libmpfr.so.*
%endif
%{scls_prefix}/lib/pkgconfig/mpfr.pc
%exclude %{scls_prefix}/share


%changelog
* Mon Dec 11 2023 Christian Messe <cmesse@lbl.gov> - 4.2.1-1
- Initial Package
