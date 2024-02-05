%define scls_oflags -O3

Name:           scls-%{scls_flavor}-hwloc
Version:        2.10.0
Release:        1%{?dist}
Summary:        Portable Hardware Locality

License:        BSD
URL:            https://www-lb.open-mpi.org/software/hwloc/v2.10/
Source0:        https://download.open-mpi.org/release/hwloc/v2.10/hwloc-2.10.0.tar.bz2

Requires:      %{scls_rpm_cc}  >= %{scls_comp_minver}
Requires:      %{scls_rpm_cxx} >= %{scls_comp_minver}
Requires:      %{scls_rpm_fc}  >= %{scls_comp_minver}
Requires:      scls-%{scls_flavor}-libevent

BuildRequires: scls-%{scls_flavor}-libevent
Requires: scls-%{scls_flavor}-libevent



%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
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
%{setup_scls_env}

%{scls_env}
%if "%{scls_libs}" == "static"
CFLAGS+="  -DHAVE_UNIX_BYTESWAP %{scls_oflags}" \
CXXFLAGS+=" -DHAVE_UNIX_BYTESWAP %{scls_oflags}" \
FCFLAGS+="  -DHAVE_UNIX_BYTESWAP %{scls_oflags}" \
%else
CFLAGS+=" -fPIC -DHAVE_UNIX_BYTESWAP %{scls_oflags}" \
CXXFLAGS+=" -fPIC -DHAVE_UNIX_BYTESWAP %{scls_oflags}" \
FCFLAGS+=" -fPIC -DHAVE_UNIX_BYTESWAP %{scls_oflags}" \
%endif
./configure \
   --prefix=%{scls_prefix} \
%if "%{scls_libs}" == "static"
   --enable-static \
   --disable-shared \
%else
   --disable-static \
   --enable-shared \
%endif
%if "%{scls_math}" == "cuda"
   --with-cuda=%{scls_cuda} \
   --enable-nvml \
%else
    --disable-cuda \
    --disable-nvml \
%endif
	--disable-rocm \
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
%{scls_remove_la_files}

%files
%{scls_prefix}/bin/hwloc*
%{scls_prefix}/bin/lstopo
%{scls_prefix}/bin/lstopo-no-graphics
%{scls_prefix}/include/hwloc.h
%{scls_prefix}/include/hwloc/autogen/config.h
%{scls_prefix}/include/hwloc/*.h
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libhwloc.a
%else
%{scls_prefix}/lib/libhwloc.so
%{scls_prefix}/lib/libhwloc.so.*
%endif
%{scls_prefix}/lib/pkgconfig/hwloc.pc
%{scls_prefix}/sbin/hwloc-dump-hwdata
%{scls_prefix}/share/hwloc/hwloc-valgrind.supp
%{scls_prefix}/share/hwloc/hwloc-dump-hwdata.service

%files doc
%{scls_prefix}/share/bash-completion/completions/hwloc
%{scls_prefix}/share/doc/hwloc/dynamic_SVG_example.html
%{scls_prefix}/share/doc/hwloc/hwloc-a4.pdf
%{scls_prefix}/share/doc/hwloc/hwloc-letter.pdf
%{scls_prefix}/share/hwloc/hwloc-ps.www/README
%{scls_prefix}/share/hwloc/hwloc-ps.www/assets/index.html
%{scls_prefix}/share/hwloc/hwloc-ps.www/assets/main.css
%{scls_prefix}/share/hwloc/hwloc-ps.www/assets/script.js
%{scls_prefix}/share/hwloc/hwloc-ps.www/assets/style.css
%{scls_prefix}/share/hwloc/hwloc-ps.www/client.js
%{scls_prefix}/share/hwloc/hwloc-ps.www/package.json
%{scls_prefix}/share/hwloc/hwloc.dtd
%{scls_prefix}/share/hwloc/hwloc2-diff.dtd
%{scls_prefix}/share/hwloc/hwloc2.dtd
%{scls_prefix}/share/man/man1/hw*
%{scls_prefix}/share/man/man1/lstopo-no-graphics.1
%{scls_prefix}/share/man/man1/lstopo.1
%{scls_prefix}/share/man/man3/HWLOC*
%{scls_prefix}/share/man/man3/hw*
%{scls_prefix}/share/man/man7/hwloc.7

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2.10.0-1
- Initial Package
