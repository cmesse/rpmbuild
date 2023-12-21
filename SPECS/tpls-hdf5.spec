%global         major 1
%global         minor 14
%global         ptch  3


Name:           tpls-%{tpls_flavor}-hdf5
Version:        %{major}.%{minor}.%{ptch}
Release:        1%{?dist}
Summary:        A general purpose library and file format for storing scientific data
License:        BSD
URL:            https://portal.hdfgroup.org/display/HDF5/HDF5

%global         version_main %(echo %version | cut -d. -f-2)
Source0:        https://hdf-wordpress-1.s3.amazonaws.com/wp-content/uploads/manual/HDF5/HDF5_%{major}_.%{minor}_%{ptch}/src/hdf5-%{version}.tar.gz

%if   "%{tpls_mpi}" == "openempi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
BuildRequires:  intel-oneapi-mpi
%end

AutoReqProv:    %{tpls_auto_req_prov}

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
prefix=%{tpls_prefix} to use h5cc, h5fc, etc. in %{tpls_prefix}/bin. 

%prep
%setup -q -n hdf5-%{version}
sed -i 's| -V -qversion -version||g' ./configure

%build

%{setup_tpls_env}

    CC=%{tpls_mpicc} \
    CXX=%{tpls_mpicxx} \
    FC=%{tpls_mpifort} \
    AR=%{tpls_ar} \
    AR_FLAGS=AR=%{tpls_arflags}  \
%if "%{tpls_libs}" == "static"
    CFLAGS="%{tpls_cflags} -I%{tpls_prefix}/include" \
    CXXFLAGS="%{tpls_cflags} -I%{tpls_prefix}/include" \
    FCFLAGS="%{tpls_cflags} -I%{tpls_prefix}/include" \
%else
    CFLAGS="%{tpls_cflags} -I%{tpls_prefix}/include -fPIC" \
    CXXFLAGS="%{tpls_cflags} -I%{tpls_prefix}/include -fPIC" \
    FCFLAGS="%{tpls_cflags} -I%{tpls_prefix}/include  -fPIC" \
%endif
    LDFLAGS="%{tpls_ldflags} %{tpls_rpath}" \
    ./configure \
        --prefix=%{tpls_prefix} \
	    --enable-parallel \
%if "%{tpls_libs}" == "static"
		--enable-static \
        --disable-shared \
%else
		--disable-static \
        --enable-shared \
%endif
        --with-default-api-version=v18
%make_build
     
%check
LD_LIBRARY_PATH=%{tpls_ld_library_path} make %{?_smp_mflags} check

