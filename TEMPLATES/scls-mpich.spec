%define scls_oflags -O2

Name:           scls-%{scls_flavor}-mpich
Version:        4.1.2
Release:        1%{?dist}
Summary:        A high-performance implementation of MPI

License:        MIT
URL:            https://www.mpich.org/
Source0:        https://www.mpich.org/static/downloads/%{version}/mpich-%{version}.tar.gz

BuildRequires: libpsm2-devel
BuildRequires: numactl-devel
BuildRequires: libuuid-devel
BuildRequires: libnl3-devel

BuildRequires:  scls-%{scls_flavor}-hwloc
Requires:       scls-%{scls_flavor}-hwloc

%description
MPICH is a high-performance and widely portable implementation of the Message
Passing Interface (MPI) standard (MPI-1, MPI-2 and MPI-3). The goals of MPICH
are: (1) to provide an MPI implementation that efficiently supports different
computation and communication platforms including commodity clusters (desktop
systems, shared-memory systems, multicore architectures), high-speed networks
(10 Gigabit Ethernet, InfiniBand, Myrinet, Quadrics) and proprietary high-end
computing systems (Blue Gene, Cray) and (2) to enable cutting-edge research in
MPI through an easy-to-extend modular framework for other derived
implementations.

The mpich binaries in this RPM packages were configured to use the default
process manager (Hydra) using the default device (ch3). The ch3 device
was configured with support for the nemesis channel that allows for
shared-memory and TCP/IP sockets based communication.

This build also include support for using the 'module environment' to select
which MPI implementation to use when multiple implementations are installed.
If you want MPICH support to be automatically loaded, you need to install the
mpich-autoload package.

%package doc
Summary:       Documentation files for MPICH
Requires:      scls-%{scls_flavor}-mpich == %{version}

BuildRequires: scls-%{scls_flavor}-pmix
Requires:      scls-%{scls_flavor}-pmix

%description doc
Documentation files for OpenMPI


%prep
%setup -q -n mpich-%{version}

%build
%{expand: %setup_scls_env}

CFLAGS+=" %{scls_oflags}"  \
CXXFLAGS+=" %{scls_oflags}"  \
%{scls_env} \
    ./configure \
        --prefix=%{scls_prefix} \
        --enable-fortran=all \
		--enable-cxx \
%if "%{scls_libs}" == "static"
		--enable-static \
		--disable-shared \
%else
		--enable-shared \
		--disable-static \
%endif
        --with-pmix-include=%{scls_prefix}/include \
        --with-pmix-lib=%{scls_prefix}/lib \
		--with-hwloc-include=%{scls_prefix}/include \
		--with-hwloc-lib=%{scls_prefix}/lib

%make_build		
%install
%make_install
%{scls_remove_la_files}

%files
%{scls_prefix}/bin/hydra_nameserver
%{scls_prefix}/bin/hydra_persist
%{scls_prefix}/bin/hydra_pmi_proxy
%{scls_prefix}/bin/mpic++
%{scls_prefix}/bin/mpicc
%{scls_prefix}/bin/mpichversion
%{scls_prefix}/bin/mpicxx
%{scls_prefix}/bin/mpiexec
%{scls_prefix}/bin/mpiexec.hydra
%{scls_prefix}/bin/mpif77
%{scls_prefix}/bin/mpif90
%{scls_prefix}/bin/mpifort
%{scls_prefix}/bin/mpirun
%{scls_prefix}/bin/mpivars
%{scls_prefix}/bin/parkill
%{scls_prefix}/include/mpi.h
%{scls_prefix}/include/mpi.mod
%{scls_prefix}/include/mpi_base.mod
%{scls_prefix}/include/mpi_c_interface.mod
%{scls_prefix}/include/mpi_c_interface_cdesc.mod
%{scls_prefix}/include/mpi_c_interface_glue.mod
%{scls_prefix}/include/mpi_c_interface_nobuf.mod
%{scls_prefix}/include/mpi_c_interface_types.mod
%{scls_prefix}/include/mpi_constants.mod
%{scls_prefix}/include/mpi_f08.mod
%{scls_prefix}/include/mpi_f08_callbacks.mod
%{scls_prefix}/include/mpi_f08_compile_constants.mod
%{scls_prefix}/include/mpi_f08_link_constants.mod
%{scls_prefix}/include/mpi_f08_types.mod
%{scls_prefix}/include/mpi_proto.h
%{scls_prefix}/include/mpi_sizeofs.mod
%{scls_prefix}/include/mpicxx.h
%{scls_prefix}/include/mpif.h
%{scls_prefix}/include/mpio.h
%{scls_prefix}/include/mpiof.h
%{scls_prefix}/include/pmpi_f08.mod
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libmpi.a
%{scls_prefix}/lib/libmpicxx.a
%{scls_prefix}/lib/libmpifort.a
%else
%{scls_prefix}/lib/libmpi.so
%{scls_prefix}/lib/libmpi.so.*
%{scls_prefix}/lib/libmpicxx.so
%{scls_prefix}/lib/libmpicxx.so.*
%{scls_prefix}/lib/libmpifort.so
%{scls_prefix}/lib/libmpifort.so.*
%{scls_prefix}/lib/libfmpich.so
%{scls_prefix}/lib/libmpich.so
%{scls_prefix}/lib/libmpichcxx.so
%{scls_prefix}/lib/libmpichf90.so
%{scls_prefix}/lib/libmpl.so
%{scls_prefix}/lib/libopa.so
%endif
%{scls_prefix}/lib/pkgconfig/mpich.pc
%{scls_prefix}/share/man/man1/hydra*.1
%{scls_prefix}/share/man/man1/mpi*.1
%{scls_prefix}/share/man/man3/MPI*.3
%{scls_prefix}/share/man/man3/mpiconsts.3

%files doc
%{scls_prefix}/share/doc/mpich

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 4.1.2-1
- Initial Package
