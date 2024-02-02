#######################################################################
# FLAVOR SPECIFIC DEFINES                                             #
#######################################################################

%define tpls_flavor skylake-gnu-mpich-rocm 

%define tpls_host skylake 
%define tpls_compiler gnu 
%define tpls_mpi mpich 
%define tpls_gpu rocm 
%define tpls_libs shared 
%define tpls_int 32 
%define tpls_comp_minver 11.4.1 

%define tpls_rpm_cc gcc 
%define tpls_rpm_cxx gcc-c++ 
%define tpls_rpm_fc gfortran 
%define tpls_auto_req_prov yes

# important paths
%define tpls_prefix /opt/tpls/skylake-gnu-mpich-rocm 
%define tpls_includes /opt/tpls/skylake-gnu-mpich-rocm/includes 
%define tpls_libdir /opt/tpls/skylake-gnu-mpich-rocm/lib 
%define tpls_comproot /usr 
%define tpls_mklroot  /opt/intel/oneapi/mkl/latest 
%define tpls_cuda  /opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda 
%define tpls_rocm  /opt/rocm 
%define tpls_ld_library_path  /opt/tpls/skylake-gnu-mpich-rocm/lib:/opt/intel/oneapi/mkl/latest/lib:/opt/rocm/lib 

# compiler executables
%define tpls_cc gcc 
%define tpls_cxx g++ 
%define tpls_fc gfortran 
%define tpls_ar ar 
%define tpls_ld ld 
%define tpls_cpp ld -E 
%define tpls_cxxcpp ld -E 

# MPI wrappers
%define tpls_mpicc   /opt/tpls/skylake-gnu-mpich-rocm/bin/mpicc
%define tpls_mpicxx  /opt/tpls/skylake-gnu-mpich-rocm/bin/mpicxx 
%define tpls_mpifort /opt/tpls/skylake-gnu-mpich-rocm/bin/mpifort 
%define tpls_mpiroot /opt/tpls/skylake-gnu-mpich-rocm 
%define tpls_mpilib /opt/tpls/skylake-gnu-mpich-rocm/lib/libmpi.so 

# Compiler Flags
%define tpls_cflags    -O2 -m64 -fno-fast-math -fPIC -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-mpich-rocm/include -I/opt/intel/oneapi/mkl/latest/include -I/opt/rocm/include
%define tpls_cxxflags  -O2 -m64 -fno-fast-math -fPIC -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-mpich-rocm/include -I/opt/intel/oneapi/mkl/latest/include -I/opt/rocm/include
%define tpls_fcflags   -O2 -m64 -fno-fast-math -fPIC -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-mpich-rocm/include -I/opt/intel/oneapi/mkl/latest/include -I/opt/rocm/include
%define tpls_ldflags    -L/opt/tpls/skylake-gnu-mpich-rocm/lib -L/opt/intel/oneapi/mkl/latest/lib -L/opt/rocm/lib  -Wl,-rpath,/opt/tpls/skylake-gnu-mpich-rocm/lib -Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib -Wl,-rpath,/opt/rocm/lib
%define tpls_arflags   -cru
%define tpls_ompflag    -fopenmp

# the netlib reference implementations
%define tpls_blas   /opt/tpls/skylake-gnu-mpich-rocm/lib/libblas.so
%define tpls_lapack  /opt/tpls/skylake-gnu-mpich-rocm/lib/liblapack.so
%define tpls_scalapack /opt/tpls/skylake-gnu-mpich-rocm/lib/libscalapack.so

# the MKL setup
%define tpls_mkl_linker_flags   -lmkl_intel_lp64 -lmkl_gnu_thread -lmkl_core  -lgomp  -lpthread -lm -ldl
%define tpls_mkl_mpi_linker_flags  -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_gnu_thread -lmkl_core -lmkl_blacs_intelmpi_lp64  -lgomp -lpthread -lm -ldl
%define tpls_arpack /opt/tpls/skylake-gnu-mpich-rocm/lib/libarpack.so
%define tpls_parpack /opt/tpls/skylake-gnu-mpich-rocm/lib/libparpack.so
%define tpls_superlu /opt/tpls/skylake-gnu-mpich-rocm/lib/libsuperlu.so
%define tpls_metis /opt/tpls/skylake-gnu-mpich-rocm/lib/libmetis.so

