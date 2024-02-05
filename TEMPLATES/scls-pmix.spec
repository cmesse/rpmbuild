%define scls_oflags -O2

Name:           scls-%{scls_flavor}-pmix
Version:        4.2.9
Release:        1%{?dist}
Summary:        An extended/exascale implementation of the PMIx Standard

License:        BSD
URL:            https://github.com/openpmix/openpmix
Source0:        https://github.com/pmix/pmix/releases/download/v%{version}/pmix-%{version}.tar.bz2

BuildRequires:  zlib-devel
BuildRequires:  scls-%{scls_flavor}-libevent
Requires:       scls-%{scls_flavor}-libevent
BuildRequires:  scls-%{scls_flavor}-hwloc
Requires:       scls-%{scls_flavor}-hwloc

%description
The Process Management Interface (PMI) has been used for quite some time as a
means of exchanging wireup information needed for interprocess communication. Two
versions (PMI-1 and PMI-2) have been released as part of the MPICH effort. While
PMI-2 demonstrates better scaling properties than its PMI-1 predecessor, attaining
rapid launch and wireup of the roughly 1M processes executing across 100k nodes
expected for exascale operations remains challenging.

PMI Exascale (PMIx) represents an attempt to resolve these questions by providing
an extended version of the PMI standard specifically designed to support clusters
up to and including exascale sizes. The overall objective of the project is to
eliminate some current restrictions that impact scalability, and provide
a reference implementation of the PMIx-server that demonstrates the desired level of
scalability.

%prep
%setup -q -n pmix-%{version}

%build
%{expand: %setup_scls_env}

%{scls_env} \
./configure \
   --prefix=%{scls_prefix} \
%if "%{scls_libs}" == "static"
   --enable-static \
   --disable-shared \
%else
   --disable-static \
   --enable-shared \
%endif
    --with-pmix-headers \
    --with-libevent=%{scls_prefix} \
    --with-hwloc=%{scls_prefix} \
    --with-slurm

%make_build

%install
%make_install
%{scls_remove_la_files}

%check
%make_build check

%files
%{scls_prefix}/bin/pattrs
%{scls_prefix}/bin/pctrl
%{scls_prefix}/bin/pevent
%{scls_prefix}/bin/plookup
%{scls_prefix}/bin/pmix_info
%{scls_prefix}/bin/pmixcc
%{scls_prefix}/bin/pps
%{scls_prefix}/bin/pquery
%{scls_prefix}/etc/pmix-mca-params.conf
%{scls_prefix}/include/pmix*.h
%{scls_prefix}/include/pmix
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libpmix.a
%{scls_prefix}/lib/pmix/pmix_mca_pcompress_zlib.a
%{scls_prefix}/lib/pmix/pmix_mca_prm_default.a
%{scls_prefix}/lib/pmix/pmix_mca_prm_slurm.a
%else
%{scls_prefix}/lib/libpmix.so
%{scls_prefix}/lib/libpmix.so.*
%{scls_prefix}/lib/pmix/pmix_mca_pcompress_zlib.so
%{scls_prefix}/lib/pmix/pmix_mca_prm_default.so
%{scls_prefix}/lib/pmix/pmix_mca_prm_slurm.so
%endif
%{scls_prefix}/lib/pkgconfig/pmix.pc
%{scls_prefix}/share/doc/pmix
%{scls_prefix}/share/man/man1/pmix*.1
%{scls_prefix}/share/man/man3/PMI*.3
%{scls_prefix}/share/man/man5/openpmix.5
%{scls_prefix}/share/pmix

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 4.2.9-1
- Initial package.

