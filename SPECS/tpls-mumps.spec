Name:           tpls-%{tpls_flavor}-mumps
Version:        5.6.2
Release:        1%{?dist}
Summary:        MUMPS libraries compiled against openmpi

License:        [license]
URL:            [URL to project homepage]
Source0:        [URL to source archive]

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

echo "# SCOTCH" > Makefile.inc
echo "SCOTCHDIR  = %{tpls_prefix}" >> Makefile.inc
echo "ISCOTCH    = -I$(SCOTCHDIR)/include" >> Makefile.inc
echo "LSCOTCH    = -lptesmumps -lptscotch -lptscotcherr -lscotch" >> Makefile.inc
echo >> Makefile.inc
echo "# PROD" >> Makefile.inc
echo "LPORDDIR = $(topdir)/PORD/lib/" >> Makefile.inc
echo "IPORD    = -I$(topdir)/PORD/include/" >> Makefile.inc
echo "LPORD    = -lpord" >> Makefile.inc
echo >> Makefile.inc
echo "# METIS" >> Makefile.inc


#-L$(LPORDDIR) 

%build
[build commands, e.g., ./configure, make]

%install
[install commands, e.g., make install DESTDIR=%{buildroot}]

%files
[files to include in the package, e.g., /usr/bin/myapp]

%changelog
* [date] [packager] - [version]-1
- Initial package.
