%define scls_oflags -O3

Name:           scls-%{scls_flavor}-mumps

%define major_version 5
%define minor_version 6
%define patch_version 2
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        1%{?dist}
Summary:        A MUltifrontal Massively Parallel sparse direct Solver

License:        CeCILL-C
URL:            https://mumps-solver.org
Source0:        http://mumps.enseeiht.fr/MUMPS_%{version}.tar.gz

# borrowed from debian
Patch0:          mumps_fix_mumps_c.patch
Patch1:          mumps_fix_makefile.patch

BuildRequires:  %{scls_rpm_cc}  >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_fc}  >= %{scls_comp_minver}

%if "%{scls_math}" == "lapack"
BuildRequires:  scls-%{scls_flavor}-blas
BuildRequires:  scls-%{scls_flavor}-lapack
BuildRequires:  scls-%{scls_flavor}-scalapack
Requires:       scls-%{scls_flavor}-blas
Requires:       scls-%{scls_flavor}-lapack
Requires:       scls-%{scls_flavor}-scalapack
%else
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%endif

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

BuildRequires:  scls-%{scls_flavor}-metis
BuildRequires:  scls-%{scls_flavor}-parmetis
BuildRequires:  scls-%{scls_flavor}-scotch

Requires:       scls-%{scls_flavor}-metis
Requires:       scls-%{scls_flavor}-scotch
Requires:       scls-%{scls_flavor}-parmetis

%description
MUMPS implements a direct solver for large sparse linear systems, with a
particular focus on symmetric positive definite matrices.  It can
operate on distributed matrices e.g. over a cluster.  It has Fortran and
C interfaces, and can interface with ordering tools such as Scotch.

%prep
%setup -q -n MUMPS_%{version}

%patch0 -p1
%patch1 -p1

%build

%{expand: %setup_scls_env}

echo "########################################################################" > Makefile.inc
echo "#              scls Makefile.inc created by cmesse@lbl.gov             #" >> Makefile.inc
echo "########################################################################" >> Makefile.inc
echo >> Makefile.inc
echo VERSION = %{version} >> Makefile.inc
echo SOVERSION = %{major_version}.%{minor_version} >> Makefile.inc
echo >> Makefile.inc
echo "# Compiler and Archiver Settings" >> Makefile.inc
echo >> Makefile.inc
echo "CC  = %{scls_mpicc}"   >> Makefile.inc
echo "CXX = %{scls_mpicxx}"  >> Makefile.inc
echo "FC  = %{scls_mpifort}" >> Makefile.inc
echo "CXXCPP = %{scls_cxxcpp}" >> Makefile.inc
%if "%{scls_libs}" == "static"
echo "AR = %{scls_ar} %{scls_arflags} " >> Makefile.inc
echo "RANLIB = ranlib" >> Makefile.inc
%else
echo "AR = %{scls_mpifort} -shared -o " >> Makefile.inc
echo "RANLIB = echo" >> Makefile.inc 
%endif
echo >> Makefile.inc
echo "# Optimization Flags" >> Makefile.inc
echo >> Makefile.inc
%if "%{scls_compiler}" == "gnu"
echo "OPTF = %{scls_fcflags} %{scls_ompflag} -fallow-argument-mismatch %{scls_oflags}" >> Makefile.inc
echo "OPTC = %{scls_cflags} %{scls_ompflag} %{scls_oflags}" >> Makefile.inc
echo "OPTL = %{scls_fcflags} %{scls_ompflag} -fallow-argument-mismatch" >> Makefile.inc
%else
echo "OPTF = %{scls_fcflags} %{scls_ompflag} %{scls_oflags}" >> Makefile.inc
echo "OPTC = %{scls_cflags} %{scls_ompflag} %{scls_oflags}" >> Makefile.inc
echo "OPTL = %{scls_fcflags} %{scls_ompflag}" >> Makefile.inc
%endif
echo >> Makefile.inc
echo "# Library Paths" >> Makefile.inc
echo "LPORDDIR = %{_builddir}/MUMPS_%{version}/PORD/lib/" >> Makefile.inc
echo "LPORD    = -L$(LPORDDIR) -lpord" >> Makefile.inc
echo >> Makefile.inc
echo "# ORDERINGS" >> Makefile.inc
echo "ORDERINGSF = -Dscotch -Dmetis -Dpord -Dptscotch -Dparmetis" >> Makefile.inc
echo "ORDERINGSC = -Dscotch -Dmetis -Dpord -Dptscotch -Dparmetis" >> Makefile.inc
echo "IORDERINGSF = -I%{scls_prefix}/include -I%{_builddir}/MUMPS_%{version}/PORD/include" >> Makefile.inc
echo "IORDERINGSC = -I%{scls_prefix}/include -I%{_builddir}/MUMPS_%{version}/PORD/include" >> Makefile.inc
echo "LORDERINGS  = -lparmetis -lmetis -lpord -lptesmumps -lptscotch -lptscotcherr" >> Makefile.inc
echo >> Makefile.inc
echo "# Library Settings" >> Makefile.inc
%if "%{scls_libs}" == "static"
echo "LIBEXT = .a" >> Makefile.inc
%else
echo "LIBEXT = .so" >> Makefile.inc
%endif
echo "LIBEXT_SHARED = .so" >> Makefile.inc
echo "SONAME = -soname" >> Makefile.inc

