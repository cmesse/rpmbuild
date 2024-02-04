%global         major 1
%global         minor 14
%global         ptch  3

%define scls_oflags -O2

Name:           scls-%{scls_flavor}-hdf5
Version:        %{major}.%{minor}.%{ptch}
Release:        1%{?dist}
Summary:        A general purpose library and file format for storing scientific data
License:        BSD
URL:            https://www.hdfgroup.org/solutions/hdf5

%global         version_main %(echo %version | cut -d. -f-2)
Source0:        https://hdf-wordpress-1.s3.amazonaws.com/wp-content/uploads/manual/HDF5/HDF5_%{major}_.%{minor}_%{ptch}/src/hdf5-%{version}.tar.gz

%if   "%{scls_mpi}" == "openmpi"
BuildRequires:  scls-%{scls_flavor}-openmpi
Requires:       scls-%{scls_flavor}-openmpi
%elif "%{scls_mpi}" == "mpich"
BuildRequires:  scls-%{scls_flavor}-mpich
Requires:       scls-%{scls_flavor}-mpich
%elif "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%endif



%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF5 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF5 files according to your needs.

%package        examples
Summary:        C-example files for HDF5

%description examples
This package contains example programs for the installed APIs and scripts to 
compile and run them.  Examples in the c and hl/c subdirectories are always 
installed, and those in fortran, hl/fortran, c++ and hl/c++ will be installed 
when fortran or c++ are enabled.

Running the run-all-ex.sh script in this directory will run the scripts and in 
turn the examples in all the subdirectories where examples are installed.  The 
scripts can also be run individually.  The appropriate compile scripts in the 
bin directory for this install will be used by default to compile and link the 
example programs.  Note that h5redeploy must be run if these binaries are 
copied or extracted in a directory other than the one where they were initially 
installed.  Compile scripts from other locations can be used by setting an 
environment variable prefix to the path of the directory containing the bin 
directory with the compile scripts h5cc, h5fc, etc.  For example, export 
prefix=%{scls_prefix} to use h5cc, h5fc, etc. in %{scls_prefix}/bin.

%prep
%setup -q -n hdf5-%{version}
sed -i 's| -V -qversion -version||g' ./configure

%build
%{scls_env} \
%{expand: %setup_scls_env}
%{scls_env} \
    CC=%{scls_mpicc} \
    FC=%{scls_mpifort} \
    AR=%{scls_ar} \
    AR_FLAGS=%{scls_arflags}  \
    CXX="%{scls_mpicxx}"\
%if "%{scls_libs}" == "static"
    CFLAGS="%{scls_cflags} -I%{scls_prefix}/include %{scls_oflags}" \
    CXXFLAGS="%{scls_cxxflags} -I%{scls_prefix}/include %{scls_oflags}" \
    FCFLAGS="%{scls_fclags} -I%{scls_prefix}/include %{scls_oflags}" \
%else
    CFLAGS="%{scls_cflags} -I%{scls_prefix}/include -fPIC %{scls_oflags}" \
    CXXFLAGS="%{scls_cxxflags} -I%{scls_prefix}/include -fPIC %{scls_oflags}" \
    FCFLAGS="%{scls_fcflags} -I%{scls_prefix}/include  -fPIC %{scls_oflags}" \
%endif
    LDFLAGS="%{scls_ldflags}" \
    ./configure \
        --prefix=%{scls_prefix} \
	    --enable-parallel \
%if "%{scls_libs}" == "static"
		--enable-static \
        --disable-shared \
%else
		--disable-static \
        --enable-shared
%endif

%make_build
     
%check
%if "%{scls_compiler}" == "intel"
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{scls_ld_library_path} make %{?_smp_mflags} check
%else
#LD_LIBRARY_PATH=%{scls_ld_library_path} make %{?_smp_mflags} check
%endif

%install
%make_install
%{scls_remove_la_files}

