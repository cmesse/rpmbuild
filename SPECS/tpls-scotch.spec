Name:           tpls-%{tpls_flavor}-scotch
Version:        7.0.4
Release:        1%{?dist}
Summary:        Graph, mesh and hypergraph partitioning library

License:        CeCILL-C
URL:            https://www.labri.fr/perso/pelegrin/scotch/
Source0:        https://gitlab.inria.fr/scotch/scotch/-/archive/v%{version}/scotch-v%{version}.tar.bz2

# taken from debian
Patch0:         build-shared-library-soname.patch
Patch1:         metis-header.patch
Patch2:         include_headers.patch
Patch3:         default_metis_v5.patch     


BuildRequires:  %{tpls_rpm_cc}  >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_fc}  >= %{tpls_comp_minver}
BuildRequires: make
BuildRequires: flex
BuildRequires: bison
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-scalapack
%endif


AutoReqProv:   %{tpls_auto_req_prov}

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch libraries are packaged in the


%prep
%setup -q -n scotch-v%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%build

%{expand: %setup_tpls_env}

cd src
echo "EXE		=" >> Makefile.inc
%if "%{tpls_libs}" == "static"
echo "LIB		= .a" >> Makefile.inc
%else
echo "LIB		= .so" >> Makefile.inc
%endif
echo "OBJ		= .o" >> Makefile.inc
echo "" >> Makefile.inc
echo "MAKE		= make" >> Makefile.inc
%if "%{tpls_libs}" == "static"
echo "AR		= %{tpls_ar}" >> Makefile.inc
echo "ARFLAGS	= %{tpls_arflags}" >> Makefile.inc
%else
echo "AR		= %{tpls_cc}" >> Makefile.inc
echo "ARFLAGS	= -shared -o " >> Makefile.inc
%endif
echo "CAT		= cat" >> Makefile.inc
echo "CCS		= %{tpls_cc }" >> Makefile.inc
echo "CCP		= mpicc" >> Makefile.inc
echo "CCD		= %{tpls_cc }" >> Makefile.inc

%if "%{tpls_libs}" == "static"
echo "CFLAGS	= %{tpls_coptflags} -I%{tpls_prefix}/include -DCOMMON_FILE_COMPRESS_GZ -DCOMMON_PTHREAD -DCOMMON_PTHREAD_AFFINITY_LINUX -DCOMMON_RANDOM_FIXED_SEED -DSCOTCH_MPI_ASYNC_COLL -DSCOTCH_PTHREAD -DSCOTCH_PTHREAD_MPI -DSCOTCH_RENAME -Drestrict=__restrict -DIDXSIZE%{tpls_intsize}" >> Makefile.inc
%else
echo "CFLAGS	= %{tpls_coptflags}  -I%{tpls_prefix}/include -fPIC -DCOMMON_FILE_COMPRESS_GZ -DCOMMON_PTHREAD -DCOMMON_PTHREAD_AFFINITY_LINUX -DCOMMON_RANDOM_FIXED_SEED -DSCOTCH_MPI_ASYNC_COLL -DSCOTCH_PTHREAD -DSCOTCH_PTHREAD_MPI -DSCOTCH_RENAME -Drestrict=__restrict -DIDXSIZE%{tpls_intsize}" >> Makefile.inc
%endif

echo "CLIBFLAGS	= " >> Makefile.inc



echo "LDFLAGS	= %{tpls_libpath} -lz -lm -lrt -pthread" >> Makefile.inc
echo "CP		= cp" >> Makefile.inc
echo "FLEX		= flex" >> Makefile.inc
echo "LN		= ln" >> Makefile.inc
echo "MKDIR		= mkdir -p" >> Makefile.inc
echo "MV		= mv" >> Makefile.inc
%if "%{tpls_libs}" == "static"
echo "RANLIB    = ranlib" >> Makefile.inc
%else
echo "RANLIB    = echo" >> Makefile.inc
%endif
echo "BISON		= bison" >> Makefile.inc

sed -i "s|?= /usr/local|= %{buildroot}/%{tpls_prefix}|g" Makefile