echo >> Makefile.inc
%if "%{scls_math}" == "lapack"
echo "LIBPAR = %{scls_scalapack} %{scls_lapack} %{scls_blas}" >> Makefile.inc
echo "LIBSEQ = %{scls_lapack} %{scls_blas} -L$(topdir)/libseq -lmpiseq" >> Makefile.inc
echo "LIBS   = %{scls_ldflags} %{scls_scalapack} %{scls_lapack} %{scls_blas} -lpthread" >> Makefile.inc
%else
echo "LIBPAR = %{scls_mkl_mpi_linker_flags}" >> Makefile.inc
echo "LIBSEQ = %{scls_mkl_linker_flags} -L$(topdir)/libseq -lmpiseq" >> Makefile.inc
echo "LIBS   = %{scls_ldflags} %{scls_mkl_mpi_linker_flags} -lpthread" >> Makefile.inc
%endif
echo "LIBOTHERS = -lpthread" >> Makefile.inc
echo "LIBSEQNEEDED =" >> Makefile.inc
echo >> Makefile.inc
echo "# Preprocessor Definitions" >> Makefile.inc
%if %{scls_index_size} == 32
echo "CDEFS = -DAdd_" >> Makefile.inc
%else
echo "CDEFS = -DAdd_ -DINTSIZE64" >> Makefile.inc
%endif
echo >> Makefile.inc
echo "# Includes" >> Makefile.inc
echo >> Makefile.inc
echo "INCS = -I%{scls_prefix}/include -I%{_builddir}/MUMPS_%{version}/PORD/include" >> Makefile.inc

# make PORD
pushd ./PORD/lib
%if %{scls_index_size} == 32
for f in *.c ; do
   %{scls_mpicc} %{scls_cflags} %{scls_ompflag} -I../include -c $f  ;
done
%else
for f in *.c ; do
   %{scls_mpicc} %{scls_cflags} %{scls_ompflag} -DPORD_INTSIZE64 -I../include c $f ;
done
%endif
pwd
%if "%{scls_libs}" == "static"
%{scls_ar} %{scls_arflags} ../../lib/libpord.a *.o
ranlib ../../lib/libpord.a
%else
%{scls_mpicc} -shared -o ../../lib/libpord.so *.o -Wl,-soname,libpord.so -Wl,-z,defs
%endif 
popd
pushd src
make  %{?_smp_mflags} all
popd

%install
pushd lib
mkdir -p %{buildroot}%{scls_prefix}/lib
%if "%{scls_libs}" == "static"
for f in *.a ; do
   install -m 644 $f %{buildroot}%{scls_prefix}/lib ;
done ;
%else
for f in *.so ; do
   install -m 755 $f %{buildroot}%{scls_prefix}/lib ;
done ; 
%endif
popd

%files
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libcmumps.a
%{scls_prefix}/lib/libdmumps.a
%{scls_prefix}/lib/libmumps_common.a
%{scls_prefix}/lib/libpord.a
%{scls_prefix}/lib/libsmumps.a
%{scls_prefix}/lib/libzmumps.a
%else
%{scls_prefix}/lib/libcmumps.so
%{scls_prefix}/lib/libdmumps.so
%{scls_prefix}/lib/libmumps_common.so
%{scls_prefix}/lib/libpord.so
%{scls_prefix}/lib/libsmumps.so
%{scls_prefix}/lib/libzmumps.so
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 5.6.2-1
- Initial Package
