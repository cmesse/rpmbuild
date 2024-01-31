#######################################################################
# FLAVOR SPECIFIC DEFINES                                             #
#######################################################################

%define tpls_flavor skylake-gnu-openmpi-cuda-shared-32 

%define tpls_host skylake 
%define tpls_compiler gnu 
%define tpls_mpi openmpi 
%define tpls_gpu cuda 
%define tpls_libs shared 
%define tpls_int 32 
%define tpls_comp_minver 11.4.1 

%define tpls_rpm_cc gcc 
%define tpls_rpm_cxx gcc-c++ 
%define tpls_rpm_fc gfortran 
%define tpls_auto_req_prov yes

# important paths
%define tpls_prefix /opt/tpls/skylake-gnu-openmpi-cuda-shared-32 
%define tpls_includes /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/includes 
%define tpls_libdir /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/lib 
%define tpls_comproot /usr 
%define tpls_mklroot  /opt/intel/oneapi/mkl/latest 
%define tpls_cuda  /opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda 
%define tpls_rocm  /opt/rocm 
%define tpls_ld_library_path  /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/lib:/opt/intel/oneapi/mkl/latest/lib:/opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda/lib64 

# compiler executables
%define tpls_cc gcc 
%define tpls_cxx g++ 
%define tpls_fc gfortran 
%define tpls_ar ar 
%define tpls_ld ld 
%define tpls_cpp ld -E 
%define tpls_cxxcpp ld -E 

# MPI wrappers
%define tpls_mpicc   /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/bin/mpicc
%define tpls_mpicxx  /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/bin/mpicxx 
%define tpls_mpifort /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/bin/mpifort 

# Compiler Flags
%define tpls_cflags   -O2 -m64 -fno-fast-math -fPIC -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-openmpi-cuda-shared-32/include -I/opt/intel/oneapi/mkl/latest/include -I/opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda/include -I/opt/nvidia/hpc_sdk/Linux_x86_64/latest/math_libs/include
%define tpls_cxxflags   -O2 -m64 -fno-fast-math -fPIC -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-openmpi-cuda-shared-32/include -I/opt/intel/oneapi/mkl/latest/include -I/opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda/include -I/opt/nvidia/hpc_sdk/Linux_x86_64/latest/math_libs/include
%define tpls_fcflags   -O2 -m64 -fno-fast-math -fPIC -mtune=skylake -m64 -I/opt/tpls/skylake-gnu-openmpi-cuda-shared-32/include -I/opt/intel/oneapi/mkl/latest/include -I/opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda/include -I/opt/nvidia/hpc_sdk/Linux_x86_64/latest/math_libs/include
%define tpls_ldflags    -L/opt/tpls/skylake-gnu-openmpi-cuda-shared-32/lib -L/opt/intel/oneapi/mkl/latest/lib -L/opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda/lib64 -L/opt/nvidia/hpc_sdk/Linux_x86_64/latest/math_libs/lib64  -Wl,-rpath,/opt/tpls/skylake-gnu-openmpi-cuda-shared-32/lib -Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib -Wl,-rpath,/opt/nvidia/hpc_sdk/Linux_x86_64/latest/cuda/lib64 -Wl,-rpath,/opt/nvidia/hpc_sdk/Linux_x86_64/latest/math_libs/lib64
%define tpls_arflags   -cru
%define tpls_ompflag    -fopenmp

# the netlib reference implementations
%define tpls_blas   /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/libblas.so
%define tpls_lapack  /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/liblapack.so
%define tpls_scalapack /opt/tpls/skylake-gnu-openmpi-cuda-shared-32/libscalapack.so

# the MKL setup
%define tpls_mkl_linker_flags   -lmkl_intel_lp64 -lmkl_gnu_thread -lmkl_core  -lgomp  -lpthread -lm -ldl
%define tpls_mkl_mpi_linker_flags  -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_gnu_thread -lmkl_core -lmkl_blacs_openmpi_lp64  -lgomp -lpthread -lm -ldl

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
Name:           tpls-%{tpls_flavor}-openmpi
Version:        5.0.1
Release:        1%{?dist}
Summary:        A powerful implementation of MPI/SHMEM

License:        BSD
URL:            https://www.open-mpi.org/
Source0:        https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-%{version}.tar.bz2

BuildRequires: make
BuildRequires: tpls-%{tpls_flavor}-libevent

Requires:      %{tpls_rpm_cc}  >= %{tpls_comp_minver}
Requires:      %{tpls_rpm_cxx} >= %{tpls_comp_minver}
Requires:      %{tpls_rpm_fc}  >= %{tpls_comp_minver}
Requires:      tpls-%{tpls_flavor}-libevent
AutoReqProv:   %{tpls_auto_req_prov}

BuildRequires: tpls-%{tpls_flavor}-hwloc
Requires:      tpls-%{tpls_flavor}-hwloc

BuildRequires: libpciaccess-devel
Requires: libpciaccess-devel
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
Requires:      tpls-%{tpls_flavor}-openmpi == %{version} 

%description doc
Documentation files for OpenMPI

%prep
%setup -q -n openmpi-%{version}

%build

%{setup_tpls_env}
CC=%{tpls_cc} CXX=%{tpls_cxx} FC=%{tpls_fc} \
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
   CC=%{tpls_cc} \
   CXX=%{tpls_cxx}  \
   FC=%{tpls_fc} \
   F77=%{tpls_fc} \
   --enable-mpi-fortran \
   --with-hwloc=%{tpls_prefix} \
   --with-hwloc-libdir=%{tpls_prefix}/lib \
%if "%{tpls_libs}" == "static"
   --enable-static \
   --disable-shared \
%else
   --disable-static \
   --enable-shared \
%endif
%if "%{tpls_gpu}" == "cuda"
   --enable-mpi-ext=cuda \
   --with-cuda=%{tpls_cuda} \
   --with-cuda-libdir=%{tpls_cuda}/lib64 \
%endif
%if "%{tpls_gpu}" == "rocm"
   --enable-mpi-ext=rocm \
   --with-rocm=%{tpls_rocm} \
%endif
   --enable-mpi1-compatibility \
   --with-libevent-libdir=%{tpls_prefix} \
   --disable-dlopen

%make_build

%check
make %{?_smp_mflags} test

%install
%make_install
%{tpls_remove_la_files}


