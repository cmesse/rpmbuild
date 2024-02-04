%define scls_oflags -O3

Name:           scls-%{scls_flavor}-gmp
Version:        6.3.0
Release:        1%{?dist}
Summary:        GNU arbitrary precision library

License:        LGPLv3+ or GPLv2+
URL:            https://gmplib.org/
Source0:        https://gmplib.org/download/gmp/gmp-%{version}.tar.xz

BuildRequires:  autoconf automake libtool
BuildRequires:  %scls_rpm_cc  >= %{scls_comp_minver}
BuildRequires:  %scls_rpm_cxx >= %{scls_comp_minver}
BuildRequires:  git
#autoreconf on arm needs:
BuildRequires:  perl-Carp
BuildRequires:  make

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

%prep
%setup -q -n gmp-%{version}


%build

%{expand: %setup_scls_env}

sed -i 's|-O2|%{scls_cflags} %{scls_oflags}|g'  ./configure
sed -i 's|skylake|%{scls_host}|g'  ./configure
sed -i 's|broadwell|%{scls_host}|g' ./configure

%{scls_env} \
./configure \
    --prefix=%{scls_prefix} \
	--enable-cxx \
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
%{scls_prefix}/include/gmp.h
%{scls_prefix}/include/gmpxx.h
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libgmp.a
%{scls_prefix}/lib/libgmpxx.a
%else
%{scls_prefix}/lib/libgmp.so
%{scls_prefix}/lib/libgmp.so.10
%{scls_prefix}/lib/libgmp.so.10.5.0
%{scls_prefix}/lib/libgmpxx.so
%{scls_prefix}/lib/libgmpxx.so.4
%{scls_prefix}/lib/libgmpxx.so.4.7.0
%endif
%{scls_prefix}/lib/pkgconfig/gmp.pc
%{scls_prefix}/lib/pkgconfig/gmpxx.pc
%exclude %{scls_prefix}/share

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 6.3.0-1
- Initial Package