%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/bin/h5clear
%{tpls_prefix}/bin/h5copy
%{tpls_prefix}/bin/h5debug
%{tpls_prefix}/bin/h5delete
%{tpls_prefix}/bin/h5diff
%{tpls_prefix}/bin/h5dump
%{tpls_prefix}/bin/h5format_convert
%{tpls_prefix}/bin/h5fuse.sh
%{tpls_prefix}/bin/h5import
%{tpls_prefix}/bin/h5jam
%{tpls_prefix}/bin/h5ls
%{tpls_prefix}/bin/h5mkgrp
%{tpls_prefix}/bin/h5pcc
%{tpls_prefix}/bin/h5perf
%{tpls_prefix}/bin/h5perf_serial
%{tpls_prefix}/bin/h5redeploy
%{tpls_prefix}/bin/h5repack
%{tpls_prefix}/bin/h5repart
%{tpls_prefix}/bin/h5stat
%{tpls_prefix}/bin/h5tools_test_utils
%{tpls_prefix}/bin/h5unjam
%{tpls_prefix}/bin/h5watch
%{tpls_prefix}/bin/ph5diff
%{tpls_prefix}/include/H5ACpublic.h
%{tpls_prefix}/include/H5Apublic.h
%{tpls_prefix}/include/H5Cpublic.h
%{tpls_prefix}/include/H5DOpublic.h
%{tpls_prefix}/include/H5DSpublic.h
%{tpls_prefix}/include/H5Dpublic.h
%{tpls_prefix}/include/H5ESdevelop.h
%{tpls_prefix}/include/H5ESpublic.h
%{tpls_prefix}/include/H5Epubgen.h
%{tpls_prefix}/include/H5Epublic.h
%{tpls_prefix}/include/H5FDcore.h
%{tpls_prefix}/include/H5FDdevelop.h
%{tpls_prefix}/include/H5FDdirect.h
%{tpls_prefix}/include/H5FDfamily.h
%{tpls_prefix}/include/H5FDhdfs.h
%{tpls_prefix}/include/H5FDioc.h
%{tpls_prefix}/include/H5FDlog.h
%{tpls_prefix}/include/H5FDmirror.h
%{tpls_prefix}/include/H5FDmpi.h
%{tpls_prefix}/include/H5FDmpio.h
%{tpls_prefix}/include/H5FDmulti.h
%{tpls_prefix}/include/H5FDonion.h
%{tpls_prefix}/include/H5FDpublic.h
%{tpls_prefix}/include/H5FDros3.h
%{tpls_prefix}/include/H5FDsec2.h
%{tpls_prefix}/include/H5FDsplitter.h
%{tpls_prefix}/include/H5FDstdio.h
%{tpls_prefix}/include/H5FDsubfiling.h
%{tpls_prefix}/include/H5FDwindows.h
%{tpls_prefix}/include/H5Fpublic.h
%{tpls_prefix}/include/H5Gpublic.h
%{tpls_prefix}/include/H5IMpublic.h
%{tpls_prefix}/include/H5Idevelop.h
%{tpls_prefix}/include/H5Ipublic.h
%{tpls_prefix}/include/H5LDpublic.h
%{tpls_prefix}/include/H5LTpublic.h
%{tpls_prefix}/include/H5Ldevelop.h
%{tpls_prefix}/include/H5Lpublic.h
%{tpls_prefix}/include/H5MMpublic.h
%{tpls_prefix}/include/H5Mpublic.h
%{tpls_prefix}/include/H5Opublic.h
%{tpls_prefix}/include/H5PLextern.h
%{tpls_prefix}/include/H5PLpublic.h
%{tpls_prefix}/include/H5PTpublic.h
%{tpls_prefix}/include/H5Ppublic.h
%{tpls_prefix}/include/H5Rpublic.h
%{tpls_prefix}/include/H5Spublic.h
%{tpls_prefix}/include/H5TBpublic.h
%{tpls_prefix}/include/H5TSdevelop.h
%{tpls_prefix}/include/H5Tdevelop.h
%{tpls_prefix}/include/H5Tpublic.h
%{tpls_prefix}/include/H5VLconnector.h
%{tpls_prefix}/include/H5VLconnector_passthru.h
%{tpls_prefix}/include/H5VLnative.h
%{tpls_prefix}/include/H5VLpassthru.h
%{tpls_prefix}/include/H5VLpublic.h
%{tpls_prefix}/include/H5Zdevelop.h
%{tpls_prefix}/include/H5Zpublic.h
%{tpls_prefix}/include/H5api_adpt.h
%{tpls_prefix}/include/H5overflow.h
%{tpls_prefix}/include/H5pubconf.h
%{tpls_prefix}/include/H5public.h
%{tpls_prefix}/include/H5version.h
%{tpls_prefix}/include/hdf5.h
%{tpls_prefix}/include/hdf5_hl.h
%{tpls_prefix}/lib/libhdf5.settings
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libhdf5.a
%{tpls_prefix}/lib/libhdf5_hl.a
%else
%{tpls_prefix}/lib/libhdf5.so
%{tpls_prefix}/lib/libhdf5.so.*
%{tpls_prefix}/lib/libhdf5_hl.so
%{tpls_prefix}/lib/libhdf5_hl.so.*
%endif