%files
%{tpls_prefix}/bin/mpiCC
%{tpls_prefix}/bin/mpic++
%{tpls_prefix}/bin/mpicc
%{tpls_prefix}/bin/mpicxx
%{tpls_prefix}/bin/mpiexec
%{tpls_prefix}/bin/mpif77
%{tpls_prefix}/bin/mpif90
%{tpls_prefix}/bin/mpifort
%{tpls_prefix}/bin/mpirun
%{tpls_prefix}/bin/ompi_info
%{tpls_prefix}/bin/opal_wrapper
%{tpls_prefix}/bin/oshrun
%{tpls_prefix}/bin/pattrs
%{tpls_prefix}/bin/pctrl
%{tpls_prefix}/bin/pevent
%{tpls_prefix}/bin/plookup
%{tpls_prefix}/bin/pmix_info
%{tpls_prefix}/bin/pmixcc
%{tpls_prefix}/bin/pps
%{tpls_prefix}/bin/pquery
%{tpls_prefix}/bin/prte
%{tpls_prefix}/bin/prte_info
%{tpls_prefix}/bin/prted
%{tpls_prefix}/bin/prterun
%{tpls_prefix}/bin/prun
%{tpls_prefix}/bin/pterm
%{tpls_prefix}/etc/openmpi-mca-params.conf
%{tpls_prefix}/etc/openmpi-totalview.tcl
%{tpls_prefix}/etc/pmix-mca-params.conf
%{tpls_prefix}/etc/prte-default-hostfile
%{tpls_prefix}/etc/prte-mca-params.conf
%{tpls_prefix}/etc/prte.conf
%{tpls_prefix}/include/mpi-ext.h
%{tpls_prefix}/include/mpi.h
%{tpls_prefix}/include/mpi_portable_platform.h
%{tpls_prefix}/include/mpif-c-constants-decl.h
%{tpls_prefix}/include/mpif-config.h
%{tpls_prefix}/include/mpif-constants.h
%{tpls_prefix}/include/mpif-ext.h
%{tpls_prefix}/include/mpif-externals.h
%{tpls_prefix}/include/mpif-handles.h
%{tpls_prefix}/include/mpif-io-constants.h
%{tpls_prefix}/include/mpif-io-handles.h
%{tpls_prefix}/include/mpif-sentinels.h
%{tpls_prefix}/include/mpif-sizeof.h
%{tpls_prefix}/include/mpif.h
%{tpls_prefix}/include/openmpi/mpiext/*.h
%{tpls_prefix}/include/pmix.h
%{tpls_prefix}/include/pmix/src/class/*.h
%{tpls_prefix}/include/pmix/src/client/pmix_client_ops.h
%{tpls_prefix}/include/pmix/src/common/pmix_attributes.h
%{tpls_prefix}/include/pmix/src/common/pmix_iof.h
%{tpls_prefix}/include/pmix/src/event/pmix_event.h
%{tpls_prefix}/include/pmix/src/hwloc/pmix_hwloc.h
%{tpls_prefix}/include/pmix/src/include/*.h
%{tpls_prefix}/include/pmix/src/mca/base/*.h
%{tpls_prefix}/include/pmix/src/mca/bfrops/base/base.h
%{tpls_prefix}/include/pmix/src/mca/bfrops/bfrops.h
%{tpls_prefix}/include/pmix/src/mca/bfrops/bfrops_types.h
%{tpls_prefix}/include/pmix/src/mca/common/dstore/dstore_base.h
%{tpls_prefix}/include/pmix/src/mca/common/dstore/dstore_common.h
%{tpls_prefix}/include/pmix/src/mca/common/dstore/dstore_file.h
%{tpls_prefix}/include/pmix/src/mca/common/dstore/dstore_segment.h
%{tpls_prefix}/include/pmix/src/mca/gds/base/base.h
%{tpls_prefix}/include/pmix/src/mca/gds/gds.h
%{tpls_prefix}/include/pmix/src/mca/mca.h
%{tpls_prefix}/include/pmix/src/mca/pcompress/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pcompress/pcompress.h
%{tpls_prefix}/include/pmix/src/mca/pdl/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pdl/pdl.h
%{tpls_prefix}/include/pmix/src/mca/pfexec/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pfexec/pfexec.h
%{tpls_prefix}/include/pmix/src/mca/pgpu/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pgpu/pgpu.h
%{tpls_prefix}/include/pmix/src/mca/pif/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pif/pif.h
%{tpls_prefix}/include/pmix/src/mca/pinstalldirs/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pinstalldirs/pinstalldirs.h
%{tpls_prefix}/include/pmix/src/mca/pinstalldirs/pinstalldirs_types.h
%{tpls_prefix}/include/pmix/src/mca/plog/base/base.h
%{tpls_prefix}/include/pmix/src/mca/plog/plog.h
%{tpls_prefix}/include/pmix/src/mca/pmdl/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pmdl/pmdl.h
%{tpls_prefix}/include/pmix/src/mca/pnet/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pnet/pnet.h
%{tpls_prefix}/include/pmix/src/mca/preg/base/base.h
%{tpls_prefix}/include/pmix/src/mca/preg/preg.h
%{tpls_prefix}/include/pmix/src/mca/preg/preg_types.h
%{tpls_prefix}/include/pmix/src/mca/prm/base/base.h
%{tpls_prefix}/include/pmix/src/mca/prm/prm.h
%{tpls_prefix}/include/pmix/src/mca/psec/base/base.h
%{tpls_prefix}/include/pmix/src/mca/psec/psec.h
%{tpls_prefix}/include/pmix/src/mca/psensor/base/base.h
%{tpls_prefix}/include/pmix/src/mca/psensor/psensor.h
%{tpls_prefix}/include/pmix/src/mca/pshmem/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pshmem/pshmem.h
%{tpls_prefix}/include/pmix/src/mca/psquash/base/base.h
%{tpls_prefix}/include/pmix/src/mca/psquash/psquash.h
%{tpls_prefix}/include/pmix/src/mca/pstat/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pstat/pstat.h
%{tpls_prefix}/include/pmix/src/mca/pstrg/base/base.h
%{tpls_prefix}/include/pmix/src/mca/pstrg/pstrg.h
%{tpls_prefix}/include/pmix/src/mca/ptl/base/base.h
%{tpls_prefix}/include/pmix/src/mca/ptl/base/ptl_base_handshake.h
%{tpls_prefix}/include/pmix/src/mca/ptl/ptl.h
%{tpls_prefix}/include/pmix/src/mca/ptl/ptl_types.h
%{tpls_prefix}/include/pmix/src/runtime/pmix_init_util.h
%{tpls_prefix}/include/pmix/src/runtime/pmix_progress_threads.h
%{tpls_prefix}/include/pmix/src/runtime/pmix_rte.h
%{tpls_prefix}/include/pmix/src/server/pmix_server_ops.h
%{tpls_prefix}/include/pmix/src/threads/pmix_mutex.h
%{tpls_prefix}/include/pmix/src/threads/pmix_mutex_unix.h
%{tpls_prefix}/include/pmix/src/threads/pmix_threads.h
%{tpls_prefix}/include/pmix/src/threads/pmix_tsd.h
%{tpls_prefix}/include/pmix/src/tool/pmix_tool_ops.h
%{tpls_prefix}/include/pmix/src/util/pmix*.h
%{tpls_prefix}/include/pmix_common.h
%{tpls_prefix}/include/pmix_deprecated.h
%{tpls_prefix}/include/pmix_server.h
%{tpls_prefix}/include/pmix_tool.h
%{tpls_prefix}/include/pmix_version.h
%{tpls_prefix}/include/prte.h
%{tpls_prefix}/include/prte/src/mca/errmgr/base/base.h
%{tpls_prefix}/include/prte/src/mca/errmgr/base/errmgr_private.h
%{tpls_prefix}/include/prte/src/mca/errmgr/errmgr.h
%{tpls_prefix}/include/prte/src/mca/ess/base/base.h
%{tpls_prefix}/include/prte/src/mca/ess/ess.h
%{tpls_prefix}/include/prte/src/mca/filem/base/base.h
%{tpls_prefix}/include/prte/src/mca/filem/filem.h
%{tpls_prefix}/include/prte/src/mca/grpcomm/base/base.h
%{tpls_prefix}/include/prte/src/mca/grpcomm/grpcomm.h
%{tpls_prefix}/include/prte/src/mca/iof/base/base.h
%{tpls_prefix}/include/prte/src/mca/iof/base/iof_base_setup.h
%{tpls_prefix}/include/prte/src/mca/iof/iof.h
%{tpls_prefix}/include/prte/src/mca/iof/iof_types.h
%{tpls_prefix}/include/prte/src/mca/odls/base/base.h
%{tpls_prefix}/include/prte/src/mca/odls/odls.h
%{tpls_prefix}/include/prte/src/mca/odls/odls_types.h
%{tpls_prefix}/include/prte/src/mca/oob/base/base.h
%{tpls_prefix}/include/prte/src/mca/oob/oob.h
%{tpls_prefix}/include/prte/src/mca/plm/base/base.h
%{tpls_prefix}/include/prte/src/mca/plm/base/plm_private.h
%{tpls_prefix}/include/prte/src/mca/plm/plm.h
%{tpls_prefix}/include/prte/src/mca/plm/plm_types.h
%{tpls_prefix}/include/prte/src/mca/prtebacktrace/base/base.h
%{tpls_prefix}/include/prte/src/mca/prtebacktrace/prtebacktrace.h
%{tpls_prefix}/include/prte/src/mca/prtedl/base/base.h
%{tpls_prefix}/include/prte/src/mca/prtedl/prtedl.h
%{tpls_prefix}/include/prte/src/mca/prteinstalldirs/base/base.h
%{tpls_prefix}/include/prte/src/mca/prteinstalldirs/prteinstalldirs.h
%{tpls_prefix}/include/prte/src/mca/prtereachable/base/base.h
%{tpls_prefix}/include/prte/src/mca/prtereachable/prtereachable.h
%{tpls_prefix}/include/prte/src/mca/ras/base/base.h
%{tpls_prefix}/include/prte/src/mca/ras/base/ras_private.h
%{tpls_prefix}/include/prte/src/mca/ras/ras.h
%{tpls_prefix}/include/prte/src/mca/rmaps/base/base.h
%{tpls_prefix}/include/prte/src/mca/rmaps/base/rmaps_private.h
%{tpls_prefix}/include/prte/src/mca/rmaps/rmaps.h
%{tpls_prefix}/include/prte/src/mca/rmaps/rmaps_types.h
%{tpls_prefix}/include/prte/src/mca/rtc/base/base.h
%{tpls_prefix}/include/prte/src/mca/rtc/rtc.h
%{tpls_prefix}/include/prte/src/mca/schizo/base/base.h
%{tpls_prefix}/include/prte/src/mca/schizo/schizo.h
%{tpls_prefix}/include/prte/src/mca/state/base/base.h
%{tpls_prefix}/include/prte/src/mca/state/state.h
%{tpls_prefix}/include/prte/src/mca/state/state_types.h
%{tpls_prefix}/include/prte_version.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libmpi.a
%{tpls_prefix}/lib/libmpi_mpifh.a
%{tpls_prefix}/lib/libmpi_usempi_ignore_tkr.a
%{tpls_prefix}/lib/libmpi_usempif08.a
%{tpls_prefix}/lib/libopen-pal.a
#%{tpls_prefix}/lib/libpmix.a
%{tpls_prefix}/lib/libprrte.a
%{tpls_prefix}/lib/openmpi/libompi_dbg_msgq.a
%else
%{tpls_prefix}/lib/libmpi.so
%{tpls_prefix}/lib/libmpi.so.*
%{tpls_prefix}/lib/libmpi_mpifh.so
%{tpls_prefix}/lib/libmpi_mpifh.so.*
%{tpls_prefix}/lib/libmpi_usempi_ignore_tkr.so
%{tpls_prefix}/lib/libmpi_usempi_ignore_tkr.so.*
%{tpls_prefix}/lib/libmpi_usempif08.so
%{tpls_prefix}/lib/libmpi_usempif08.so.*
%{tpls_prefix}/lib/libopen-pal.so
%{tpls_prefix}/lib/libopen-pal.so.*
%{tpls_prefix}/lib/libpmix.so
%{tpls_prefix}/lib/libpmix.so.*
%{tpls_prefix}/lib/libprrte.so
%{tpls_prefix}/lib/libprrte.so.*
%{tpls_prefix}/lib/openmpi/libompi_dbg_msgq.so
#%{tpls_prefix}/lib/pmix/pmix_mca_pcompress_zlib.so
#%{tpls_prefix}/lib/pmix/pmix_mca_prm_default.so
#%{tpls_prefix}/lib/pmix/pmix_mca_prm_slurm.so
%endif
%{tpls_prefix}/lib/mpi.mod
%{tpls_prefix}/lib/mpi_ext.mod
%{tpls_prefix}/lib/mpi_f08.mod
%{tpls_prefix}/lib/mpi_f08_callbacks.mod
%{tpls_prefix}/lib/mpi_f08_ext.mod
%{tpls_prefix}/lib/mpi_f08_interfaces.mod
%{tpls_prefix}/lib/mpi_f08_interfaces_callbacks.mod
%{tpls_prefix}/lib/mpi_f08_types.mod
%{tpls_prefix}/lib/mpi_types.mod
%{tpls_prefix}/lib/pkgconfig/ompi-c.pc
%{tpls_prefix}/lib/pkgconfig/ompi-cxx.pc
%{tpls_prefix}/lib/pkgconfig/ompi-f77.pc
%{tpls_prefix}/lib/pkgconfig/ompi-f90.pc
%{tpls_prefix}/lib/pkgconfig/ompi-fort.pc
%{tpls_prefix}/lib/pkgconfig/ompi.pc
%{tpls_prefix}/lib/pkgconfig/pmix.pc
%{tpls_prefix}/lib/pmpi_f08_interfaces.mod
%{tpls_prefix}/share/openmpi/amca-param-sets/example.conf
%{tpls_prefix}/share/openmpi/amca-param-sets/ft-mpi
%{tpls_prefix}/share/openmpi/help*.txt
%{tpls_prefix}/share/openmpi/mpi*.txt
%{tpls_prefix}/share/openmpi/openmpi-valgrind.supp
%{tpls_prefix}/share/pmix/help-*.txt
%{tpls_prefix}/share/pmix/pmix-valgrind.supp
%{tpls_prefix}/share/pmix/pmixcc-wrapper-data.txt
%{tpls_prefix}/share/prte/amca-param-sets/example.conf
%{tpls_prefix}/share/prte/help*.txt
%{tpls_prefix}/share/prte/rst/prrte-rst-content/*.rst
%{tpls_prefix}/share/prte/rst/schizo-ompi-rst-content/schizo-ompi-cli.rstxt

%files doc
%{tpls_prefix}/share/doc/openmpi/html
%{tpls_prefix}/share/doc/pmix/html
%{tpls_prefix}/share/doc/prrte/html
%{tpls_prefix}/share/man/man1/mpic++.1
%{tpls_prefix}/share/man/man1/mpicc.1
%{tpls_prefix}/share/man/man1/mpicxx.1
%{tpls_prefix}/share/man/man1/mpif77.1
%{tpls_prefix}/share/man/man1/mpif90.1
%{tpls_prefix}/share/man/man1/mpifort.1
%{tpls_prefix}/share/man/man1/mpirun.1
%{tpls_prefix}/share/man/man1/mpisync.1
%{tpls_prefix}/share/man/man1/ompi-wrapper-compiler.1
%{tpls_prefix}/share/man/man1/ompi_info.1
%{tpls_prefix}/share/man/man1/opal_wrapper.1
%{tpls_prefix}/share/man/man1/pmix_info.1
%{tpls_prefix}/share/man/man1/prte.1
%{tpls_prefix}/share/man/man1/prte_info.1
%{tpls_prefix}/share/man/man1/prted.1
%{tpls_prefix}/share/man/man1/prterun.1
%{tpls_prefix}/share/man/man1/prun.1
%{tpls_prefix}/share/man/man1/pterm.1
%{tpls_prefix}/share/man/man3/MPIX_Comm_ack_failed.3
%{tpls_prefix}/share/man/man3/MPIX_Comm_agree.3
%{tpls_prefix}/share/man/man3/MPIX_Comm_get_failed.3
%{tpls_prefix}/share/man/man3/MPIX_Comm_iagree.3
%{tpls_prefix}/share/man/man3/MPIX_Comm_is_revoked.3
%{tpls_prefix}/share/man/man3/MPIX_Comm_ishrink.3
%{tpls_prefix}/share/man/man3/MPIX_Comm_revoke.3
%{tpls_prefix}/share/man/man3/MPIX_Comm_shrink.3
%{tpls_prefix}/share/man/man3/MPIX_Query_cuda_support.3
%{tpls_prefix}/share/man/man3/MPIX_Query_rocm_support.3
%{tpls_prefix}/share/man/man3/MPI_Abort.3
%{tpls_prefix}/share/man/man3/MPI_Accumulate.3
%{tpls_prefix}/share/man/man3/MPI_Add_error_class.3
%{tpls_prefix}/share/man/man3/MPI_Add_error_code.3
%{tpls_prefix}/share/man/man3/MPI_Add_error_string.3
%{tpls_prefix}/share/man/man3/MPI_Address.3
%{tpls_prefix}/share/man/man3/MPI_Aint_add.3
%{tpls_prefix}/share/man/man3/MPI_Aint_diff.3
%{tpls_prefix}/share/man/man3/MPI_Allgather.3
%{tpls_prefix}/share/man/man3/MPI_Allgather_init.3
%{tpls_prefix}/share/man/man3/MPI_Allgatherv.3
%{tpls_prefix}/share/man/man3/MPI_Allgatherv_init.3
%{tpls_prefix}/share/man/man3/MPI_Alloc_mem.3
%{tpls_prefix}/share/man/man3/MPI_Allreduce.3
%{tpls_prefix}/share/man/man3/MPI_Allreduce_init.3
%{tpls_prefix}/share/man/man3/MPI_Alltoall.3
%{tpls_prefix}/share/man/man3/MPI_Alltoall_init.3
%{tpls_prefix}/share/man/man3/MPI_Alltoallv.3
%{tpls_prefix}/share/man/man3/MPI_Alltoallv_init.3
%{tpls_prefix}/share/man/man3/MPI_Alltoallw.3
%{tpls_prefix}/share/man/man3/MPI_Alltoallw_init.3
%{tpls_prefix}/share/man/man3/MPI_Attr_delete.3
%{tpls_prefix}/share/man/man3/MPI_Attr_get.3
%{tpls_prefix}/share/man/man3/MPI_Attr_put.3
%{tpls_prefix}/share/man/man3/MPI_Barrier.3
%{tpls_prefix}/share/man/man3/MPI_Barrier_init.3
%{tpls_prefix}/share/man/man3/MPI_Bcast.3
%{tpls_prefix}/share/man/man3/MPI_Bcast_init.3
%{tpls_prefix}/share/man/man3/MPI_Bsend.3
%{tpls_prefix}/share/man/man3/MPI_Bsend_init.3
%{tpls_prefix}/share/man/man3/MPI_Buffer_attach.3
%{tpls_prefix}/share/man/man3/MPI_Buffer_detach.3
%{tpls_prefix}/share/man/man3/MPI_Cancel.3
%{tpls_prefix}/share/man/man3/MPI_Cart_coords.3
%{tpls_prefix}/share/man/man3/MPI_Cart_create.3
%{tpls_prefix}/share/man/man3/MPI_Cart_get.3
%{tpls_prefix}/share/man/man3/MPI_Cart_map.3
%{tpls_prefix}/share/man/man3/MPI_Cart_rank.3
%{tpls_prefix}/share/man/man3/MPI_Cart_shift.3
%{tpls_prefix}/share/man/man3/MPI_Cart_sub.3
%{tpls_prefix}/share/man/man3/MPI_Cartdim_get.3
%{tpls_prefix}/share/man/man3/MPI_Close_port.3
%{tpls_prefix}/share/man/man3/MPI_Comm_accept.3
%{tpls_prefix}/share/man/man3/MPI_Comm_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Comm_call_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Comm_compare.3
%{tpls_prefix}/share/man/man3/MPI_Comm_connect.3
%{tpls_prefix}/share/man/man3/MPI_Comm_create.3
%{tpls_prefix}/share/man/man3/MPI_Comm_create_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Comm_create_from_group.3
%{tpls_prefix}/share/man/man3/MPI_Comm_create_group.3
%{tpls_prefix}/share/man/man3/MPI_Comm_create_keyval.3
%{tpls_prefix}/share/man/man3/MPI_Comm_delete_attr.3
%{tpls_prefix}/share/man/man3/MPI_Comm_disconnect.3
%{tpls_prefix}/share/man/man3/MPI_Comm_dup.3
%{tpls_prefix}/share/man/man3/MPI_Comm_dup_with_info.3
%{tpls_prefix}/share/man/man3/MPI_Comm_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Comm_free.3
%{tpls_prefix}/share/man/man3/MPI_Comm_free_keyval.3
%{tpls_prefix}/share/man/man3/MPI_Comm_get_attr.3
%{tpls_prefix}/share/man/man3/MPI_Comm_get_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Comm_get_info.3
%{tpls_prefix}/share/man/man3/MPI_Comm_get_name.3
%{tpls_prefix}/share/man/man3/MPI_Comm_get_parent.3
%{tpls_prefix}/share/man/man3/MPI_Comm_group.3
%{tpls_prefix}/share/man/man3/MPI_Comm_idup.3
%{tpls_prefix}/share/man/man3/MPI_Comm_idup_with_info.3
%{tpls_prefix}/share/man/man3/MPI_Comm_join.3
%{tpls_prefix}/share/man/man3/MPI_Comm_rank.3
%{tpls_prefix}/share/man/man3/MPI_Comm_remote_group.3
%{tpls_prefix}/share/man/man3/MPI_Comm_remote_size.3
%{tpls_prefix}/share/man/man3/MPI_Comm_set_attr.3
%{tpls_prefix}/share/man/man3/MPI_Comm_set_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Comm_set_info.3
%{tpls_prefix}/share/man/man3/MPI_Comm_set_name.3
%{tpls_prefix}/share/man/man3/MPI_Comm_size.3
%{tpls_prefix}/share/man/man3/MPI_Comm_spawn.3
%{tpls_prefix}/share/man/man3/MPI_Comm_spawn_multiple.3
%{tpls_prefix}/share/man/man3/MPI_Comm_split.3
%{tpls_prefix}/share/man/man3/MPI_Comm_split_type.3
%{tpls_prefix}/share/man/man3/MPI_Comm_test_inter.3
%{tpls_prefix}/share/man/man3/MPI_Compare_and_swap.3
%{tpls_prefix}/share/man/man3/MPI_Dims_create.3
%{tpls_prefix}/share/man/man3/MPI_Dist_graph_create.3
%{tpls_prefix}/share/man/man3/MPI_Dist_graph_create_adjacent.3
%{tpls_prefix}/share/man/man3/MPI_Dist_graph_neighbors.3
%{tpls_prefix}/share/man/man3/MPI_Dist_graph_neighbors_count.3
%{tpls_prefix}/share/man/man3/MPI_Errhandler_create.3
%{tpls_prefix}/share/man/man3/MPI_Errhandler_free.3
%{tpls_prefix}/share/man/man3/MPI_Errhandler_get.3
%{tpls_prefix}/share/man/man3/MPI_Errhandler_set.3
%{tpls_prefix}/share/man/man3/MPI_Error_class.3
%{tpls_prefix}/share/man/man3/MPI_Error_string.3
%{tpls_prefix}/share/man/man3/MPI_Exscan.3
%{tpls_prefix}/share/man/man3/MPI_Exscan_init.3
%{tpls_prefix}/share/man/man3/MPI_Fetch_and_op.3
%{tpls_prefix}/share/man/man3/MPI_File_c2f.3
%{tpls_prefix}/share/man/man3/MPI_File_call_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_File_close.3
%{tpls_prefix}/share/man/man3/MPI_File_create_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_File_delete.3
%{tpls_prefix}/share/man/man3/MPI_File_f2c.3
%{tpls_prefix}/share/man/man3/MPI_File_get_amode.3
%{tpls_prefix}/share/man/man3/MPI_File_get_atomicity.3
%{tpls_prefix}/share/man/man3/MPI_File_get_byte_offset.3
%{tpls_prefix}/share/man/man3/MPI_File_get_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_File_get_group.3
%{tpls_prefix}/share/man/man3/MPI_File_get_info.3
%{tpls_prefix}/share/man/man3/MPI_File_get_position.3
%{tpls_prefix}/share/man/man3/MPI_File_get_position_shared.3
%{tpls_prefix}/share/man/man3/MPI_File_get_size.3
%{tpls_prefix}/share/man/man3/MPI_File_get_type_extent.3
%{tpls_prefix}/share/man/man3/MPI_File_get_view.3
%{tpls_prefix}/share/man/man3/MPI_File_iread.3
%{tpls_prefix}/share/man/man3/MPI_File_iread_all.3
%{tpls_prefix}/share/man/man3/MPI_File_iread_at.3
%{tpls_prefix}/share/man/man3/MPI_File_iread_at_all.3
%{tpls_prefix}/share/man/man3/MPI_File_iread_shared.3
%{tpls_prefix}/share/man/man3/MPI_File_iwrite.3
%{tpls_prefix}/share/man/man3/MPI_File_iwrite_all.3
%{tpls_prefix}/share/man/man3/MPI_File_iwrite_at.3
%{tpls_prefix}/share/man/man3/MPI_File_iwrite_at_all.3
%{tpls_prefix}/share/man/man3/MPI_File_iwrite_shared.3
%{tpls_prefix}/share/man/man3/MPI_File_open.3
%{tpls_prefix}/share/man/man3/MPI_File_preallocate.3
%{tpls_prefix}/share/man/man3/MPI_File_read.3
%{tpls_prefix}/share/man/man3/MPI_File_read_all.3
%{tpls_prefix}/share/man/man3/MPI_File_read_all_begin.3
%{tpls_prefix}/share/man/man3/MPI_File_read_all_end.3
%{tpls_prefix}/share/man/man3/MPI_File_read_at.3
%{tpls_prefix}/share/man/man3/MPI_File_read_at_all.3
%{tpls_prefix}/share/man/man3/MPI_File_read_at_all_begin.3
%{tpls_prefix}/share/man/man3/MPI_File_read_at_all_end.3
%{tpls_prefix}/share/man/man3/MPI_File_read_ordered.3
%{tpls_prefix}/share/man/man3/MPI_File_read_ordered_begin.3
%{tpls_prefix}/share/man/man3/MPI_File_read_ordered_end.3
%{tpls_prefix}/share/man/man3/MPI_File_read_shared.3
%{tpls_prefix}/share/man/man3/MPI_File_seek.3
%{tpls_prefix}/share/man/man3/MPI_File_seek_shared.3
%{tpls_prefix}/share/man/man3/MPI_File_set_atomicity.3
%{tpls_prefix}/share/man/man3/MPI_File_set_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_File_set_info.3
%{tpls_prefix}/share/man/man3/MPI_File_set_size.3
%{tpls_prefix}/share/man/man3/MPI_File_set_view.3
%{tpls_prefix}/share/man/man3/MPI_File_sync.3
%{tpls_prefix}/share/man/man3/MPI_File_write.3
%{tpls_prefix}/share/man/man3/MPI_File_write_all.3
%{tpls_prefix}/share/man/man3/MPI_File_write_all_begin.3
%{tpls_prefix}/share/man/man3/MPI_File_write_all_end.3
%{tpls_prefix}/share/man/man3/MPI_File_write_at.3
%{tpls_prefix}/share/man/man3/MPI_File_write_at_all.3
%{tpls_prefix}/share/man/man3/MPI_File_write_at_all_begin.3
%{tpls_prefix}/share/man/man3/MPI_File_write_at_all_end.3
%{tpls_prefix}/share/man/man3/MPI_File_write_ordered.3
%{tpls_prefix}/share/man/man3/MPI_File_write_ordered_begin.3
%{tpls_prefix}/share/man/man3/MPI_File_write_ordered_end.3
%{tpls_prefix}/share/man/man3/MPI_File_write_shared.3
%{tpls_prefix}/share/man/man3/MPI_Finalize.3
%{tpls_prefix}/share/man/man3/MPI_Finalized.3
%{tpls_prefix}/share/man/man3/MPI_Free_mem.3
%{tpls_prefix}/share/man/man3/MPI_Gather.3
%{tpls_prefix}/share/man/man3/MPI_Gather_init.3
%{tpls_prefix}/share/man/man3/MPI_Gatherv.3
%{tpls_prefix}/share/man/man3/MPI_Gatherv_init.3
%{tpls_prefix}/share/man/man3/MPI_Get.3
%{tpls_prefix}/share/man/man3/MPI_Get_accumulate.3
%{tpls_prefix}/share/man/man3/MPI_Get_address.3
%{tpls_prefix}/share/man/man3/MPI_Get_count.3
%{tpls_prefix}/share/man/man3/MPI_Get_elements.3
%{tpls_prefix}/share/man/man3/MPI_Get_elements_x.3
%{tpls_prefix}/share/man/man3/MPI_Get_library_version.3
%{tpls_prefix}/share/man/man3/MPI_Get_processor_name.3
%{tpls_prefix}/share/man/man3/MPI_Get_version.3
%{tpls_prefix}/share/man/man3/MPI_Graph_create.3
%{tpls_prefix}/share/man/man3/MPI_Graph_get.3
%{tpls_prefix}/share/man/man3/MPI_Graph_map.3
%{tpls_prefix}/share/man/man3/MPI_Graph_neighbors.3
%{tpls_prefix}/share/man/man3/MPI_Graph_neighbors_count.3
%{tpls_prefix}/share/man/man3/MPI_Graphdims_get.3
%{tpls_prefix}/share/man/man3/MPI_Grequest_complete.3
%{tpls_prefix}/share/man/man3/MPI_Grequest_start.3
%{tpls_prefix}/share/man/man3/MPI_Group_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Group_compare.3
%{tpls_prefix}/share/man/man3/MPI_Group_difference.3
%{tpls_prefix}/share/man/man3/MPI_Group_excl.3
%{tpls_prefix}/share/man/man3/MPI_Group_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Group_free.3
%{tpls_prefix}/share/man/man3/MPI_Group_from_session_pset.3
%{tpls_prefix}/share/man/man3/MPI_Group_incl.3
%{tpls_prefix}/share/man/man3/MPI_Group_intersection.3
%{tpls_prefix}/share/man/man3/MPI_Group_range_excl.3
%{tpls_prefix}/share/man/man3/MPI_Group_range_incl.3
%{tpls_prefix}/share/man/man3/MPI_Group_rank.3
%{tpls_prefix}/share/man/man3/MPI_Group_size.3
%{tpls_prefix}/share/man/man3/MPI_Group_translate_ranks.3
%{tpls_prefix}/share/man/man3/MPI_Group_union.3
%{tpls_prefix}/share/man/man3/MPI_Iallgather.3
%{tpls_prefix}/share/man/man3/MPI_Iallgatherv.3
%{tpls_prefix}/share/man/man3/MPI_Iallreduce.3
%{tpls_prefix}/share/man/man3/MPI_Ialltoall.3
%{tpls_prefix}/share/man/man3/MPI_Ialltoallv.3
%{tpls_prefix}/share/man/man3/MPI_Ialltoallw.3
%{tpls_prefix}/share/man/man3/MPI_Ibarrier.3
%{tpls_prefix}/share/man/man3/MPI_Ibcast.3
%{tpls_prefix}/share/man/man3/MPI_Ibsend.3
%{tpls_prefix}/share/man/man3/MPI_Iexscan.3
%{tpls_prefix}/share/man/man3/MPI_Igather.3
%{tpls_prefix}/share/man/man3/MPI_Igatherv.3
%{tpls_prefix}/share/man/man3/MPI_Improbe.3
%{tpls_prefix}/share/man/man3/MPI_Imrecv.3
%{tpls_prefix}/share/man/man3/MPI_Ineighbor_allgather.3
%{tpls_prefix}/share/man/man3/MPI_Ineighbor_allgatherv.3
%{tpls_prefix}/share/man/man3/MPI_Ineighbor_alltoall.3
%{tpls_prefix}/share/man/man3/MPI_Ineighbor_alltoallv.3
%{tpls_prefix}/share/man/man3/MPI_Ineighbor_alltoallw.3
%{tpls_prefix}/share/man/man3/MPI_Info_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Info_create.3
%{tpls_prefix}/share/man/man3/MPI_Info_delete.3
%{tpls_prefix}/share/man/man3/MPI_Info_dup.3
%{tpls_prefix}/share/man/man3/MPI_Info_env.3
%{tpls_prefix}/share/man/man3/MPI_Info_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Info_free.3
%{tpls_prefix}/share/man/man3/MPI_Info_get.3
%{tpls_prefix}/share/man/man3/MPI_Info_get_nkeys.3
%{tpls_prefix}/share/man/man3/MPI_Info_get_nthkey.3
%{tpls_prefix}/share/man/man3/MPI_Info_get_string.3
%{tpls_prefix}/share/man/man3/MPI_Info_get_valuelen.3
%{tpls_prefix}/share/man/man3/MPI_Info_set.3
%{tpls_prefix}/share/man/man3/MPI_Init.3
%{tpls_prefix}/share/man/man3/MPI_Init_thread.3
%{tpls_prefix}/share/man/man3/MPI_Initialized.3
%{tpls_prefix}/share/man/man3/MPI_Intercomm_create.3
%{tpls_prefix}/share/man/man3/MPI_Intercomm_create_from_groups.3
%{tpls_prefix}/share/man/man3/MPI_Intercomm_merge.3
%{tpls_prefix}/share/man/man3/MPI_Iprobe.3
%{tpls_prefix}/share/man/man3/MPI_Irecv.3
%{tpls_prefix}/share/man/man3/MPI_Ireduce.3
%{tpls_prefix}/share/man/man3/MPI_Ireduce_scatter.3
%{tpls_prefix}/share/man/man3/MPI_Ireduce_scatter_block.3
%{tpls_prefix}/share/man/man3/MPI_Irsend.3
%{tpls_prefix}/share/man/man3/MPI_Is_thread_main.3
%{tpls_prefix}/share/man/man3/MPI_Iscan.3
%{tpls_prefix}/share/man/man3/MPI_Iscatter.3
%{tpls_prefix}/share/man/man3/MPI_Iscatterv.3
%{tpls_prefix}/share/man/man3/MPI_Isend.3
%{tpls_prefix}/share/man/man3/MPI_Isendrecv.3
%{tpls_prefix}/share/man/man3/MPI_Isendrecv_replace.3
%{tpls_prefix}/share/man/man3/MPI_Issend.3
%{tpls_prefix}/share/man/man3/MPI_Keyval_create.3
%{tpls_prefix}/share/man/man3/MPI_Keyval_free.3
%{tpls_prefix}/share/man/man3/MPI_Lookup_name.3
%{tpls_prefix}/share/man/man3/MPI_Message_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Message_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Mprobe.3
%{tpls_prefix}/share/man/man3/MPI_Mrecv.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_allgather.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_allgather_init.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_allgatherv.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_allgatherv_init.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_alltoall.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_alltoall_init.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_alltoallv.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_alltoallv_init.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_alltoallw.3
%{tpls_prefix}/share/man/man3/MPI_Neighbor_alltoallw_init.3
%{tpls_prefix}/share/man/man3/MPI_Op_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Op_commutative.3
%{tpls_prefix}/share/man/man3/MPI_Op_create.3
%{tpls_prefix}/share/man/man3/MPI_Op_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Op_free.3
%{tpls_prefix}/share/man/man3/MPI_Open_port.3
%{tpls_prefix}/share/man/man3/MPI_Pack.3
%{tpls_prefix}/share/man/man3/MPI_Pack_external.3
%{tpls_prefix}/share/man/man3/MPI_Pack_external_size.3
%{tpls_prefix}/share/man/man3/MPI_Pack_size.3
%{tpls_prefix}/share/man/man3/MPI_Parrived.3
%{tpls_prefix}/share/man/man3/MPI_Pcontrol.3
%{tpls_prefix}/share/man/man3/MPI_Pready.3
%{tpls_prefix}/share/man/man3/MPI_Pready_list.3
%{tpls_prefix}/share/man/man3/MPI_Pready_range.3
%{tpls_prefix}/share/man/man3/MPI_Precv_init.3
%{tpls_prefix}/share/man/man3/MPI_Probe.3
%{tpls_prefix}/share/man/man3/MPI_Psend_init.3
%{tpls_prefix}/share/man/man3/MPI_Publish_name.3
%{tpls_prefix}/share/man/man3/MPI_Put.3
%{tpls_prefix}/share/man/man3/MPI_Query_thread.3
%{tpls_prefix}/share/man/man3/MPI_Raccumulate.3
%{tpls_prefix}/share/man/man3/MPI_Recv.3
%{tpls_prefix}/share/man/man3/MPI_Recv_init.3
%{tpls_prefix}/share/man/man3/MPI_Reduce.3
%{tpls_prefix}/share/man/man3/MPI_Reduce_init.3
%{tpls_prefix}/share/man/man3/MPI_Reduce_local.3
%{tpls_prefix}/share/man/man3/MPI_Reduce_scatter.3
%{tpls_prefix}/share/man/man3/MPI_Reduce_scatter_block.3
%{tpls_prefix}/share/man/man3/MPI_Reduce_scatter_block_init.3
%{tpls_prefix}/share/man/man3/MPI_Reduce_scatter_init.3
%{tpls_prefix}/share/man/man3/MPI_Register_datarep.3
%{tpls_prefix}/share/man/man3/MPI_Request_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Request_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Request_free.3
%{tpls_prefix}/share/man/man3/MPI_Request_get_status.3
%{tpls_prefix}/share/man/man3/MPI_Rget.3
%{tpls_prefix}/share/man/man3/MPI_Rget_accumulate.3
%{tpls_prefix}/share/man/man3/MPI_Rput.3
%{tpls_prefix}/share/man/man3/MPI_Rsend.3
%{tpls_prefix}/share/man/man3/MPI_Rsend_init.3
%{tpls_prefix}/share/man/man3/MPI_Scan.3
%{tpls_prefix}/share/man/man3/MPI_Scan_init.3
%{tpls_prefix}/share/man/man3/MPI_Scatter.3
%{tpls_prefix}/share/man/man3/MPI_Scatter_init.3
%{tpls_prefix}/share/man/man3/MPI_Scatterv.3
%{tpls_prefix}/share/man/man3/MPI_Scatterv_init.3
%{tpls_prefix}/share/man/man3/MPI_Send.3
%{tpls_prefix}/share/man/man3/MPI_Send_init.3
%{tpls_prefix}/share/man/man3/MPI_Sendrecv.3
%{tpls_prefix}/share/man/man3/MPI_Sendrecv_replace.3
%{tpls_prefix}/share/man/man3/MPI_Session_create_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Session_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Session_finalize.3
%{tpls_prefix}/share/man/man3/MPI_Session_get_info.3
%{tpls_prefix}/share/man/man3/MPI_Session_get_nth_pset.3
%{tpls_prefix}/share/man/man3/MPI_Session_get_num_psets.3
%{tpls_prefix}/share/man/man3/MPI_Session_get_pset_info.3
%{tpls_prefix}/share/man/man3/MPI_Session_init.3
%{tpls_prefix}/share/man/man3/MPI_Sizeof.3
%{tpls_prefix}/share/man/man3/MPI_Ssend.3
%{tpls_prefix}/share/man/man3/MPI_Ssend_init.3
%{tpls_prefix}/share/man/man3/MPI_Start.3
%{tpls_prefix}/share/man/man3/MPI_Startall.3
%{tpls_prefix}/share/man/man3/MPI_Status_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Status_c2f08.3
%{tpls_prefix}/share/man/man3/MPI_Status_f082c.3
%{tpls_prefix}/share/man/man3/MPI_Status_f082f.3
%{tpls_prefix}/share/man/man3/MPI_Status_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Status_f2f08.3
%{tpls_prefix}/share/man/man3/MPI_Status_set_cancelled.3
%{tpls_prefix}/share/man/man3/MPI_Status_set_elements.3
%{tpls_prefix}/share/man/man3/MPI_Status_set_elements_x.3
%{tpls_prefix}/share/man/man3/MPI_T.3
%{tpls_prefix}/share/man/man3/MPI_T_category_changed.3
%{tpls_prefix}/share/man/man3/MPI_T_category_get_categories.3
%{tpls_prefix}/share/man/man3/MPI_T_category_get_cvars.3
%{tpls_prefix}/share/man/man3/MPI_T_category_get_info.3
%{tpls_prefix}/share/man/man3/MPI_T_category_get_num.3
%{tpls_prefix}/share/man/man3/MPI_T_category_get_pvars.3
%{tpls_prefix}/share/man/man3/MPI_T_cvar_get_info.3
%{tpls_prefix}/share/man/man3/MPI_T_cvar_get_num.3
%{tpls_prefix}/share/man/man3/MPI_T_cvar_handle_alloc.3
%{tpls_prefix}/share/man/man3/MPI_T_cvar_handle_free.3
%{tpls_prefix}/share/man/man3/MPI_T_cvar_read.3
%{tpls_prefix}/share/man/man3/MPI_T_cvar_write.3
%{tpls_prefix}/share/man/man3/MPI_T_enum_get_info.3
%{tpls_prefix}/share/man/man3/MPI_T_enum_get_item.3
%{tpls_prefix}/share/man/man3/MPI_T_finalize.3
%{tpls_prefix}/share/man/man3/MPI_T_init_thread.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_get_info.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_get_num.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_handle_alloc.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_handle_free.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_read.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_readreset.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_reset.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_session_create.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_session_free.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_start.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_stop.3
%{tpls_prefix}/share/man/man3/MPI_T_pvar_write.3
%{tpls_prefix}/share/man/man3/MPI_Test.3
%{tpls_prefix}/share/man/man3/MPI_Test_cancelled.3
%{tpls_prefix}/share/man/man3/MPI_Testall.3
%{tpls_prefix}/share/man/man3/MPI_Testany.3
%{tpls_prefix}/share/man/man3/MPI_Testsome.3
%{tpls_prefix}/share/man/man3/MPI_Topo_test.3
%{tpls_prefix}/share/man/man3/MPI_Type_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Type_commit.3
%{tpls_prefix}/share/man/man3/MPI_Type_contiguous.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_darray.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_f90_complex.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_f90_integer.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_f90_real.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_hindexed.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_hindexed_block.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_hvector.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_indexed_block.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_keyval.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_resized.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_struct.3
%{tpls_prefix}/share/man/man3/MPI_Type_create_subarray.3
%{tpls_prefix}/share/man/man3/MPI_Type_delete_attr.3
%{tpls_prefix}/share/man/man3/MPI_Type_dup.3
%{tpls_prefix}/share/man/man3/MPI_Type_extent.3
%{tpls_prefix}/share/man/man3/MPI_Type_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Type_free.3
%{tpls_prefix}/share/man/man3/MPI_Type_free_keyval.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_attr.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_contents.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_envelope.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_extent.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_extent_x.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_name.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_true_extent.3
%{tpls_prefix}/share/man/man3/MPI_Type_get_true_extent_x.3
%{tpls_prefix}/share/man/man3/MPI_Type_hindexed.3
%{tpls_prefix}/share/man/man3/MPI_Type_hvector.3
%{tpls_prefix}/share/man/man3/MPI_Type_indexed.3
%{tpls_prefix}/share/man/man3/MPI_Type_lb.3
%{tpls_prefix}/share/man/man3/MPI_Type_match_size.3
%{tpls_prefix}/share/man/man3/MPI_Type_set_attr.3
%{tpls_prefix}/share/man/man3/MPI_Type_set_name.3
%{tpls_prefix}/share/man/man3/MPI_Type_size.3
%{tpls_prefix}/share/man/man3/MPI_Type_size_x.3
%{tpls_prefix}/share/man/man3/MPI_Type_struct.3
%{tpls_prefix}/share/man/man3/MPI_Type_ub.3
%{tpls_prefix}/share/man/man3/MPI_Type_vector.3
%{tpls_prefix}/share/man/man3/MPI_Unpack.3
%{tpls_prefix}/share/man/man3/MPI_Unpack_external.3
%{tpls_prefix}/share/man/man3/MPI_Unpublish_name.3
%{tpls_prefix}/share/man/man3/MPI_Wait.3
%{tpls_prefix}/share/man/man3/MPI_Waitall.3
%{tpls_prefix}/share/man/man3/MPI_Waitany.3
%{tpls_prefix}/share/man/man3/MPI_Waitsome.3
%{tpls_prefix}/share/man/man3/MPI_Win_allocate.3
%{tpls_prefix}/share/man/man3/MPI_Win_allocate_shared.3
%{tpls_prefix}/share/man/man3/MPI_Win_attach.3
%{tpls_prefix}/share/man/man3/MPI_Win_c2f.3
%{tpls_prefix}/share/man/man3/MPI_Win_call_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Win_complete.3
%{tpls_prefix}/share/man/man3/MPI_Win_create.3
%{tpls_prefix}/share/man/man3/MPI_Win_create_dynamic.3
%{tpls_prefix}/share/man/man3/MPI_Win_create_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Win_create_keyval.3
%{tpls_prefix}/share/man/man3/MPI_Win_delete_attr.3
%{tpls_prefix}/share/man/man3/MPI_Win_detach.3
%{tpls_prefix}/share/man/man3/MPI_Win_f2c.3
%{tpls_prefix}/share/man/man3/MPI_Win_fence.3
%{tpls_prefix}/share/man/man3/MPI_Win_flush.3
%{tpls_prefix}/share/man/man3/MPI_Win_flush_all.3
%{tpls_prefix}/share/man/man3/MPI_Win_flush_local.3
%{tpls_prefix}/share/man/man3/MPI_Win_flush_local_all.3
%{tpls_prefix}/share/man/man3/MPI_Win_free.3
%{tpls_prefix}/share/man/man3/MPI_Win_free_keyval.3
%{tpls_prefix}/share/man/man3/MPI_Win_get_attr.3
%{tpls_prefix}/share/man/man3/MPI_Win_get_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Win_get_group.3
%{tpls_prefix}/share/man/man3/MPI_Win_get_info.3
%{tpls_prefix}/share/man/man3/MPI_Win_get_name.3
%{tpls_prefix}/share/man/man3/MPI_Win_lock.3
%{tpls_prefix}/share/man/man3/MPI_Win_lock_all.3
%{tpls_prefix}/share/man/man3/MPI_Win_post.3
%{tpls_prefix}/share/man/man3/MPI_Win_set_attr.3
%{tpls_prefix}/share/man/man3/MPI_Win_set_errhandler.3
%{tpls_prefix}/share/man/man3/MPI_Win_set_info.3
%{tpls_prefix}/share/man/man3/MPI_Win_set_name.3
%{tpls_prefix}/share/man/man3/MPI_Win_shared_query.3
%{tpls_prefix}/share/man/man3/MPI_Win_start.3
%{tpls_prefix}/share/man/man3/MPI_Win_sync.3
%{tpls_prefix}/share/man/man3/MPI_Win_test.3
%{tpls_prefix}/share/man/man3/MPI_Win_unlock.3
%{tpls_prefix}/share/man/man3/MPI_Win_unlock_all.3
%{tpls_prefix}/share/man/man3/MPI_Win_wait.3
%{tpls_prefix}/share/man/man3/MPI_Wtick.3
%{tpls_prefix}/share/man/man3/MPI_Wtime.3
%{tpls_prefix}/share/man/man3/OMPI_Affinity_str.3
%{tpls_prefix}/share/man/man3/PMIx_Abort.3
%{tpls_prefix}/share/man/man3/PMIx_Finalize.3
%{tpls_prefix}/share/man/man3/PMIx_Init.3
%{tpls_prefix}/share/man/man5/openpmix.5
%{tpls_prefix}/share/man/man5/prte.5
%{tpls_prefix}/share/man/man7/Open-MPI.7

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 5.0.1-1
- Initial Package

