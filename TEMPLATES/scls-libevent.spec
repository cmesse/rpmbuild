%define scls_oflags -O2
Name:           scls-%{scls_flavor}-libevent
Version:        2.1.12
Release:        1%{?dist}
Summary:        Abstract asynchronous event notification library

# arc4random.c, which is used in build, is ISC. The rest is BSD.
License:        BSD and ISC
URL:            https://libevent.org/
Source0:        https://github.com/libevent/libevent/releases/download/release-%{version}-stable/libevent-%{version}-stable.tar.gz


BuildRequires: openssl-devel
BuildRequires: python3-devel

Requires:      %{scls_rpm_cc}  >= %{scls_comp_minver}
Requires:      %{scls_rpm_cxx} >= %{scls_comp_minver}
Requires:      %{scls_rpm_fc}  >= %{scls_comp_minver}

# Fix Python shebang
Patch00 :        libevent_fix_python_shebang.patch
# Disable network tests
Patch01: libevent-nonettests.patch
# Upstream patch:
Patch02: libevent-build-do-not-try-install-doxygen-man-pages-if-they-w.patch
# Upstream patch:
Patch03: libevent-build-add-doxygen-to-all.patch
# Temporary downstream change: revert a problematic upstream change
# until Transmission is fixed. Please drop the patch when the Transmission
# issue is fixed.
# https://github.com/transmission/transmission/issues/1437
Patch04: libevent-Revert-Fix-checking-return-value-of-the-evdns_base_r.patch

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%prep
%setup -q -n libevent-%{version}-stable
%patch00 -p1
#%patch01 -p1 -b .nonettests
#%patch02 -p1 -b .fix-install
#%patch03 -p1 -b .fix-install-2
#%patch04 -p1 -b .revert-problematic-change

%build

%{setup_scls_env}

%{scls_env} \
CFLAGS+=" %{scls_oflags}" \
CXXFLAGS+=" %{scls_oflags}" \
FCFLAGS+=" %{scls_oflags}" \
./configure \
    --prefix=%{scls_prefix} \
    --disable-dependency-tracking \
%if "%{scls_libs}" == "static"
    --enable-static \
    --disable-shared
%else
    --disable-static \
    --enable-shared
%endif
%make_build all

%check
# Tests fail due to nameserver not running locally
# [msg] Nameserver 127.0.0.1:38762 has failed: request timed out.
# On some architects this error is ignored on others it is not.
#make check

%install

%make_install
%{scls_remove_la_files}

# Fix multilib install of devel (bug #477685)
mv $RPM_BUILD_ROOT%{scls_prefix}/include/event2/event-config.h \
   $RPM_BUILD_ROOT%{scls_prefix}/include/event2/event-config-%{__isa_bits}.h
cat > $RPM_BUILD_ROOT%{scls_prefix}/include/event2/event-config.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include <event2/event-config-32.h>
#elif __WORDSIZE == 64
#include <event2/event-config-64.h>
#else
#error "Unknown word size"
#endif
EOF

%files
%{scls_prefix}/bin/event_rpcgen.py
%{scls_prefix}/include/evdns.h
%{scls_prefix}/include/event.h
%{scls_prefix}/include/event2/buffer.h
%{scls_prefix}/include/event2/buffer_compat.h
%{scls_prefix}/include/event2/bufferevent.h
%{scls_prefix}/include/event2/bufferevent_compat.h
%{scls_prefix}/include/event2/bufferevent_ssl.h
%{scls_prefix}/include/event2/bufferevent_struct.h
%{scls_prefix}/include/event2/dns.h
%{scls_prefix}/include/event2/dns_compat.h
%{scls_prefix}/include/event2/dns_struct.h
%{scls_prefix}/include/event2/event-config-64.h
%{scls_prefix}/include/event2/event-config.h
%{scls_prefix}/include/event2/event.h
%{scls_prefix}/include/event2/event_compat.h
%{scls_prefix}/include/event2/event_struct.h
%{scls_prefix}/include/event2/http.h
%{scls_prefix}/include/event2/http_compat.h
%{scls_prefix}/include/event2/http_struct.h
%{scls_prefix}/include/event2/keyvalq_struct.h
%{scls_prefix}/include/event2/listener.h
%{scls_prefix}/include/event2/rpc.h
%{scls_prefix}/include/event2/rpc_compat.h
%{scls_prefix}/include/event2/rpc_struct.h
%{scls_prefix}/include/event2/tag.h
%{scls_prefix}/include/event2/tag_compat.h
%{scls_prefix}/include/event2/thread.h
%{scls_prefix}/include/event2/util.h
%{scls_prefix}/include/event2/visibility.h
%{scls_prefix}/include/evhttp.h
%{scls_prefix}/include/evrpc.h
%{scls_prefix}/include/evutil.h
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libevent.a
%{scls_prefix}/lib/libevent_core.a
%{scls_prefix}/lib/libevent_extra.a
%{scls_prefix}/lib/libevent_openssl.a
%{scls_prefix}/lib/libevent_pthreads.a
%else
%{scls_prefix}/lib/libevent-2.1.so.*
%{scls_prefix}/lib/libevent.so
%{scls_prefix}/lib/libevent_core-2.1.so.*
%{scls_prefix}/lib/libevent_core.so
%{scls_prefix}/lib/libevent_extra-2.1.so.*
%{scls_prefix}/lib/libevent_extra.so
%{scls_prefix}/lib/libevent_openssl-2.1.so.*
%{scls_prefix}/lib/libevent_openssl.so
%{scls_prefix}/lib/libevent_pthreads-2.1.so.*
%{scls_prefix}/lib/libevent_pthreads.so
%endif
%{scls_prefix}/lib/pkgconfig/libevent.pc
%{scls_prefix}/lib/pkgconfig/libevent_core.pc
%{scls_prefix}/lib/pkgconfig/libevent_extra.pc
%{scls_prefix}/lib/pkgconfig/libevent_openssl.pc
%{scls_prefix}/lib/pkgconfig/libevent_pthreads.pc


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.1.12-1
- Initial Package
