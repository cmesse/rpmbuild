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

BuildRequires: libpciaccess-devel
Requires: libpciaccess-devel

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

%{setup_scls_env}
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
%{scls_prefix}/bin/mpiCC
%{scls_prefix}/bin/mpic++
%{scls_prefix}/bin/mpicc
%{scls_prefix}/bin/mpicxx
%{scls_prefix}/bin/mpiexec
%{scls_prefix}/bin/mpif77
%{scls_prefix}/bin/mpif90
%{scls_prefix}/bin/mpifort
%{scls_prefix}/bin/mpirun
%{scls_prefix}/bin/ompi_info
%{scls_prefix}/bin/opal_wrapper
%{scls_prefix}/bin/oshrun
%{scls_prefix}/bin/pattrs
%{scls_prefix}/bin/pctrl
%{scls_prefix}/bin/pevent
%{scls_prefix}/bin/plookup
%{scls_prefix}/bin/pmix_info
%{scls_prefix}/bin/pmixcc
%{scls_prefix}/bin/pps
%{scls_prefix}/bin/pquery
%{scls_prefix}/bin/prte
%{scls_prefix}/bin/prte_info
%{scls_prefix}/bin/prted
%{scls_prefix}/bin/prterun
%{scls_prefix}/bin/prun
%{scls_prefix}/bin/pterm
%{scls_prefix}/etc/openmpi-mca-params.conf
%{scls_prefix}/etc/openmpi-totalview.tcl
%{scls_prefix}/etc/pmix-mca-params.conf
%{scls_prefix}/etc/prte-default-hostfile
%{scls_prefix}/etc/prte-mca-params.conf
%{scls_prefix}/etc/prte.conf
%{scls_prefix}/include/mpi-ext.h
%{scls_prefix}/include/mpi.h
%{scls_prefix}/include/mpi_portable_platform.h
%{scls_prefix}/include/mpif-c-constants-decl.h
%{scls_prefix}/include/mpif-config.h
%{scls_prefix}/include/mpif-constants.h
%{scls_prefix}/include/mpif-ext.h
%{scls_prefix}/include/mpif-externals.h
%{scls_prefix}/include/mpif-handles.h
%{scls_prefix}/include/mpif-io-constants.h
%{scls_prefix}/include/mpif-io-handles.h
%{scls_prefix}/include/mpif-sentinels.h
%{scls_prefix}/include/mpif-sizeof.h
%{scls_prefix}/include/mpif.h
%{scls_prefix}/include/openmpi/mpiext/*.h
%{scls_prefix}/include/pmix.h
%{scls_prefix}/include/pmix
%{scls_prefix}/include/pmix*.h
%{scls_prefix}/include/prte.h
%{scls_prefix}/include/prte
%{scls_prefix}/include/prte*.h

%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libmpi.a
%{scls_prefix}/lib/libmpi_mpifh.a
%{scls_prefix}/lib/libmpi_usempi_ignore_tkr.a
%{scls_prefix}/lib/libmpi_usempif08.a
%{scls_prefix}/lib/libopen-pal.a
#%{scls_prefix}/lib/libpmix.a
%{scls_prefix}/lib/libprrte.a
%{scls_prefix}/lib/openmpi/libompi_dbg_msgq.a
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
%{scls_prefix}/lib/libpmix.so
%{scls_prefix}/lib/libpmix.so.*
%{scls_prefix}/lib/libprrte.so
%{scls_prefix}/lib/libprrte.so.*
%{scls_prefix}/lib/openmpi/libompi_dbg_msgq.so
#%{scls_prefix}/lib/pmix/pmix_mca_pcompress_zlib.so
#%{scls_prefix}/lib/pmix/pmix_mca_prm_default.so
#%{scls_prefix}/lib/pmix/pmix_mca_prm_slurm.so
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
%{scls_prefix}/lib/pkgconfig/pmix.pc
%{scls_prefix}/lib/pmpi_f08_interfaces.mod
%{scls_prefix}/share/openmpi/amca-param-sets/example.conf
%{scls_prefix}/share/openmpi/amca-param-sets/ft-mpi
%{scls_prefix}/share/openmpi/help*.txt
%{scls_prefix}/share/openmpi/mpi*.txt
%{scls_prefix}/share/openmpi/openmpi-valgrind.supp
%{scls_prefix}/share/pmix/help-*.txt
%{scls_prefix}/share/pmix/pmix-valgrind.supp
%{scls_prefix}/share/pmix/pmixcc-wrapper-data.txt
%{scls_prefix}/share/prte/amca-param-sets/example.conf
%{scls_prefix}/share/prte/help*.txt
%{scls_prefix}/share/prte/rst/prrte-rst-content/*.rst
%{scls_prefix}/share/prte/rst/schizo-ompi-rst-content/schizo-ompi-cli.rstxt

%files doc
%{scls_prefix}/share/doc/openmpi/html
%{scls_prefix}/share/doc/pmix/html
%{scls_prefix}/share/doc/prrte/html
%{scls_prefix}/share/man/man1/mpic++.1
%{scls_prefix}/share/man/man1/mpicc.1
%{scls_prefix}/share/man/man1/mpicxx.1
%{scls_prefix}/share/man/man1/mpif77.1
%{scls_prefix}/share/man/man1/mpif90.1
%{scls_prefix}/share/man/man1/mpifort.1
%{scls_prefix}/share/man/man1/mpirun.1
%{scls_prefix}/share/man/man1/mpisync.1
%{scls_prefix}/share/man/man1/ompi-wrapper-compiler.1
%{scls_prefix}/share/man/man1/ompi_info.1
%{scls_prefix}/share/man/man1/opal_wrapper.1
%{scls_prefix}/share/man/man1/pmix_info.1
%{scls_prefix}/share/man/man1/prte.1
%{scls_prefix}/share/man/man1/prte_info.1
%{scls_prefix}/share/man/man1/prted.1
%{scls_prefix}/share/man/man1/prterun.1
%{scls_prefix}/share/man/man1/prun.1
%{scls_prefix}/share/man/man1/pterm.1
%{scls_prefix}/share/man/man3/MPIX_Comm_ack_failed.3
%{scls_prefix}/share/man/man3/MPIX_Comm_agree.3
%{scls_prefix}/share/man/man3/MPIX_Comm_get_failed.3
%{scls_prefix}/share/man/man3/MPIX_Comm_iagree.3
%{scls_prefix}/share/man/man3/MPIX_Comm_is_revoked.3
%{scls_prefix}/share/man/man3/MPIX_Comm_ishrink.3
%{scls_prefix}/share/man/man3/MPIX_Comm_revoke.3
%{scls_prefix}/share/man/man3/MPIX_Comm_shrink.3
%{scls_prefix}/share/man/man3/MPIX_Query_cuda_support.3
%{scls_prefix}/share/man/man3/MPIX_Query_rocm_support.3
%{scls_prefix}/share/man/man3/MPI_Abort.3
%{scls_prefix}/share/man/man3/MPI_Accumulate.3
%{scls_prefix}/share/man/man3/MPI_Add_error_class.3
%{scls_prefix}/share/man/man3/MPI_Add_error_code.3
%{scls_prefix}/share/man/man3/MPI_Add_error_string.3
%{scls_prefix}/share/man/man3/MPI_Address.3
%{scls_prefix}/share/man/man3/MPI_Aint_add.3
%{scls_prefix}/share/man/man3/MPI_Aint_diff.3
%{scls_prefix}/share/man/man3/MPI_Allgather.3
%{scls_prefix}/share/man/man3/MPI_Allgather_init.3
%{scls_prefix}/share/man/man3/MPI_Allgatherv.3
%{scls_prefix}/share/man/man3/MPI_Allgatherv_init.3
%{scls_prefix}/share/man/man3/MPI_Alloc_mem.3
%{scls_prefix}/share/man/man3/MPI_Allreduce.3
%{scls_prefix}/share/man/man3/MPI_Allreduce_init.3
%{scls_prefix}/share/man/man3/MPI_Alltoall.3
%{scls_prefix}/share/man/man3/MPI_Alltoall_init.3
%{scls_prefix}/share/man/man3/MPI_Alltoallv.3
%{scls_prefix}/share/man/man3/MPI_Alltoallv_init.3
%{scls_prefix}/share/man/man3/MPI_Alltoallw.3
%{scls_prefix}/share/man/man3/MPI_Alltoallw_init.3
%{scls_prefix}/share/man/man3/MPI_Attr_delete.3
%{scls_prefix}/share/man/man3/MPI_Attr_get.3
%{scls_prefix}/share/man/man3/MPI_Attr_put.3
%{scls_prefix}/share/man/man3/MPI_Barrier.3
%{scls_prefix}/share/man/man3/MPI_Barrier_init.3
%{scls_prefix}/share/man/man3/MPI_Bcast.3
%{scls_prefix}/share/man/man3/MPI_Bcast_init.3
%{scls_prefix}/share/man/man3/MPI_Bsend.3
%{scls_prefix}/share/man/man3/MPI_Bsend_init.3
%{scls_prefix}/share/man/man3/MPI_Buffer_attach.3
%{scls_prefix}/share/man/man3/MPI_Buffer_detach.3
%{scls_prefix}/share/man/man3/MPI_Cancel.3
%{scls_prefix}/share/man/man3/MPI_Cart_coords.3
%{scls_prefix}/share/man/man3/MPI_Cart_create.3
%{scls_prefix}/share/man/man3/MPI_Cart_get.3
%{scls_prefix}/share/man/man3/MPI_Cart_map.3
%{scls_prefix}/share/man/man3/MPI_Cart_rank.3
%{scls_prefix}/share/man/man3/MPI_Cart_shift.3
%{scls_prefix}/share/man/man3/MPI_Cart_sub.3
%{scls_prefix}/share/man/man3/MPI_Cartdim_get.3
%{scls_prefix}/share/man/man3/MPI_Close_port.3
%{scls_prefix}/share/man/man3/MPI_Comm_accept.3
%{scls_prefix}/share/man/man3/MPI_Comm_c2f.3
%{scls_prefix}/share/man/man3/MPI_Comm_call_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Comm_compare.3
%{scls_prefix}/share/man/man3/MPI_Comm_connect.3
%{scls_prefix}/share/man/man3/MPI_Comm_create.3
%{scls_prefix}/share/man/man3/MPI_Comm_create_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Comm_create_from_group.3
%{scls_prefix}/share/man/man3/MPI_Comm_create_group.3
%{scls_prefix}/share/man/man3/MPI_Comm_create_keyval.3
%{scls_prefix}/share/man/man3/MPI_Comm_delete_attr.3
%{scls_prefix}/share/man/man3/MPI_Comm_disconnect.3
%{scls_prefix}/share/man/man3/MPI_Comm_dup.3
%{scls_prefix}/share/man/man3/MPI_Comm_dup_with_info.3
%{scls_prefix}/share/man/man3/MPI_Comm_f2c.3
%{scls_prefix}/share/man/man3/MPI_Comm_free.3
%{scls_prefix}/share/man/man3/MPI_Comm_free_keyval.3
%{scls_prefix}/share/man/man3/MPI_Comm_get_attr.3
%{scls_prefix}/share/man/man3/MPI_Comm_get_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Comm_get_info.3
%{scls_prefix}/share/man/man3/MPI_Comm_get_name.3
%{scls_prefix}/share/man/man3/MPI_Comm_get_parent.3
%{scls_prefix}/share/man/man3/MPI_Comm_group.3
%{scls_prefix}/share/man/man3/MPI_Comm_idup.3
%{scls_prefix}/share/man/man3/MPI_Comm_idup_with_info.3
%{scls_prefix}/share/man/man3/MPI_Comm_join.3
%{scls_prefix}/share/man/man3/MPI_Comm_rank.3
%{scls_prefix}/share/man/man3/MPI_Comm_remote_group.3
%{scls_prefix}/share/man/man3/MPI_Comm_remote_size.3
%{scls_prefix}/share/man/man3/MPI_Comm_set_attr.3
%{scls_prefix}/share/man/man3/MPI_Comm_set_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Comm_set_info.3
%{scls_prefix}/share/man/man3/MPI_Comm_set_name.3
%{scls_prefix}/share/man/man3/MPI_Comm_size.3
%{scls_prefix}/share/man/man3/MPI_Comm_spawn.3
%{scls_prefix}/share/man/man3/MPI_Comm_spawn_multiple.3
%{scls_prefix}/share/man/man3/MPI_Comm_split.3
%{scls_prefix}/share/man/man3/MPI_Comm_split_type.3
%{scls_prefix}/share/man/man3/MPI_Comm_test_inter.3
%{scls_prefix}/share/man/man3/MPI_Compare_and_swap.3
%{scls_prefix}/share/man/man3/MPI_Dims_create.3
%{scls_prefix}/share/man/man3/MPI_Dist_graph_create.3
%{scls_prefix}/share/man/man3/MPI_Dist_graph_create_adjacent.3
%{scls_prefix}/share/man/man3/MPI_Dist_graph_neighbors.3
%{scls_prefix}/share/man/man3/MPI_Dist_graph_neighbors_count.3
%{scls_prefix}/share/man/man3/MPI_Errhandler_create.3
%{scls_prefix}/share/man/man3/MPI_Errhandler_free.3
%{scls_prefix}/share/man/man3/MPI_Errhandler_get.3
%{scls_prefix}/share/man/man3/MPI_Errhandler_set.3
%{scls_prefix}/share/man/man3/MPI_Error_class.3
%{scls_prefix}/share/man/man3/MPI_Error_string.3
%{scls_prefix}/share/man/man3/MPI_Exscan.3
%{scls_prefix}/share/man/man3/MPI_Exscan_init.3
%{scls_prefix}/share/man/man3/MPI_Fetch_and_op.3
%{scls_prefix}/share/man/man3/MPI_File_c2f.3
%{scls_prefix}/share/man/man3/MPI_File_call_errhandler.3
%{scls_prefix}/share/man/man3/MPI_File_close.3
%{scls_prefix}/share/man/man3/MPI_File_create_errhandler.3
%{scls_prefix}/share/man/man3/MPI_File_delete.3
%{scls_prefix}/share/man/man3/MPI_File_f2c.3
%{scls_prefix}/share/man/man3/MPI_File_get_amode.3
%{scls_prefix}/share/man/man3/MPI_File_get_atomicity.3
%{scls_prefix}/share/man/man3/MPI_File_get_byte_offset.3
%{scls_prefix}/share/man/man3/MPI_File_get_errhandler.3
%{scls_prefix}/share/man/man3/MPI_File_get_group.3
%{scls_prefix}/share/man/man3/MPI_File_get_info.3
%{scls_prefix}/share/man/man3/MPI_File_get_position.3
%{scls_prefix}/share/man/man3/MPI_File_get_position_shared.3
%{scls_prefix}/share/man/man3/MPI_File_get_size.3
%{scls_prefix}/share/man/man3/MPI_File_get_type_extent.3
%{scls_prefix}/share/man/man3/MPI_File_get_view.3
%{scls_prefix}/share/man/man3/MPI_File_iread.3
%{scls_prefix}/share/man/man3/MPI_File_iread_all.3
%{scls_prefix}/share/man/man3/MPI_File_iread_at.3
%{scls_prefix}/share/man/man3/MPI_File_iread_at_all.3
%{scls_prefix}/share/man/man3/MPI_File_iread_shared.3
%{scls_prefix}/share/man/man3/MPI_File_iwrite.3
%{scls_prefix}/share/man/man3/MPI_File_iwrite_all.3
%{scls_prefix}/share/man/man3/MPI_File_iwrite_at.3
%{scls_prefix}/share/man/man3/MPI_File_iwrite_at_all.3
%{scls_prefix}/share/man/man3/MPI_File_iwrite_shared.3
%{scls_prefix}/share/man/man3/MPI_File_open.3
%{scls_prefix}/share/man/man3/MPI_File_preallocate.3
%{scls_prefix}/share/man/man3/MPI_File_read.3
%{scls_prefix}/share/man/man3/MPI_File_read_all.3
%{scls_prefix}/share/man/man3/MPI_File_read_all_begin.3
%{scls_prefix}/share/man/man3/MPI_File_read_all_end.3
%{scls_prefix}/share/man/man3/MPI_File_read_at.3
%{scls_prefix}/share/man/man3/MPI_File_read_at_all.3
%{scls_prefix}/share/man/man3/MPI_File_read_at_all_begin.3
%{scls_prefix}/share/man/man3/MPI_File_read_at_all_end.3
%{scls_prefix}/share/man/man3/MPI_File_read_ordered.3
%{scls_prefix}/share/man/man3/MPI_File_read_ordered_begin.3
%{scls_prefix}/share/man/man3/MPI_File_read_ordered_end.3
%{scls_prefix}/share/man/man3/MPI_File_read_shared.3
%{scls_prefix}/share/man/man3/MPI_File_seek.3
%{scls_prefix}/share/man/man3/MPI_File_seek_shared.3
%{scls_prefix}/share/man/man3/MPI_File_set_atomicity.3
%{scls_prefix}/share/man/man3/MPI_File_set_errhandler.3
%{scls_prefix}/share/man/man3/MPI_File_set_info.3
%{scls_prefix}/share/man/man3/MPI_File_set_size.3
%{scls_prefix}/share/man/man3/MPI_File_set_view.3
%{scls_prefix}/share/man/man3/MPI_File_sync.3
%{scls_prefix}/share/man/man3/MPI_File_write.3
%{scls_prefix}/share/man/man3/MPI_File_write_all.3
%{scls_prefix}/share/man/man3/MPI_File_write_all_begin.3
%{scls_prefix}/share/man/man3/MPI_File_write_all_end.3
%{scls_prefix}/share/man/man3/MPI_File_write_at.3
%{scls_prefix}/share/man/man3/MPI_File_write_at_all.3
%{scls_prefix}/share/man/man3/MPI_File_write_at_all_begin.3
%{scls_prefix}/share/man/man3/MPI_File_write_at_all_end.3
%{scls_prefix}/share/man/man3/MPI_File_write_ordered.3
%{scls_prefix}/share/man/man3/MPI_File_write_ordered_begin.3
%{scls_prefix}/share/man/man3/MPI_File_write_ordered_end.3
%{scls_prefix}/share/man/man3/MPI_File_write_shared.3
%{scls_prefix}/share/man/man3/MPI_Finalize.3
%{scls_prefix}/share/man/man3/MPI_Finalized.3
%{scls_prefix}/share/man/man3/MPI_Free_mem.3
%{scls_prefix}/share/man/man3/MPI_Gather.3
%{scls_prefix}/share/man/man3/MPI_Gather_init.3
%{scls_prefix}/share/man/man3/MPI_Gatherv.3
%{scls_prefix}/share/man/man3/MPI_Gatherv_init.3
%{scls_prefix}/share/man/man3/MPI_Get.3
%{scls_prefix}/share/man/man3/MPI_Get_accumulate.3
%{scls_prefix}/share/man/man3/MPI_Get_address.3
%{scls_prefix}/share/man/man3/MPI_Get_count.3
%{scls_prefix}/share/man/man3/MPI_Get_elements.3
%{scls_prefix}/share/man/man3/MPI_Get_elements_x.3
%{scls_prefix}/share/man/man3/MPI_Get_library_version.3
%{scls_prefix}/share/man/man3/MPI_Get_processor_name.3
%{scls_prefix}/share/man/man3/MPI_Get_version.3
%{scls_prefix}/share/man/man3/MPI_Graph_create.3
%{scls_prefix}/share/man/man3/MPI_Graph_get.3
%{scls_prefix}/share/man/man3/MPI_Graph_map.3
%{scls_prefix}/share/man/man3/MPI_Graph_neighbors.3
%{scls_prefix}/share/man/man3/MPI_Graph_neighbors_count.3
%{scls_prefix}/share/man/man3/MPI_Graphdims_get.3
%{scls_prefix}/share/man/man3/MPI_Grequest_complete.3
%{scls_prefix}/share/man/man3/MPI_Grequest_start.3
%{scls_prefix}/share/man/man3/MPI_Group_c2f.3
%{scls_prefix}/share/man/man3/MPI_Group_compare.3
%{scls_prefix}/share/man/man3/MPI_Group_difference.3
%{scls_prefix}/share/man/man3/MPI_Group_excl.3
%{scls_prefix}/share/man/man3/MPI_Group_f2c.3
%{scls_prefix}/share/man/man3/MPI_Group_free.3
%{scls_prefix}/share/man/man3/MPI_Group_from_session_pset.3
%{scls_prefix}/share/man/man3/MPI_Group_incl.3
%{scls_prefix}/share/man/man3/MPI_Group_intersection.3
%{scls_prefix}/share/man/man3/MPI_Group_range_excl.3
%{scls_prefix}/share/man/man3/MPI_Group_range_incl.3
%{scls_prefix}/share/man/man3/MPI_Group_rank.3
%{scls_prefix}/share/man/man3/MPI_Group_size.3
%{scls_prefix}/share/man/man3/MPI_Group_translate_ranks.3
%{scls_prefix}/share/man/man3/MPI_Group_union.3
%{scls_prefix}/share/man/man3/MPI_Iallgather.3
%{scls_prefix}/share/man/man3/MPI_Iallgatherv.3
%{scls_prefix}/share/man/man3/MPI_Iallreduce.3
%{scls_prefix}/share/man/man3/MPI_Ialltoall.3
%{scls_prefix}/share/man/man3/MPI_Ialltoallv.3
%{scls_prefix}/share/man/man3/MPI_Ialltoallw.3
%{scls_prefix}/share/man/man3/MPI_Ibarrier.3
%{scls_prefix}/share/man/man3/MPI_Ibcast.3
%{scls_prefix}/share/man/man3/MPI_Ibsend.3
%{scls_prefix}/share/man/man3/MPI_Iexscan.3
%{scls_prefix}/share/man/man3/MPI_Igather.3
%{scls_prefix}/share/man/man3/MPI_Igatherv.3
%{scls_prefix}/share/man/man3/MPI_Improbe.3
%{scls_prefix}/share/man/man3/MPI_Imrecv.3
%{scls_prefix}/share/man/man3/MPI_Ineighbor_allgather.3
%{scls_prefix}/share/man/man3/MPI_Ineighbor_allgatherv.3
%{scls_prefix}/share/man/man3/MPI_Ineighbor_alltoall.3
%{scls_prefix}/share/man/man3/MPI_Ineighbor_alltoallv.3
%{scls_prefix}/share/man/man3/MPI_Ineighbor_alltoallw.3
%{scls_prefix}/share/man/man3/MPI_Info_c2f.3
%{scls_prefix}/share/man/man3/MPI_Info_create.3
%{scls_prefix}/share/man/man3/MPI_Info_delete.3
%{scls_prefix}/share/man/man3/MPI_Info_dup.3
%{scls_prefix}/share/man/man3/MPI_Info_env.3
%{scls_prefix}/share/man/man3/MPI_Info_f2c.3
%{scls_prefix}/share/man/man3/MPI_Info_free.3
%{scls_prefix}/share/man/man3/MPI_Info_get.3
%{scls_prefix}/share/man/man3/MPI_Info_get_nkeys.3
%{scls_prefix}/share/man/man3/MPI_Info_get_nthkey.3
%{scls_prefix}/share/man/man3/MPI_Info_get_string.3
%{scls_prefix}/share/man/man3/MPI_Info_get_valuelen.3
%{scls_prefix}/share/man/man3/MPI_Info_set.3
%{scls_prefix}/share/man/man3/MPI_Init.3
%{scls_prefix}/share/man/man3/MPI_Init_thread.3
%{scls_prefix}/share/man/man3/MPI_Initialized.3
%{scls_prefix}/share/man/man3/MPI_Intercomm_create.3
%{scls_prefix}/share/man/man3/MPI_Intercomm_create_from_groups.3
%{scls_prefix}/share/man/man3/MPI_Intercomm_merge.3
%{scls_prefix}/share/man/man3/MPI_Iprobe.3
%{scls_prefix}/share/man/man3/MPI_Irecv.3
%{scls_prefix}/share/man/man3/MPI_Ireduce.3
%{scls_prefix}/share/man/man3/MPI_Ireduce_scatter.3
%{scls_prefix}/share/man/man3/MPI_Ireduce_scatter_block.3
%{scls_prefix}/share/man/man3/MPI_Irsend.3
%{scls_prefix}/share/man/man3/MPI_Is_thread_main.3
%{scls_prefix}/share/man/man3/MPI_Iscan.3
%{scls_prefix}/share/man/man3/MPI_Iscatter.3
%{scls_prefix}/share/man/man3/MPI_Iscatterv.3
%{scls_prefix}/share/man/man3/MPI_Isend.3
%{scls_prefix}/share/man/man3/MPI_Isendrecv.3
%{scls_prefix}/share/man/man3/MPI_Isendrecv_replace.3
%{scls_prefix}/share/man/man3/MPI_Issend.3
%{scls_prefix}/share/man/man3/MPI_Keyval_create.3
%{scls_prefix}/share/man/man3/MPI_Keyval_free.3
%{scls_prefix}/share/man/man3/MPI_Lookup_name.3
%{scls_prefix}/share/man/man3/MPI_Message_c2f.3
%{scls_prefix}/share/man/man3/MPI_Message_f2c.3
%{scls_prefix}/share/man/man3/MPI_Mprobe.3
%{scls_prefix}/share/man/man3/MPI_Mrecv.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_allgather.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_allgather_init.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_allgatherv.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_allgatherv_init.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_alltoall.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_alltoall_init.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_alltoallv.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_alltoallv_init.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_alltoallw.3
%{scls_prefix}/share/man/man3/MPI_Neighbor_alltoallw_init.3
%{scls_prefix}/share/man/man3/MPI_Op_c2f.3
%{scls_prefix}/share/man/man3/MPI_Op_commutative.3
%{scls_prefix}/share/man/man3/MPI_Op_create.3
%{scls_prefix}/share/man/man3/MPI_Op_f2c.3
%{scls_prefix}/share/man/man3/MPI_Op_free.3
%{scls_prefix}/share/man/man3/MPI_Open_port.3
%{scls_prefix}/share/man/man3/MPI_Pack.3
%{scls_prefix}/share/man/man3/MPI_Pack_external.3
%{scls_prefix}/share/man/man3/MPI_Pack_external_size.3
%{scls_prefix}/share/man/man3/MPI_Pack_size.3
%{scls_prefix}/share/man/man3/MPI_Parrived.3
%{scls_prefix}/share/man/man3/MPI_Pcontrol.3
%{scls_prefix}/share/man/man3/MPI_Pready.3
%{scls_prefix}/share/man/man3/MPI_Pready_list.3
%{scls_prefix}/share/man/man3/MPI_Pready_range.3
%{scls_prefix}/share/man/man3/MPI_Precv_init.3
%{scls_prefix}/share/man/man3/MPI_Probe.3
%{scls_prefix}/share/man/man3/MPI_Psend_init.3
%{scls_prefix}/share/man/man3/MPI_Publish_name.3
%{scls_prefix}/share/man/man3/MPI_Put.3
%{scls_prefix}/share/man/man3/MPI_Query_thread.3
%{scls_prefix}/share/man/man3/MPI_Raccumulate.3
%{scls_prefix}/share/man/man3/MPI_Recv.3
%{scls_prefix}/share/man/man3/MPI_Recv_init.3
%{scls_prefix}/share/man/man3/MPI_Reduce.3
%{scls_prefix}/share/man/man3/MPI_Reduce_init.3
%{scls_prefix}/share/man/man3/MPI_Reduce_local.3
%{scls_prefix}/share/man/man3/MPI_Reduce_scatter.3
%{scls_prefix}/share/man/man3/MPI_Reduce_scatter_block.3
%{scls_prefix}/share/man/man3/MPI_Reduce_scatter_block_init.3
%{scls_prefix}/share/man/man3/MPI_Reduce_scatter_init.3
%{scls_prefix}/share/man/man3/MPI_Register_datarep.3
%{scls_prefix}/share/man/man3/MPI_Request_c2f.3
%{scls_prefix}/share/man/man3/MPI_Request_f2c.3
%{scls_prefix}/share/man/man3/MPI_Request_free.3
%{scls_prefix}/share/man/man3/MPI_Request_get_status.3
%{scls_prefix}/share/man/man3/MPI_Rget.3
%{scls_prefix}/share/man/man3/MPI_Rget_accumulate.3
%{scls_prefix}/share/man/man3/MPI_Rput.3
%{scls_prefix}/share/man/man3/MPI_Rsend.3
%{scls_prefix}/share/man/man3/MPI_Rsend_init.3
%{scls_prefix}/share/man/man3/MPI_Scan.3
%{scls_prefix}/share/man/man3/MPI_Scan_init.3
%{scls_prefix}/share/man/man3/MPI_Scatter.3
%{scls_prefix}/share/man/man3/MPI_Scatter_init.3
%{scls_prefix}/share/man/man3/MPI_Scatterv.3
%{scls_prefix}/share/man/man3/MPI_Scatterv_init.3
%{scls_prefix}/share/man/man3/MPI_Send.3
%{scls_prefix}/share/man/man3/MPI_Send_init.3
%{scls_prefix}/share/man/man3/MPI_Sendrecv.3
%{scls_prefix}/share/man/man3/MPI_Sendrecv_replace.3
%{scls_prefix}/share/man/man3/MPI_Session_create_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Session_f2c.3
%{scls_prefix}/share/man/man3/MPI_Session_finalize.3
%{scls_prefix}/share/man/man3/MPI_Session_get_info.3
%{scls_prefix}/share/man/man3/MPI_Session_get_nth_pset.3
%{scls_prefix}/share/man/man3/MPI_Session_get_num_psets.3
%{scls_prefix}/share/man/man3/MPI_Session_get_pset_info.3
%{scls_prefix}/share/man/man3/MPI_Session_init.3
%{scls_prefix}/share/man/man3/MPI_Sizeof.3
%{scls_prefix}/share/man/man3/MPI_Ssend.3
%{scls_prefix}/share/man/man3/MPI_Ssend_init.3
%{scls_prefix}/share/man/man3/MPI_Start.3
%{scls_prefix}/share/man/man3/MPI_Startall.3
%{scls_prefix}/share/man/man3/MPI_Status_c2f.3
%{scls_prefix}/share/man/man3/MPI_Status_c2f08.3
%{scls_prefix}/share/man/man3/MPI_Status_f082c.3
%{scls_prefix}/share/man/man3/MPI_Status_f082f.3
%{scls_prefix}/share/man/man3/MPI_Status_f2c.3
%{scls_prefix}/share/man/man3/MPI_Status_f2f08.3
%{scls_prefix}/share/man/man3/MPI_Status_set_cancelled.3
%{scls_prefix}/share/man/man3/MPI_Status_set_elements.3
%{scls_prefix}/share/man/man3/MPI_Status_set_elements_x.3
%{scls_prefix}/share/man/man3/MPI_T.3
%{scls_prefix}/share/man/man3/MPI_T_category_changed.3
%{scls_prefix}/share/man/man3/MPI_T_category_get_categories.3
%{scls_prefix}/share/man/man3/MPI_T_category_get_cvars.3
%{scls_prefix}/share/man/man3/MPI_T_category_get_info.3
%{scls_prefix}/share/man/man3/MPI_T_category_get_num.3
%{scls_prefix}/share/man/man3/MPI_T_category_get_pvars.3
%{scls_prefix}/share/man/man3/MPI_T_cvar_get_info.3
%{scls_prefix}/share/man/man3/MPI_T_cvar_get_num.3
%{scls_prefix}/share/man/man3/MPI_T_cvar_handle_alloc.3
%{scls_prefix}/share/man/man3/MPI_T_cvar_handle_free.3
%{scls_prefix}/share/man/man3/MPI_T_cvar_read.3
%{scls_prefix}/share/man/man3/MPI_T_cvar_write.3
%{scls_prefix}/share/man/man3/MPI_T_enum_get_info.3
%{scls_prefix}/share/man/man3/MPI_T_enum_get_item.3
%{scls_prefix}/share/man/man3/MPI_T_finalize.3
%{scls_prefix}/share/man/man3/MPI_T_init_thread.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_get_info.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_get_num.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_handle_alloc.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_handle_free.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_read.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_readreset.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_reset.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_session_create.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_session_free.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_start.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_stop.3
%{scls_prefix}/share/man/man3/MPI_T_pvar_write.3
%{scls_prefix}/share/man/man3/MPI_Test.3
%{scls_prefix}/share/man/man3/MPI_Test_cancelled.3
%{scls_prefix}/share/man/man3/MPI_Testall.3
%{scls_prefix}/share/man/man3/MPI_Testany.3
%{scls_prefix}/share/man/man3/MPI_Testsome.3
%{scls_prefix}/share/man/man3/MPI_Topo_test.3
%{scls_prefix}/share/man/man3/MPI_Type_c2f.3
%{scls_prefix}/share/man/man3/MPI_Type_commit.3
%{scls_prefix}/share/man/man3/MPI_Type_contiguous.3
%{scls_prefix}/share/man/man3/MPI_Type_create_darray.3
%{scls_prefix}/share/man/man3/MPI_Type_create_f90_complex.3
%{scls_prefix}/share/man/man3/MPI_Type_create_f90_integer.3
%{scls_prefix}/share/man/man3/MPI_Type_create_f90_real.3
%{scls_prefix}/share/man/man3/MPI_Type_create_hindexed.3
%{scls_prefix}/share/man/man3/MPI_Type_create_hindexed_block.3
%{scls_prefix}/share/man/man3/MPI_Type_create_hvector.3
%{scls_prefix}/share/man/man3/MPI_Type_create_indexed_block.3
%{scls_prefix}/share/man/man3/MPI_Type_create_keyval.3
%{scls_prefix}/share/man/man3/MPI_Type_create_resized.3
%{scls_prefix}/share/man/man3/MPI_Type_create_struct.3
%{scls_prefix}/share/man/man3/MPI_Type_create_subarray.3
%{scls_prefix}/share/man/man3/MPI_Type_delete_attr.3
%{scls_prefix}/share/man/man3/MPI_Type_dup.3
%{scls_prefix}/share/man/man3/MPI_Type_extent.3
%{scls_prefix}/share/man/man3/MPI_Type_f2c.3
%{scls_prefix}/share/man/man3/MPI_Type_free.3
%{scls_prefix}/share/man/man3/MPI_Type_free_keyval.3
%{scls_prefix}/share/man/man3/MPI_Type_get_attr.3
%{scls_prefix}/share/man/man3/MPI_Type_get_contents.3
%{scls_prefix}/share/man/man3/MPI_Type_get_envelope.3
%{scls_prefix}/share/man/man3/MPI_Type_get_extent.3
%{scls_prefix}/share/man/man3/MPI_Type_get_extent_x.3
%{scls_prefix}/share/man/man3/MPI_Type_get_name.3
%{scls_prefix}/share/man/man3/MPI_Type_get_true_extent.3
%{scls_prefix}/share/man/man3/MPI_Type_get_true_extent_x.3
%{scls_prefix}/share/man/man3/MPI_Type_hindexed.3
%{scls_prefix}/share/man/man3/MPI_Type_hvector.3
%{scls_prefix}/share/man/man3/MPI_Type_indexed.3
%{scls_prefix}/share/man/man3/MPI_Type_lb.3
%{scls_prefix}/share/man/man3/MPI_Type_match_size.3
%{scls_prefix}/share/man/man3/MPI_Type_set_attr.3
%{scls_prefix}/share/man/man3/MPI_Type_set_name.3
%{scls_prefix}/share/man/man3/MPI_Type_size.3
%{scls_prefix}/share/man/man3/MPI_Type_size_x.3
%{scls_prefix}/share/man/man3/MPI_Type_struct.3
%{scls_prefix}/share/man/man3/MPI_Type_ub.3
%{scls_prefix}/share/man/man3/MPI_Type_vector.3
%{scls_prefix}/share/man/man3/MPI_Unpack.3
%{scls_prefix}/share/man/man3/MPI_Unpack_external.3
%{scls_prefix}/share/man/man3/MPI_Unpublish_name.3
%{scls_prefix}/share/man/man3/MPI_Wait.3
%{scls_prefix}/share/man/man3/MPI_Waitall.3
%{scls_prefix}/share/man/man3/MPI_Waitany.3
%{scls_prefix}/share/man/man3/MPI_Waitsome.3
%{scls_prefix}/share/man/man3/MPI_Win_allocate.3
%{scls_prefix}/share/man/man3/MPI_Win_allocate_shared.3
%{scls_prefix}/share/man/man3/MPI_Win_attach.3
%{scls_prefix}/share/man/man3/MPI_Win_c2f.3
%{scls_prefix}/share/man/man3/MPI_Win_call_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Win_complete.3
%{scls_prefix}/share/man/man3/MPI_Win_create.3
%{scls_prefix}/share/man/man3/MPI_Win_create_dynamic.3
%{scls_prefix}/share/man/man3/MPI_Win_create_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Win_create_keyval.3
%{scls_prefix}/share/man/man3/MPI_Win_delete_attr.3
%{scls_prefix}/share/man/man3/MPI_Win_detach.3
%{scls_prefix}/share/man/man3/MPI_Win_f2c.3
%{scls_prefix}/share/man/man3/MPI_Win_fence.3
%{scls_prefix}/share/man/man3/MPI_Win_flush.3
%{scls_prefix}/share/man/man3/MPI_Win_flush_all.3
%{scls_prefix}/share/man/man3/MPI_Win_flush_local.3
%{scls_prefix}/share/man/man3/MPI_Win_flush_local_all.3
%{scls_prefix}/share/man/man3/MPI_Win_free.3
%{scls_prefix}/share/man/man3/MPI_Win_free_keyval.3
%{scls_prefix}/share/man/man3/MPI_Win_get_attr.3
%{scls_prefix}/share/man/man3/MPI_Win_get_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Win_get_group.3
%{scls_prefix}/share/man/man3/MPI_Win_get_info.3
%{scls_prefix}/share/man/man3/MPI_Win_get_name.3
%{scls_prefix}/share/man/man3/MPI_Win_lock.3
%{scls_prefix}/share/man/man3/MPI_Win_lock_all.3
%{scls_prefix}/share/man/man3/MPI_Win_post.3
%{scls_prefix}/share/man/man3/MPI_Win_set_attr.3
%{scls_prefix}/share/man/man3/MPI_Win_set_errhandler.3
%{scls_prefix}/share/man/man3/MPI_Win_set_info.3
%{scls_prefix}/share/man/man3/MPI_Win_set_name.3
%{scls_prefix}/share/man/man3/MPI_Win_shared_query.3
%{scls_prefix}/share/man/man3/MPI_Win_start.3
%{scls_prefix}/share/man/man3/MPI_Win_sync.3
%{scls_prefix}/share/man/man3/MPI_Win_test.3
%{scls_prefix}/share/man/man3/MPI_Win_unlock.3
%{scls_prefix}/share/man/man3/MPI_Win_unlock_all.3
%{scls_prefix}/share/man/man3/MPI_Win_wait.3
%{scls_prefix}/share/man/man3/MPI_Wtick.3
%{scls_prefix}/share/man/man3/MPI_Wtime.3
%{scls_prefix}/share/man/man3/OMPI_Affinity_str.3
%{scls_prefix}/share/man/man3/PMIx_Abort.3
%{scls_prefix}/share/man/man3/PMIx_Finalize.3
%{scls_prefix}/share/man/man3/PMIx_Init.3
%{scls_prefix}/share/man/man5/openpmix.5
%{scls_prefix}/share/man/man5/prte.5
%{scls_prefix}/share/man/man7/Open-MPI.7

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 5.0.1-1
- Initial Package