make %{?_smp_mflags}

%check
cd src
LD_LIBRARY_PATH=$(dirname $(pwd))/lib  FC=%{tpls_fc}  make %{?_smp_mflags} check


%install
cd src
make install

%files
%{tpls_prefix}/bin/acpl
%{tpls_prefix}/bin/amk_ccc
%{tpls_prefix}/bin/amk_fft2
%{tpls_prefix}/bin/amk_grf
%{tpls_prefix}/bin/amk_hy
%{tpls_prefix}/bin/amk_m2
%{tpls_prefix}/bin/amk_p2
%{tpls_prefix}/bin/atst
%{tpls_prefix}/bin/dggath
%{tpls_prefix}/bin/dgmap
%{tpls_prefix}/bin/dgord
%{tpls_prefix}/bin/dgpart
%{tpls_prefix}/bin/dgscat
%{tpls_prefix}/bin/dgtst
%{tpls_prefix}/bin/gbase
%{tpls_prefix}/bin/gcv
%{tpls_prefix}/bin/gdump
%{tpls_prefix}/bin/gmap
%{tpls_prefix}/bin/gmk_hy
%{tpls_prefix}/bin/gmk_m2
%{tpls_prefix}/bin/gmk_m3
%{tpls_prefix}/bin/gmk_msh
%{tpls_prefix}/bin/gmk_ub2
%{tpls_prefix}/bin/gmtst
%{tpls_prefix}/bin/gord
%{tpls_prefix}/bin/gotst
%{tpls_prefix}/bin/gout
%{tpls_prefix}/bin/gpart
%{tpls_prefix}/bin/gscat
%{tpls_prefix}/bin/gtst
%{tpls_prefix}/bin/mcv
%{tpls_prefix}/bin/mmk_m2
%{tpls_prefix}/bin/mmk_m3
%{tpls_prefix}/bin/mord
%{tpls_prefix}/bin/mtst
%exclude %{tpls_prefix}/include/metis.h
%exclude %{tpls_prefix}/include/metisf.h
%exclude %{tpls_prefix}/include/parmetis.h
%{tpls_prefix}/include/ptscotch.h
%{tpls_prefix}/include/ptscotchf.h
%{tpls_prefix}/include/scotch.h
%{tpls_prefix}/include/scotchf.h
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libptscotch.a
%{tpls_prefix}/lib/libptscotcherr.a
%{tpls_prefix}/lib/libptscotcherrexit.a
%{tpls_prefix}/lib/libptscotchparmetisv3.a
%{tpls_prefix}/lib/libscotch.a
%{tpls_prefix}/lib/libscotcherr.a
%{tpls_prefix}/lib/libscotcherrexit.a
%exclude %{tpls_prefix}/lib/libscotchmetisv3.a
%exclude %{tpls_prefix}/lib/libscotchmetisv5.a
%else
%{tpls_prefix}/lib/libptscotch-7.0.4.so
%{tpls_prefix}/lib/libptscotch-7.0.so
%{tpls_prefix}/lib/libptscotch.so
%{tpls_prefix}/lib/libptscotcherr-7.0.4.so
%{tpls_prefix}/lib/libptscotcherr-7.0.so
%{tpls_prefix}/lib/libptscotcherr.so
%{tpls_prefix}/lib/libptscotcherrexit-7.0.4.so
%{tpls_prefix}/lib/libptscotcherrexit-7.0.so
%{tpls_prefix}/lib/libptscotcherrexit.so
%{tpls_prefix}/lib/libptscotchparmetisv3-7.0.4.so
%{tpls_prefix}/lib/libptscotchparmetisv3-7.0.so
%{tpls_prefix}/lib/libptscotchparmetisv3.so
%{tpls_prefix}/lib/libscotch-7.0.4.so
%{tpls_prefix}/lib/libscotch-7.0.so
%{tpls_prefix}/lib/libscotch.so
%{tpls_prefix}/lib/libscotcherr-7.0.4.so
%{tpls_prefix}/lib/libscotcherr-7.0.so
%{tpls_prefix}/lib/libscotcherr.so
%{tpls_prefix}/lib/libscotcherrexit-7.0.4.so
%{tpls_prefix}/lib/libscotcherrexit-7.0.so
%{tpls_prefix}/lib/libscotcherrexit.so
%exclude %{tpls_prefix}/lib/libscotchmetisv3-7.0.4.so
%exclude %{tpls_prefix}/lib/libscotchmetisv3-7.0.so
%exclude %{tpls_prefix}/lib/libscotchmetisv3.so
%exclude %{tpls_prefix}/lib/libscotchmetisv5-7.0.4.so
%exclude %{tpls_prefix}/lib/libscotchmetisv5-7.0.so
%exclude %{tpls_prefix}/lib/libscotchmetisv5.so
%endif
%{tpls_prefix}/share/man/man1/Makefile
%{tpls_prefix}/share/man/man1/acpl.1
%{tpls_prefix}/share/man/man1/acpl.1.txt
%{tpls_prefix}/share/man/man1/amk_ccc.1
%{tpls_prefix}/share/man/man1/amk_ccc.1.txt
%{tpls_prefix}/share/man/man1/amk_grf.1
%{tpls_prefix}/share/man/man1/amk_grf.1.txt
%{tpls_prefix}/share/man/man1/atst.1
%{tpls_prefix}/share/man/man1/atst.1.txt
%{tpls_prefix}/share/man/man1/dgmap.1
%{tpls_prefix}/share/man/man1/dgmap.1.txt
%{tpls_prefix}/share/man/man1/dgord.1
%{tpls_prefix}/share/man/man1/dgord.1.txt
%{tpls_prefix}/share/man/man1/dgscat.1
%{tpls_prefix}/share/man/man1/dgscat.1.txt
%{tpls_prefix}/share/man/man1/dgtst.1
%{tpls_prefix}/share/man/man1/dgtst.1.txt
%{tpls_prefix}/share/man/man1/gbase.1
%{tpls_prefix}/share/man/man1/gbase.1.txt
%{tpls_prefix}/share/man/man1/gcv.1
%{tpls_prefix}/share/man/man1/gcv.1.txt
%{tpls_prefix}/share/man/man1/gdump.1
%{tpls_prefix}/share/man/man1/gdump.1.txt
%{tpls_prefix}/share/man/man1/gmap.1
%{tpls_prefix}/share/man/man1/gmap.1.txt
%{tpls_prefix}/share/man/man1/gmk_hy.1
%{tpls_prefix}/share/man/man1/gmk_hy.1.txt
%{tpls_prefix}/share/man/man1/gmk_m2.1
%{tpls_prefix}/share/man/man1/gmk_m2.1.txt
%{tpls_prefix}/share/man/man1/gmk_msh.1
%{tpls_prefix}/share/man/man1/gmk_msh.1.txt
%{tpls_prefix}/share/man/man1/gmtst.1
%{tpls_prefix}/share/man/man1/gmtst.1.txt
%{tpls_prefix}/share/man/man1/gord.1
%{tpls_prefix}/share/man/man1/gord.1.txt
%{tpls_prefix}/share/man/man1/gotst.1
%{tpls_prefix}/share/man/man1/gotst.1.txt
%{tpls_prefix}/share/man/man1/gout.1
%{tpls_prefix}/share/man/man1/gout.1.txt
%{tpls_prefix}/share/man/man1/gtst.1
%{tpls_prefix}/share/man/man1/gtst.1.txt
%{tpls_prefix}/share/man/man1/mcv.1
%{tpls_prefix}/share/man/man1/mcv.1.txt
%{tpls_prefix}/share/man/man1/mmk_m2.1
%{tpls_prefix}/share/man/man1/mmk_m2.1.txt
%{tpls_prefix}/share/man/man1/mord.1
%{tpls_prefix}/share/man/man1/mord.1.txt
%{tpls_prefix}/share/man/man1/mtst.1
%{tpls_prefix}/share/man/man1/mtst.1.txt

%changelog
* Mon Dec 18 2023 Christian Messe <cmesse@lbl.gov> - 7.0.4-1
- Initial Package