%files examples
%{tpls_prefix}/share/hdf5_examples/README
%{tpls_prefix}/share/hdf5_examples/c/h5_attribute.c
%{tpls_prefix}/share/hdf5_examples/c/h5_chunk_read.c
%{tpls_prefix}/share/hdf5_examples/c/h5_cmprss.c
%{tpls_prefix}/share/hdf5_examples/c/h5_compound.c
%{tpls_prefix}/share/hdf5_examples/c/h5_crtatt.c
%{tpls_prefix}/share/hdf5_examples/c/h5_crtdat.c
%{tpls_prefix}/share/hdf5_examples/c/h5_crtgrp.c
%{tpls_prefix}/share/hdf5_examples/c/h5_crtgrpar.c
%{tpls_prefix}/share/hdf5_examples/c/h5_crtgrpd.c
%{tpls_prefix}/share/hdf5_examples/c/h5_debug_trace.c
%{tpls_prefix}/share/hdf5_examples/c/h5_drivers.c
%{tpls_prefix}/share/hdf5_examples/c/h5_elink_unix2win.c
%{tpls_prefix}/share/hdf5_examples/c/h5_extend.c
%{tpls_prefix}/share/hdf5_examples/c/h5_extend_write.c
%{tpls_prefix}/share/hdf5_examples/c/h5_extlink.c
%{tpls_prefix}/share/hdf5_examples/c/h5_group.c
%{tpls_prefix}/share/hdf5_examples/c/h5_mount.c
%{tpls_prefix}/share/hdf5_examples/c/h5_rdwt.c
%{tpls_prefix}/share/hdf5_examples/c/h5_read.c
%{tpls_prefix}/share/hdf5_examples/c/h5_ref2reg_deprec.c
%{tpls_prefix}/share/hdf5_examples/c/h5_ref_compat.c
%{tpls_prefix}/share/hdf5_examples/c/h5_ref_extern.c
%{tpls_prefix}/share/hdf5_examples/c/h5_reference_deprec.c
%{tpls_prefix}/share/hdf5_examples/c/h5_select.c
%{tpls_prefix}/share/hdf5_examples/c/h5_shared_mesg.c
%{tpls_prefix}/share/hdf5_examples/c/h5_subset.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds-eiger.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds-exc.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds-exclim.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds-percival-unlim-maxmin.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds-percival-unlim.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds-percival.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds-simpleIO.c
%{tpls_prefix}/share/hdf5_examples/c/h5_vds.c
%{tpls_prefix}/share/hdf5_examples/c/h5_write.c
%{tpls_prefix}/share/hdf5_examples/c/ph5_filtered_writes.c
%{tpls_prefix}/share/hdf5_examples/c/ph5_filtered_writes_no_sel.c
%{tpls_prefix}/share/hdf5_examples/c/ph5_subfiling.c
%{tpls_prefix}/share/hdf5_examples/c/ph5example.c
%{tpls_prefix}/share/hdf5_examples/c/run-c-ex.sh
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_ds1.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_image1.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_image2.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_lite1.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_lite2.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_lite3.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_01.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_02.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_03.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_04.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_05.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_06.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_07.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_08.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_09.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_10.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_11.c
%{tpls_prefix}/share/hdf5_examples/hl/c/ex_table_12.c
%{tpls_prefix}/share/hdf5_examples/hl/c/image24pixel.txt
%{tpls_prefix}/share/hdf5_examples/hl/c/image8.txt
%{tpls_prefix}/share/hdf5_examples/hl/c/pal_rgb.h
%{tpls_prefix}/share/hdf5_examples/hl/c/ptExampleFL.c
%{tpls_prefix}/share/hdf5_examples/hl/c/run-hlc-ex.sh
%{tpls_prefix}/share/hdf5_examples/hl/run-hl-ex.sh
%{tpls_prefix}/share/hdf5_examples/run-all-ex.sh


%changelog
* Thu Dec 14 2023 Christian Messe <cmesse@lbl.gov> - 1.14.3-1
- Initial Package