%files
%{scls_prefix}/bin/h5clear
%{scls_prefix}/bin/h5copy
%{scls_prefix}/bin/h5debug
%{scls_prefix}/bin/h5delete
%{scls_prefix}/bin/h5diff
%{scls_prefix}/bin/h5dump
%{scls_prefix}/bin/h5format_convert
%{scls_prefix}/bin/h5fuse.sh
%{scls_prefix}/bin/h5import
%{scls_prefix}/bin/h5jam
%{scls_prefix}/bin/h5ls
%{scls_prefix}/bin/h5mkgrp
%{scls_prefix}/bin/h5pcc
%{scls_prefix}/bin/h5perf
%{scls_prefix}/bin/h5perf_serial
%{scls_prefix}/bin/h5redeploy
%{scls_prefix}/bin/h5repack
%{scls_prefix}/bin/h5repart
%{scls_prefix}/bin/h5stat
%{scls_prefix}/bin/h5tools_test_utils
%{scls_prefix}/bin/h5unjam
%{scls_prefix}/bin/h5watch
%{scls_prefix}/bin/ph5diff
%{scls_prefix}/include/H5ACpublic.h
%{scls_prefix}/include/H5Apublic.h
%{scls_prefix}/include/H5Cpublic.h
%{scls_prefix}/include/H5DOpublic.h
%{scls_prefix}/include/H5DSpublic.h
%{scls_prefix}/include/H5Dpublic.h
%{scls_prefix}/include/H5ESdevelop.h
%{scls_prefix}/include/H5ESpublic.h
%{scls_prefix}/include/H5Epubgen.h
%{scls_prefix}/include/H5Epublic.h
%{scls_prefix}/include/H5FDcore.h
%{scls_prefix}/include/H5FDdevelop.h
%{scls_prefix}/include/H5FDdirect.h
%{scls_prefix}/include/H5FDfamily.h
%{scls_prefix}/include/H5FDhdfs.h
%{scls_prefix}/include/H5FDioc.h
%{scls_prefix}/include/H5FDlog.h
%{scls_prefix}/include/H5FDmirror.h
%{scls_prefix}/include/H5FDmpi.h
%{scls_prefix}/include/H5FDmpio.h
%{scls_prefix}/include/H5FDmulti.h
%{scls_prefix}/include/H5FDonion.h
%{scls_prefix}/include/H5FDpublic.h
%{scls_prefix}/include/H5FDros3.h
%{scls_prefix}/include/H5FDsec2.h
%{scls_prefix}/include/H5FDsplitter.h
%{scls_prefix}/include/H5FDstdio.h
%{scls_prefix}/include/H5FDsubfiling.h
%{scls_prefix}/include/H5FDwindows.h
%{scls_prefix}/include/H5Fpublic.h
%{scls_prefix}/include/H5Gpublic.h
%{scls_prefix}/include/H5IMpublic.h
%{scls_prefix}/include/H5Idevelop.h
%{scls_prefix}/include/H5Ipublic.h
%{scls_prefix}/include/H5LDpublic.h
%{scls_prefix}/include/H5LTpublic.h
%{scls_prefix}/include/H5Ldevelop.h
%{scls_prefix}/include/H5Lpublic.h
%{scls_prefix}/include/H5MMpublic.h
%{scls_prefix}/include/H5Mpublic.h
%{scls_prefix}/include/H5Opublic.h
%{scls_prefix}/include/H5PLextern.h
%{scls_prefix}/include/H5PLpublic.h
%{scls_prefix}/include/H5PTpublic.h
%{scls_prefix}/include/H5Ppublic.h
%{scls_prefix}/include/H5Rpublic.h
%{scls_prefix}/include/H5Spublic.h
%{scls_prefix}/include/H5TBpublic.h
%{scls_prefix}/include/H5TSdevelop.h
%{scls_prefix}/include/H5Tdevelop.h
%{scls_prefix}/include/H5Tpublic.h
%{scls_prefix}/include/H5VLconnector.h
%{scls_prefix}/include/H5VLconnector_passthru.h
%{scls_prefix}/include/H5VLnative.h
%{scls_prefix}/include/H5VLpassthru.h
%{scls_prefix}/include/H5VLpublic.h
%{scls_prefix}/include/H5Zdevelop.h
%{scls_prefix}/include/H5Zpublic.h
%{scls_prefix}/include/H5api_adpt.h
%{scls_prefix}/include/H5overflow.h
%{scls_prefix}/include/H5pubconf.h
%{scls_prefix}/include/H5public.h
%{scls_prefix}/include/H5version.h
%{scls_prefix}/include/hdf5.h
%{scls_prefix}/include/hdf5_hl.h
%{scls_prefix}/lib/libhdf5.settings
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libhdf5.a
%{scls_prefix}/lib/libhdf5_hl.a
%else
%{scls_prefix}/lib/libhdf5.so
%{scls_prefix}/lib/libhdf5.so.*
%{scls_prefix}/lib/libhdf5_hl.so
%{scls_prefix}/lib/libhdf5_hl.so.*
%endif

