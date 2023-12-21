Name:           tpls-%{tpls_flavor}-mumps
Version:        5.6.2
Release:        1%{?dist}
Summary:        A MUltifrontal Massively Parallel sparse direct Solver

License:        CeCILL-C
URL:            http://mumps.enseeiht.fr/
Source0:        http://mumps.enseeiht.fr/MUMPS_%{version}.tar.gz

#Patch0:         MUMPS-examples-mpilibs.patch
#Patch1:         MUMPS-shared-pord.patch
#Patch2:         MUMPS-shared.patch


BuildRequires:  %{tpls_rpm_cc}  >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_fc}  >= %{tpls_comp_minver}

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-lapack
BuildRequires:  tpls-%{tpls_flavor}-scalapack
Requires:       tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-scalapack
%else
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%endif

BuildRequires:  tpls-%{tpls_flavor}-openmpi
BuildRequires:  tpls-%{tpls_flavor}-metis
BuildRequires:  tpls-%{tpls_flavor}-scotch

Requires:       tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-metis
Requires:       tpls-%{tpls_flavor}-scotch


%description
MUMPS implements a direct solver for large sparse linear systems, with a
particular focus on symmetric positive definite matrices.  It can
operate on distributed matrices e.g. over a cluster.  It has Fortran and
C interfaces, and can interface with ordering tools such as Scotch.

%prep
%setup -q -n MUMPS_%{version}

#%patch0 -p1
#%patch1 -p1
#%patch2 -p1


%build

%{expand: %setup_tpls_env}

echo "########################################################################" > Makefile.inc
echo "#              TPLS Makefile.inc created by cmesse@lbl.gov             #" >> Makefile.inc
echo "########################################################################" >> Makefile.inc
echo >> Makefile.inc
echo "# Compiler and Archiver Settings" >> Makefile.inc
echo >> Makefile.inc
echo "CC  = %{tpls_mpicc}"   >> Makefile.inc
echo "CXX = %{tpls_mpicxx}"  >> Makefile.inc
echo "FC  = %{tpls_mpifort}" >> Makefile.inc
echo "CXXCPP = %{tpls_cxxcpp}" >> Makefile.inc
echo "AR = %{tpls_ar} %{tpls_arflags} " >> Makefile.inc
echo "RANLIB = ranlib" >> Makefile.inc
echo >> Makefile.inc
echo "# Optimization Flags" >> Makefile.inc
echo >> Makefile.inc
%if "%{tpls_compiler}" == "gnu"
echo "OPTF = %{tpls_fcflags} %{tpls_ompflag} -fallow-argument-mismatch" >> Makefile.inc
echo "OPTC = %{tpls_cflags} %{tpls_ompflag}" >> Makefile.inc
echo "OPTL = %{tpls_fcflags} %{tpls_ompflag} -fallow-argument-mismatch" >> Makefile.inc
%else
echo "OPTF = %{tpls_fcflags} %{tpls_ompflag}" >> Makefile.inc
echo "OPTC = %{tpls_cflags} %{tpls_ompflag}" >> Makefile.inc
echo "OPTL = %{tpls_fcflags} %{tpls_ompflag}" >> Makefile.inc
%endif
echo >> Makefile.inc
echo "# Library Paths" >> Makefile.inc
echo "LPORDDIR = %{_builddir}/MUMPS_%{version}/PORD/lib/" >> Makefile.inc
echo "LPORD    = -L$(LPORDDIR) -lpord" >> Makefile.inc


echo >> Makefile.inc
echo "# ORDERINGS" >> Makefile.inc
echo "ORDERINGSF = -Dscotch -Dmetis -Dpord -Dptscotch -Dparmetis" >> Makefile.inc
echo "ORDERINGSC = -Dscotch -Dmetis -Dpord -Dptscotch -Dparmetis" >> Makefile.inc
echo "IORDERINGSF = -I%{tpls_prefix}/include -I%{_builddir}/MUMPS_%{version}/PORD/include" >> Makefile.inc
echo "IORDERINGSC = -I%{tpls_prefix}/include -I%{_builddir}/MUMPS_%{version}/PORD/include" >> Makefile.inc
echo "LORDERINGS  = -lparmetis -lmetis -lpord -lptesmumps -lptscotch -lptscotcherr" >> Makefile.inc
echo >> Makefile.inc
echo "# Library Settings" >> Makefile.inc
echo "LIBEXT = .a" >> Makefile.inc
echo "LIBEXT_SHARED = .so" >> Makefile.inc
echo >> Makefile.inc
%if "%{tpls_gpu}" == "lapack"
echo "LIBPAR = %{tpls_scalapack} %{tpls_lapack} %{tpls_blas}" >> Makefile.inc
echo "LIBSEQ = %{tpls_lapack} %{tpls_blas} -L$(topdir)/libseq -lmpiseq" >> Makefile.inc
%else
echo "LIBPAR = %{mkl_mpi_linker_flags}" >> Makefile.inc
echo "LIBSEQ = %{mkl_linker_flags} -L$(topdir)/libseq -lmpiseq" >> Makefile.inc
%endif
echo "LIBOTHERS = -lpthread" >> Makefile.inc
echo >> Makefile.inc
echo "# Preprocessor Definitions" >> Makefile.inc
echo "CDEFS = -DAdd_" >> Makefile.inc
echo >> Makefile.inc
echo "# Include and Library Settings for Parallel and Sequential Versions" >> Makefile.inc
echo >> Makefile.inc
echo "INCS = -I%{tpls_prefix}/include -I%{_builddir}/MUMPS_%{version}/PORD/include" >> Makefile.inc
echo "LIBS = $(LIBPAR)" >> Makefile.inc
echo "LIBSEQNEEDED =" >> Makefile.inc

%make_build

%install
%make_install

%files


%changelog
* Wed Dec 20 2023 Christian Messe <cmesse@lbl.gov> - 5.6.2-1
- Initial Package
