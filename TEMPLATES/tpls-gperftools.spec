Name:           tpls-%{tpls_flavor}-gperftools
Version:        2.15
Release:        1%{?dist}

License:	BSD
Summary:	Very fast malloc and performance analysis tools
URL:		https://github.com/gperftools/gperftools
Source:     https://github.com/gperftools/gperftools/releases/download/gperftools-%{version}/gperftools-%{version}.tar.gz


BuildRequires:	libunwind-devel
BuildRequires:	perl-generators
BuildRequires:	autoconf, automake, libtool
BuildRequires:	make

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly heap-checker,
a heap profiler, and a cpu-profiler.

This is a metapackage which pulls in all of the gperftools (and pprof)
binaries, libraries, and development headers, so that you can use them.

%prep
%setup -q -n gperftools-%{version}

%build
%{tpls_env} ./configure \
    --prefix=%{tpls_prefix} \
%if "%{tpls_libs}" == "static"
	--enable-static \
	--disable-shared \
%else
	--disable-static \
	--enable-shared \
%endif
	--enable-libunwind

%make_build

%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/bin/pprof
%{tpls_prefix}/bin/pprof-symbolize
%{tpls_prefix}/include/google
%{tpls_prefix}/include/gperftools
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libprofiler.a
%{tpls_prefix}/lib/libtcmalloc.a
%{tpls_prefix}/lib/libtcmalloc_and_profiler.a
%{tpls_prefix}/lib/libtcmalloc_debug.a
%{tpls_prefix}/lib/libtcmalloc_minimal.a
%{tpls_prefix}/lib/libtcmalloc_minimal_debug.a
%else
%{tpls_prefix}/lib/libprofiler.so
%{tpls_prefix}/lib/libprofiler.so.*
%{tpls_prefix}/lib/libtcmalloc.so
%{tpls_prefix}/lib/libtcmalloc.so.*
%{tpls_prefix}/lib/libtcmalloc_and_profiler.so
%{tpls_prefix}/lib/libtcmalloc_and_profiler.so.*
%{tpls_prefix}/lib/libtcmalloc_debug.so
%{tpls_prefix}/lib/libtcmalloc_debug.so.*
%{tpls_prefix}/lib/libtcmalloc_minimal.so
%{tpls_prefix}/lib/libtcmalloc_minimal.so.*
%{tpls_prefix}/lib/libtcmalloc_minimal_debug.so
%{tpls_prefix}/lib/libtcmalloc_minimal_debug.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/libprofiler.pc
%{tpls_prefix}/lib/pkgconfig/libtcmalloc.pc
%{tpls_prefix}/lib/pkgconfig/libtcmalloc_debug.pc
%{tpls_prefix}/lib/pkgconfig/libtcmalloc_minimal.pc
%{tpls_prefix}/lib/pkgconfig/libtcmalloc_minimal_debug.pc
%{tpls_prefix}/share/doc/gperftools
%{tpls_prefix}/share/man/man1/pprof.1


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.15-1
- Initial Package
