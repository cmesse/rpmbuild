Name:           scls-%{scls_flavor}-gperftools
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
%{scls_env} \
./configure \
    --prefix=%{scls_prefix} \
%if "%{scls_libs}" == "static"
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
%{scls_remove_la_files}

%files
%{scls_prefix}/bin/pprof
%{scls_prefix}/bin/pprof-symbolize
%{scls_prefix}/include/google
%{scls_prefix}/include/gperftools
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libprofiler.a
%{scls_prefix}/lib/libtcmalloc.a
%{scls_prefix}/lib/libtcmalloc_and_profiler.a
%{scls_prefix}/lib/libtcmalloc_debug.a
%{scls_prefix}/lib/libtcmalloc_minimal.a
%{scls_prefix}/lib/libtcmalloc_minimal_debug.a
%else
%{scls_prefix}/lib/libprofiler.so
%{scls_prefix}/lib/libprofiler.so.*
%{scls_prefix}/lib/libtcmalloc.so
%{scls_prefix}/lib/libtcmalloc.so.*
%{scls_prefix}/lib/libtcmalloc_and_profiler.so
%{scls_prefix}/lib/libtcmalloc_and_profiler.so.*
%{scls_prefix}/lib/libtcmalloc_debug.so
%{scls_prefix}/lib/libtcmalloc_debug.so.*
%{scls_prefix}/lib/libtcmalloc_minimal.so
%{scls_prefix}/lib/libtcmalloc_minimal.so.*
%{scls_prefix}/lib/libtcmalloc_minimal_debug.so
%{scls_prefix}/lib/libtcmalloc_minimal_debug.so.*
%endif
%{scls_prefix}/lib/pkgconfig/libprofiler.pc
%{scls_prefix}/lib/pkgconfig/libtcmalloc.pc
%{scls_prefix}/lib/pkgconfig/libtcmalloc_debug.pc
%{scls_prefix}/lib/pkgconfig/libtcmalloc_minimal.pc
%{scls_prefix}/lib/pkgconfig/libtcmalloc_minimal_debug.pc
%{scls_prefix}/share/doc/gperftools
%{scls_prefix}/share/man/man1/pprof.1


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.15-1
- Initial Package
