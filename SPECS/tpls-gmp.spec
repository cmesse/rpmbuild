Name:           tpls-%{tpls_flavor}-gmp
Version:        6.3.0
Release:        1%{?dist}
Summary:        GNU arbitrary precision library

License:        LGPLv3+ or GPLv2+
URL:            https://gmplib.org/
Source0:        https://gmplib.org/download/gmp/gmp-%{version}.tar.xz

BuildRequires:  autoconf automake libtool
BuildRequires:  %tpls_rpm_cc  >= %{tpls_comp_minver}
BuildRequires:  %tpls_rpm_cxx >= %{tpls_comp_minver}
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
sed -i 's/-O2/%{tpls_coptflags}/g'  ./configure
sed -i 's/skylake/%{tpls_host}/g'  ./configure
sed -i 's/broadwell/%{tpls_host}/g' ./configure

CFLAGS="%{tpls_coptflags}" \
CXXFLAGS="%{tpls_cxxoptflags}" \
%tpls_configure_noprefixdir \
	--enable-cxx \
%if "%{tpls_libs}" == "static"
	--enable-static \
	--disable-shared
%else
	--disable-static \
	--enable-shared
%endif

%make_build

%if %{tpls_check} == 1
%make_build check
%endif

%install
%make_install
%{tpls_remove_la_files}
%{tpls_remove_info_files}
%{tpls_remove_doc_files}

%files
%{tpls_prefix}/include/gmp.h
%{tpls_prefix}/include/gmpxx.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libgmp.a
%{tpls_prefix}/lib/libgmpxx.a
%else
%{tpls_prefix}/lib/libgmp.so
%{tpls_prefix}/lib/libgmp.so.10
%{tpls_prefix}/lib/libgmp.so.10.5.0
%{tpls_prefix}/lib/libgmpxx.so
%{tpls_prefix}/lib/libgmpxx.so.4
%{tpls_prefix}/lib/libgmpxx.so.4.7.0
%endif
%{tpls_prefix}/lib/pkgconfig/gmp.pc
%{tpls_prefix}/lib/pkgconfig/gmpxx.pc
%exclude %{tpls_prefix}/share

%changelog
* Mon Dec 11 2023 Christian Messe <cmesse@lbl.gov> - 6.3.0-1
- Initial Package
