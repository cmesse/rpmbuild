%define scls_oflags -O2

Name:           scls-%{scls_flavor}-openmpi
Version:        5.0.1
Release:        1%{?dist}
Summary:        A powerful implementation of MPI/SHMEM

License:        BSD
URL:            https://www.open-mpi.org/
Source0:        https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-%{version}.tar.bz2

BuildRequires: make
BuildRequires: scls-%{scls_flavor}-libevent

Requires:      %{scls_rpm_cc}  >= %{scls_comp_minver}
Requires:      %{scls_rpm_cxx} >= %{scls_comp_minver}
Requires:      %{scls_rpm_fc}  >= %{scls_comp_minver}
Requires:      scls-%{scls_flavor}-libevent


BuildRequires: scls-%{scls_flavor}-hwloc
Requires:      scls-%{scls_flavor}-hwloc

BuildRequires: scls-%{scls_flavor}-pmix
Requires:      scls-%{scls_flavor}-pmix

BuildRequires: libpciaccess
BuildRequires: libpciaccess-devel
Requires:      libpciaccess

BuildRequires:  libfabric
BuildRequires:  libfabric-devel
Requires:  libfabric

BuildRequires: ucx
BuildRequires: ucx-devel
Requires: ucx

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%description
Open MPI is an open source implementation of the Message Passing
Interface specification (https://www.mpi-forum.org/) developed and
maintained by a consortium of research, academic, and industry
partners.

Open MPI also includes an implementation of the OpenSHMEM parallel
programming API (https://www.openshmem.org/).  OpenSHMEM is a
Partitioned Global Address Space (PGAS) abstraction layer, which
provides fast inter-process communication using one-sided
communication techniques.

This RPM contains all the tools necessary to compile, link, and run
Open MPI and OpenSHMEM jobs

%package doc
Summary:       Documentation files for OpenMPI
Requires:      scls-%{scls_flavor}-openmpi == %{version}

%description doc
Documentation files for OpenMPI

%prep
%setup -q -n openmpi-%{version}

%build

%{expand: %setup_scls_env}

%{scls_env} \
CC=%{scls_cc} CXX=%{scls_cxx} FC=%{scls_fc} \
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
   CC=%{scls_cc} \
   CXX=%{scls_cxx}  \
   FC=%{scls_fc} \
   F77=%{scls_fc} \
   --enable-mpi-fortran \
   --with-pmix=%{scls_prefix} \
   --with-hwloc=%{scls_prefix} \
   --with-hwloc-libdir=%{scls_prefix}/lib \
%if "%{scls_libs}" == "static"
   --enable-static \
   --disable-shared \
%else
   --disable-static \
   --enable-shared \
%endif
%if "%{scls_math}" == "cuda"
   --enable-mpi-ext=cuda \
   --with-cuda=%{scls_cuda} \
   --with-cuda-libdir=%{scls_cuda}/lib64 \
%endif
   --enable-mpi1-compatibility \
   --with-libevent-libdir=%{scls_prefix} \
   --disable-dlopen

%make_build

%check
make %{?_smp_mflags} test

%install
%make_install
%{scls_remove_la_files}


%files
%{scls_prefix}/bin/mpi*
%{scls_prefix}/bin/ompi_info
%{scls_prefix}/bin/opal_wrapper
%{scls_prefix}/bin/os*
%{scls_prefix}/bin/p*
%{scls_prefix}/bin/sh*
%{scls_prefix}/etc/openmpi-mca-params.conf
%{scls_prefix}/etc/openmpi-totalview.tcl
%{scls_prefix}/etc/prte-default-hostfile
%{scls_prefix}/etc/prte-mca-params.conf
%{scls_prefix}/etc/prte.conf
%{scls_prefix}/include/mpi*.h
%{scls_prefix}/include/openmpi
%{scls_prefix}/include/prte
%{scls_prefix}/include/mpp
%{scls_prefix}/include/openshmem
%{scls_prefix}/include/p*.h
%{scls_prefix}/include/s*.h
%{scls_prefix}/include/shmem.fh

%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libmpi.a
%{scls_prefix}/lib/libmpi_mpifh.a
%{scls_prefix}/lib/libmpi_usempi_ignore_tkr.a
%{scls_prefix}/lib/libmpi_usempif08.a
%{scls_prefix}/lib/libopen-pal.a
%{scls_prefix}/lib/libprrte.a
%{scls_prefix}/lib/openmpi/libompi_dbg_msgq.a
%{scls_prefix}/lib/liboshmem.a
%else
%{scls_prefix}/lib/libmpi.so
%{scls_prefix}/lib/libmpi.so.*
%{scls_prefix}/lib/libmpi_mpifh.so
%{scls_prefix}/lib/libmpi_mpifh.so.*
%{scls_prefix}/lib/libmpi_usempi_ignore_tkr.so
%{scls_prefix}/lib/libmpi_usempi_ignore_tkr.so.*
%{scls_prefix}/lib/libmpi_usempif08.so
%{scls_prefix}/lib/libmpi_usempif08.so.*
%{scls_prefix}/lib/libopen-pal.so
%{scls_prefix}/lib/libopen-pal.so.*
%{scls_prefix}/lib/libprrte.so
%{scls_prefix}/lib/libprrte.so.*
%{scls_prefix}/lib/openmpi/libompi_dbg_msgq.so
%{scls_prefix}/lib/liboshmem.so
%{scls_prefix}/lib/liboshmem.so.*
%endif
%{scls_prefix}/lib/mpi.mod
%{scls_prefix}/lib/mpi_ext.mod
%{scls_prefix}/lib/mpi_f08.mod
%{scls_prefix}/lib/mpi_f08_callbacks.mod
%{scls_prefix}/lib/mpi_f08_ext.mod
%{scls_prefix}/lib/mpi_f08_interfaces.mod
%{scls_prefix}/lib/mpi_f08_interfaces_callbacks.mod
%{scls_prefix}/lib/mpi_f08_types.mod
%{scls_prefix}/lib/mpi_types.mod
%{scls_prefix}/lib/pkgconfig/ompi-c.pc
%{scls_prefix}/lib/pkgconfig/ompi-cxx.pc
%{scls_prefix}/lib/pkgconfig/ompi-f77.pc
%{scls_prefix}/lib/pkgconfig/ompi-f90.pc
%{scls_prefix}/lib/pkgconfig/ompi-fort.pc
%{scls_prefix}/lib/pkgconfig/ompi.pc
%{scls_prefix}/lib/pkgconfig/oshmem-c.pc
%{scls_prefix}/lib/pkgconfig/oshmem-cxx.pc
%{scls_prefix}/lib/pkgconfig/oshmem-fort.pc
%{scls_prefix}/lib/pkgconfig/oshmem.pc
%{scls_prefix}/lib/pmpi_f08_interfaces.mod
%{scls_prefix}/share/openmpi/amca-param-sets/example.conf
%{scls_prefix}/share/openmpi/amca-param-sets/ft-mpi
%{scls_prefix}/share/openmpi/*.txt
%{scls_prefix}/share/openmpi/openmpi-valgrind.supp
%{scls_prefix}/share/prte/amca-param-sets/example.conf
%{scls_prefix}/share/prte/help*.txt
%{scls_prefix}/share/prte/rst/prrte-rst-content/*.rst
%{scls_prefix}/share/prte/rst/schizo-ompi-rst-content/schizo-ompi-cli.rstxt

%files doc
%{scls_prefix}/share/doc/openmpi/html
%{scls_prefix}/share/doc/prrte/html
%{scls_prefix}/share/man/man1/*.1
%{scls_prefix}/share/man/man3/*.3
%{scls_prefix}/share/man/man5/*.5
%{scls_prefix}/share/man/man7/*.7

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 5.0.1-1
- Initial Package

