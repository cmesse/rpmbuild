Name:           tpls-%{tpls_flavor}-hwloc
Version:        2.10.0
Release:        1%{?dist}
Summary:        Portable Hardware Locality

License:        BSD
URL:            https://www-lb.open-mpi.org/software/hwloc/v2.10/
Source0:        https://download.open-mpi.org/release/hwloc/v2.10/hwloc-2.10.0.tar.bz2

Requires:      %{tpls_rpm_cc}  >= %{tpls_comp_minver}
Requires:      %{tpls_rpm_cxx} >= %{tpls_comp_minver}
Requires:      %{tpls_rpm_fc}  >= %{tpls_comp_minver}
Requires:      tpls-%{tpls_flavor}-libevent

BuildRequires: tpls-%{tpls_flavor}-libevent
Requires: tpls-%{tpls_flavor}-libevent

AutoReqProv:   %{tpls_auto_req_prov}

%if "%{tpls_gpu}" == "cuda"
BuildRequires: nvhpc-cuda-multi 
Requires:      nvhpc-cuda-multi 
%elif "%{tpls_gpu}" == "rocm"
BuildRequires: rocm-hip-sdk
BuildRequires: rocsolver-devel
BuildRequires: rocblas-devel
BuildRequires: hip-runtime-amd
Requires: rocm-hip-sdk
Requires: rocsolver-devel
Requires: rocblas-devel
Requires: hip-runtime-amd
%endif

%description
The Portable Hardware Locality (hwloc) software package provides a portable abstraction (across OS, versions, architectures, ...) of the hierarchical topology of modern architectures, including NUMA memory nodes (DRAM, HBM, non-volatile memory, CXL, etc.), sockets, shared caches, cores and simultaneous multithreading. It also gathers various system attributes such as cache and memory information as well as the locality of I/O devices such as network interfaces, InfiniBand HCAs or GPUs.

hwloc primarily aims at helping applications with gathering information about increasingly complex parallel computing platforms so as to exploit them accordingly and efficiently. For instance, two tasks that tightly cooperate should probably be placed onto cores sharing a cache. However, two independent memory-intensive tasks should better be spread out onto different sockets so as to maximize their memory throughput. As described in this paper, OpenMP threads have to be placed according to their affinities and to the hardware characteristics. MPI implementations apply similar techniques while also adapting their communication strategies to the network locality as described in this paper or this one.

hwloc may also help many applications just by providing a portable CPU and memory binding API and a reliable way to find out how many cores and/or hardware threads are available.

%package doc
Summary: Documentation files for hwloc
%description doc
Documentation files for hwloc

%prep
%setup -q -n hwloc-%{version}


%build
%{setup_tpls_env}

%{tpls_env}

%if "%{tpls_libs}" == "static"
CFLAGS+="  -DHAVE_UNIX_BYTESWAP" \
CXXFLAGS+=" -DHAVE_UNIX_BYTESWAP" \
FCFLAGS+="  -DHAVE_UNIX_BYTESWAP" \
%else
CFLAGS+=" -fPIC -DHAVE_UNIX_BYTESWAP" \
CXXFLAGS+=" -fPIC -DHAVE_UNIX_BYTESWAP" \
FCFLAGS+=" -fPIC -DHAVE_UNIX_BYTESWAP" \
%endif
./configure \
   --prefix=%{tpls_prefix} \
%if "%{tpls_libs}" == "static"
   --enable-static \
   --disable-shared \
%else
   --disable-static \
   --enable-shared \
%endif
%if "%{tpls_gpu}" == "cuda"
   --with-cuda=%{tpls_cuda} \
   --enable-nvml \
%else
    --disable-cuda \
    --disable-nvml \
%endif
%if "%{tpls_gpu}" == "rocm"
	--with-rocm=%{tpls_rocm} \
%else
	--disable-rocm \
%endif
	--enable-pci \
	--disable-opencl \
	--disable-gl \
	--disable-levelzero \
	--disable-embedded-mode \
	--disable-libxml2 \
	--disable-doxygen \
	--disable-cairo \
	--disable-readme

%make_build

%check
make %{?_smp_mflags} check 

%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/bin/hwloc*
%{tpls_prefix}/bin/lstopo
%{tpls_prefix}/bin/lstopo-no-graphics
%{tpls_prefix}/include/hwloc.h
%{tpls_prefix}/include/hwloc/autogen/config.h
%{tpls_prefix}/include/hwloc/*.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libhwloc.a
%else
%{tpls_prefix}/lib/libhwloc.so
%{tpls_prefix}/lib/libhwloc.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/hwloc.pc
%{tpls_prefix}/sbin/hwloc-dump-hwdata
%{tpls_prefix}/share/hwloc/hwloc-valgrind.supp
%{tpls_prefix}/share/hwloc/hwloc-dump-hwdata.service

%files doc
%{tpls_prefix}/share/bash-completion/completions/hwloc
%{tpls_prefix}/share/doc/hwloc/dynamic_SVG_example.html
%{tpls_prefix}/share/doc/hwloc/hwloc-a4.pdf
%{tpls_prefix}/share/doc/hwloc/hwloc-letter.pdf
%{tpls_prefix}/share/hwloc/hwloc-ps.www/README
%{tpls_prefix}/share/hwloc/hwloc-ps.www/assets/index.html
%{tpls_prefix}/share/hwloc/hwloc-ps.www/assets/main.css
%{tpls_prefix}/share/hwloc/hwloc-ps.www/assets/script.js
%{tpls_prefix}/share/hwloc/hwloc-ps.www/assets/style.css
%{tpls_prefix}/share/hwloc/hwloc-ps.www/client.js
%{tpls_prefix}/share/hwloc/hwloc-ps.www/package.json
%{tpls_prefix}/share/hwloc/hwloc.dtd
%{tpls_prefix}/share/hwloc/hwloc2-diff.dtd
%{tpls_prefix}/share/hwloc/hwloc2.dtd
%{tpls_prefix}/share/man/man1/hw*
%{tpls_prefix}/share/man/man1/lstopo-no-graphics.1
%{tpls_prefix}/share/man/man1/lstopo.1
%{tpls_prefix}/share/man/man3/HWLOC*
%{tpls_prefix}/share/man/man3/hw*
%{tpls_prefix}/share/man/man7/hwloc.7

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.10.0-1
- Initial Package
