Name:           tpls-%{tpls_flavor}-libevent
Version:        2.1.12
Release:        1%{?dist}
Summary:        Abstract asynchronous event notification library

# arc4random.c, which is used in build, is ISC. The rest is BSD.
License:        BSD and ISC
URL:            http://libevent.org/
Source0:        https://github.com/libevent/libevent/releases/download/release-%{version}-stable/libevent-%{version}-stable.tar.gz


BuildRequires: openssl-devel
BuildRequires: python3-devel

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
%if "%{tpls_compiler}" == "intel"
if [ "$SETVARS_COMPLETED" != "1" ]; then
	source /opt/intel/oneapi/setvars.sh intel64
fi
%endif

./configure \
    --prefix=%{tpls_prefix} \
    --disable-dependency-tracking \
%if "%{tpls_libs}" == "static"
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
%{tpls_remove_la_files}

# Fix multilib install of devel (bug #477685)
mv $RPM_BUILD_ROOT%{tpls_prefix}/include/event2/event-config.h \
   $RPM_BUILD_ROOT%{tpls_prefix}/include/event2/event-config-%{__isa_bits}.h
cat > $RPM_BUILD_ROOT%{tpls_prefix}/include/event2/event-config.h << EOF
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
%{tpls_prefix}/bin/event_rpcgen.py
%{tpls_prefix}/include/evdns.h
%{tpls_prefix}/include/event.h
%{tpls_prefix}/include/event2/buffer.h
%{tpls_prefix}/include/event2/buffer_compat.h
%{tpls_prefix}/include/event2/bufferevent.h
%{tpls_prefix}/include/event2/bufferevent_compat.h
%{tpls_prefix}/include/event2/bufferevent_ssl.h
%{tpls_prefix}/include/event2/bufferevent_struct.h
%{tpls_prefix}/include/event2/dns.h
%{tpls_prefix}/include/event2/dns_compat.h
%{tpls_prefix}/include/event2/dns_struct.h
%{tpls_prefix}/include/event2/event-config-64.h
%{tpls_prefix}/include/event2/event-config.h
%{tpls_prefix}/include/event2/event.h
%{tpls_prefix}/include/event2/event_compat.h
%{tpls_prefix}/include/event2/event_struct.h
%{tpls_prefix}/include/event2/http.h
%{tpls_prefix}/include/event2/http_compat.h
%{tpls_prefix}/include/event2/http_struct.h
%{tpls_prefix}/include/event2/keyvalq_struct.h
%{tpls_prefix}/include/event2/listener.h
%{tpls_prefix}/include/event2/rpc.h
%{tpls_prefix}/include/event2/rpc_compat.h
%{tpls_prefix}/include/event2/rpc_struct.h
%{tpls_prefix}/include/event2/tag.h
%{tpls_prefix}/include/event2/tag_compat.h
%{tpls_prefix}/include/event2/thread.h
%{tpls_prefix}/include/event2/util.h
%{tpls_prefix}/include/event2/visibility.h
%{tpls_prefix}/include/evhttp.h
%{tpls_prefix}/include/evrpc.h
%{tpls_prefix}/include/evutil.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libevent.a
%{tpls_prefix}/lib/libevent_core.a
%{tpls_prefix}/lib/libevent_extra.a
%{tpls_prefix}/lib/libevent_openssl.a
%{tpls_prefix}/lib/libevent_pthreads.a
%else
%{tpls_prefix}/lib/libevent-2.1.so.*
%{tpls_prefix}/lib/libevent.so
%{tpls_prefix}/lib/libevent_core-2.1.so.*
%{tpls_prefix}/lib/libevent_core.so
%{tpls_prefix}/lib/libevent_extra-2.1.so.*
%{tpls_prefix}/lib/libevent_extra.so
%{tpls_prefix}/lib/libevent_openssl-2.1.so.*
%{tpls_prefix}/lib/libevent_openssl.so
%{tpls_prefix}/lib/libevent_pthreads-2.1.so.*
%{tpls_prefix}/lib/libevent_pthreads.so
%endif
%{tpls_prefix}/lib/pkgconfig/libevent.pc
%{tpls_prefix}/lib/pkgconfig/libevent_core.pc
%{tpls_prefix}/lib/pkgconfig/libevent_extra.pc
%{tpls_prefix}/lib/pkgconfig/libevent_openssl.pc
%{tpls_prefix}/lib/pkgconfig/libevent_pthreads.pc


%changelog
* Wed Dec 13 2023 Christian Messe <cmesse@lbl.gov> - 2.1.12-1
- Initial package.
