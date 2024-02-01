Name:           tpls-%{tpls_flavor}-mpich
Version:        4.1.2
Release:        1%{?dist}
Summary:        A high-performance implementation of MPI

License:        MIT
URL:            https://www.mpich.org/
Source0:        https://www.mpich.org/static/downloads/%{version}/mpich-%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-hwloc
Requires:       tpls-%{tpls_flavor}-hwloc

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
Requires:      tpls-%{tpls_flavor}-mpich == %{version} 

%description doc
Documentation files for OpenMPI


%prep
%setup -q -n mpich-%{version}

%build
%{expand: %setup_tpls_env}

%{tpls_env} \
    ./configure \
        --prefix=%{tpls_prefix} \
        --enable-fortran=all \
		--enable-cxx \
%if "%{tpls_libs}" == "static"
		--enable-static \
		--disable-shared \
%else
		--enable-shared \
		--disable-static \
%endif
		--with-hwloc-include=%{tpls_prefix}/include \
		--with-hwloc-lib=%{tpls_prefix}/lib

%make_build		
%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/bin/hydra_nameserver
%{tpls_prefix}/bin/hydra_persist
%{tpls_prefix}/bin/hydra_pmi_proxy
%{tpls_prefix}/bin/mpic++
%{tpls_prefix}/bin/mpicc
%{tpls_prefix}/bin/mpichversion
%{tpls_prefix}/bin/mpicxx
%{tpls_prefix}/bin/mpiexec
%{tpls_prefix}/bin/mpiexec.hydra
%{tpls_prefix}/bin/mpif77
%{tpls_prefix}/bin/mpif90
%{tpls_prefix}/bin/mpifort
%{tpls_prefix}/bin/mpirun
%{tpls_prefix}/bin/mpivars
%{tpls_prefix}/bin/parkill
%{tpls_prefix}/include/mpi.h
%{tpls_prefix}/include/mpi.mod
%{tpls_prefix}/include/mpi_base.mod
%{tpls_prefix}/include/mpi_c_interface.mod
%{tpls_prefix}/include/mpi_c_interface_cdesc.mod
%{tpls_prefix}/include/mpi_c_interface_glue.mod
%{tpls_prefix}/include/mpi_c_interface_nobuf.mod
%{tpls_prefix}/include/mpi_c_interface_types.mod
%{tpls_prefix}/include/mpi_constants.mod
%{tpls_prefix}/include/mpi_f08.mod
%{tpls_prefix}/include/mpi_f08_callbacks.mod
%{tpls_prefix}/include/mpi_f08_compile_constants.mod
%{tpls_prefix}/include/mpi_f08_link_constants.mod
%{tpls_prefix}/include/mpi_f08_types.mod
%{tpls_prefix}/include/mpi_proto.h
%{tpls_prefix}/include/mpi_sizeofs.mod
%{tpls_prefix}/include/mpicxx.h
%{tpls_prefix}/include/mpif.h
%{tpls_prefix}/include/mpio.h
%{tpls_prefix}/include/mpiof.h
%{tpls_prefix}/include/pmpi_f08.mod
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libmpi.a
%{tpls_prefix}/lib/libmpicxx.a
%{tpls_prefix}/lib/libmpifort.a
%else
%{tpls_prefix}/lib/libmpi.so
%{tpls_prefix}/lib/libmpi.so.*
%{tpls_prefix}/lib/libmpicxx.so
%{tpls_prefix}/lib/libmpicxx.so.*
%{tpls_prefix}/lib/libmpifort.so
%{tpls_prefix}/lib/libmpifort.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/mpich.pc
%{tpls_prefix}/share/man/man1/hydra*.1
%{tpls_prefix}/share/man/man1/mpi*.1
%{tpls_prefix}/share/man/man3/MPI*.3
%{tpls_prefix}/share/man/man3/mpiconsts.3

%files doc
%{tpls_prefix}/share/doc/mpich

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 4.1.2-1
- Initial Package