%files examples
%{scls_prefix}/share/hdf5_examples/README
%{scls_prefix}/share/hdf5_examples/c/h5_attribute.c
%{scls_prefix}/share/hdf5_examples/c/h5_chunk_read.c
%{scls_prefix}/share/hdf5_examples/c/h5_cmprss.c
%{scls_prefix}/share/hdf5_examples/c/h5_compound.c
%{scls_prefix}/share/hdf5_examples/c/h5_crtatt.c
%{scls_prefix}/share/hdf5_examples/c/h5_crtdat.c
%{scls_prefix}/share/hdf5_examples/c/h5_crtgrp.c
%{scls_prefix}/share/hdf5_examples/c/h5_crtgrpar.c
%{scls_prefix}/share/hdf5_examples/c/h5_crtgrpd.c
%{scls_prefix}/share/hdf5_examples/c/h5_debug_trace.c
%{scls_prefix}/share/hdf5_examples/c/h5_drivers.c
%{scls_prefix}/share/hdf5_examples/c/h5_elink_unix2win.c
%{scls_prefix}/share/hdf5_examples/c/h5_extend.c
%{scls_prefix}/share/hdf5_examples/c/h5_extend_write.c
%{scls_prefix}/share/hdf5_examples/c/h5_extlink.c
%{scls_prefix}/share/hdf5_examples/c/h5_group.c
%{scls_prefix}/share/hdf5_examples/c/h5_mount.c
%{scls_prefix}/share/hdf5_examples/c/h5_rdwt.c
%{scls_prefix}/share/hdf5_examples/c/h5_read.c
%{scls_prefix}/share/hdf5_examples/c/h5_ref2reg_deprec.c
%{scls_prefix}/share/hdf5_examples/c/h5_ref_compat.c
%{scls_prefix}/share/hdf5_examples/c/h5_ref_extern.c
%{scls_prefix}/share/hdf5_examples/c/h5_reference_deprec.c
%{scls_prefix}/share/hdf5_examples/c/h5_select.c
%{scls_prefix}/share/hdf5_examples/c/h5_shared_mesg.c
%{scls_prefix}/share/hdf5_examples/c/h5_subset.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds-eiger.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds-exc.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds-exclim.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds-percival-unlim-maxmin.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds-percival-unlim.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds-percival.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds-simpleIO.c
%{scls_prefix}/share/hdf5_examples/c/h5_vds.c
%{scls_prefix}/share/hdf5_examples/c/h5_write.c
%{scls_prefix}/share/hdf5_examples/c/ph5_filtered_writes.c
%{scls_prefix}/share/hdf5_examples/c/ph5_filtered_writes_no_sel.c
%{scls_prefix}/share/hdf5_examples/c/ph5_subfiling.c
%{scls_prefix}/share/hdf5_examples/c/ph5example.c
%{scls_prefix}/share/hdf5_examples/c/run-c-ex.sh
%{scls_prefix}/share/hdf5_examples/hl/c/ex_ds1.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_image1.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_image2.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_lite1.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_lite2.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_lite3.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_01.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_02.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_03.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_04.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_05.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_06.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_07.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_08.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_09.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_10.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_11.c
%{scls_prefix}/share/hdf5_examples/hl/c/ex_table_12.c
%{scls_prefix}/share/hdf5_examples/hl/c/image24pixel.txt
%{scls_prefix}/share/hdf5_examples/hl/c/image8.txt
%{scls_prefix}/share/hdf5_examples/hl/c/pal_rgb.h
%{scls_prefix}/share/hdf5_examples/hl/c/ptExampleFL.c
%{scls_prefix}/share/hdf5_examples/hl/c/run-hlc-ex.sh
%{scls_prefix}/share/hdf5_examples/hl/run-hl-ex.sh
%{scls_prefix}/share/hdf5_examples/run-all-ex.sh


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 1.14.3-1
- Initial Package