########################################################################
# ENVIRONMENT SETUP                                                    #
########################################################################


%global setup_tpls_env \
# setup the Intel OneAPI \
if [ "%{tpls_gpu}" != "lapack" ]; then \
  if [ "$SETVARS_COMPLETED" != "1" ]; then \
    source /opt/intel/oneapi/setvars.sh intel64; \
  fi; \
fi; \
export LD=%{tpls_ld} \
export AR=%{tpls_ar} \
export CC=%{tpls_cc} \
export CPP="%{tpls_cc} -E" \
export CXXCPP="%{tpls_cxx} -E" \
export CXX=%{tpls_cxx} \
export FC=%{tpls_fc} \
export F77=%{tpls_fc} \
export FF=%{tpls_fc} \
export CFLAGS="%{tpls_cflags}" \
export CXXFLAGS="%{tpls_cxxflags}" \
export FFLAGS="%{tpls_fcflags}" \
export FCLAGS="%{tpls_fcflags}" \
# check if the compilers are in the path \
if [[ ":$PATH:" != *:%{tpls_comproot}/bin* ]]; then \
  export PATH="%{tpls_comproot}/bin:$PATH"; \
fi; \
# check if CUDA is used and in the path \
if [ "%{tpls_gpu}" == "cuda" ]; then \
  if [[ ":$PATH:" != *:%{tpls_cuda}/bin* ]]; then \
    export PATH="%{tpls_cuda}/bin:$PATH"; \
  fi; \
fi; \
# check if ROCM is used and in the path \
if [ "%{tpls_gpu}" == "rocm" ]; then \
  if [[ ":$PATH:" != *:%{tpls_rocm}/bin* ]]; then \
    export PATH="%{tpls_rocm}/bin:$PATH"; \
  fi; \
fi; \
# add the TPLS binary directory \
if [[ ":$PATH:" != *:%{tpls_prefix}/bin* ]]; then \
  export PATH="%{tpls_prefix}/bin:$PATH"; \
fi;
########################################################################
# AUTOMATIC MACROS                                                     #
########################################################################

%define tpls_maxprocs 64

%define tpls_env \
    PKG_CONFIG_PATH=%{tpls_prefix}lib/pkgconfig \
	LD=%{tpls_ld}   \
	AR=%{tpls_ar}   \
	CC=%{tpls_cc}   \
	CXX=%{tpls_cxx} \
	FC=%{tpls_fc}   \
	FF=%{tpls_fc}   \
	F77=%{tpls_fc} \
    CFLAGS="%{tpls_cflags}" \
	CXXFLAGS="%{tpls_cxxflags}" \
	FCFLAGS="%{tpls_fcflags}"
		
# fix the qversion bug in configure
%define tpls_remove_qversion    sed -i 's| -qversion||'g ./configure ;

# cmake
%define tpls_cmake %{tpls_prefix}/bin/cmake -DCMAKE_INSTALL_PREFIX=%{tpls_prefix} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_LIBDIR=lib


# delete-la-tool
%define tpls_remove_la_files    find %{buildroot} -name '*.la' -delete
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

Requires:      %{tpls_rpm_cc}  >= %{tpls_comp_minver}
Requires:      %{tpls_rpm_cxx} >= %{tpls_comp_minver}
Requires:      %{tpls_rpm_fc}  >= %{tpls_comp_minver}
AutoReqProv:   %{tpls_auto_req_prov}

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

%{setup_tpls_env}

%{tpls_env} ./configure \
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
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.1.12-1
- Initial Package
