%define  opensslversion 3.2.0
%define  pythonversion  3.12.1

Name:           tpls-%{tpls_host}-openssl
Version:        %{opensslversion}
Release:        1%{?dist}
Summary:        Utilities from the general purpose cryptography library with TLS implementation

License:        ASL 2.0
URL:            https://www.openssl.org/
Source0:        https://www.openssl.org/source/openssl-%{opensslversion}.tar.gz

BuildRequires:  intel-oneapi-compiler-dpcpp-cpp
BuildRequires:  intel-oneapi-compiler-fortran
BuildRequires:  intel-oneapi-mkl-devel
BuildRequires:  coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires:  lksctp-tools-devel
BuildRequires:  /usr/bin/rename
BuildRequires:  /usr/bin/pod2man
BuildRequires:  /usr/sbin/sysctl
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Math-BigInt
BuildRequires:  perl-Module-Load-Conditional
BuildRequires:  perl-Time-HiRes
BuildRequires:  perl-IPC-Cmd
BuildRequires:  perl-Pod-Html
BuildRequires:  perl-File-Temp
BuildRequires:  perl-Digest-SHA1
BuildRequires:  perl-FindBin
BuildRequires:  perl-File-Compare
BuildRequires:  perl-File-Copy
BuildRequires:  perl-Test-Pod
BuildRequires:  git-core
BuildRequires:  systemtap-sdt-devel
BuildRequires:  gdbm-devel
BuildRequires:  sqlite-devel

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.


%prep
%setup -q -n openssl-%{version}



%build

if [ "$SETVARS_COMPLETED" != "1" ]; then \
  source /opt/intel/oneapi/setvars.sh intel64; \
fi;

for f in $(grep -rHino ', #alloc' . | cut -d: -f 1) ; do sed -i 's|, #alloc||g' $f ; done

mkdir build && cd build

export CC=icx
export CXX=icpx
export CPP="icx -E"
export CXXCPP="icpx -E"
export FC="ifx -rpath /opt/intel/oneapi/mkl/latest/lib:/opt/intel/oneapi/compiler/latest/lib"
export F77=$FC
export CFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC  -qmkl=parallel -DPURIFY -Wa,--noexecstack -Wl,--allow-multiple-definition"
export CXXFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC  -qmkl=parallel -DPURIFY -Wa,--noexecstack -Wl,--allow-multiple-definition"
export FCFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC  -qmkl=parallel "
export F77FLAGS=$FCFLAGS
export FFLAGS=$FCFLAGS
export LIBDIR=lib
export LDFLAGS="-L/opt/intel/oneapi/mkl/latest/lib -L/opt/intel/oneapi/compiler/latest/lib -Wl,-rpath,/opt/intel/oneapi/mkl/latest -Wl,-rpath,/opt/intel/oneapi/compiler/latest/lib -Wl,--build-id"

../Configure \
	--prefix=/opt/python/%{pythonversion} \
	--openssldir=/opt/python/%{pythonversion}/etc/pki/tls \
	zlib \
	disable-fips \
	enable-rc5 \
	enable-cms \
	enable-md2 \
	enable-rc5 \
	shared
	
sed -i 's|LIBDIR=lib64|LIBDIR=lib|g' Makefile

%make_build

%install
cd build && %make_install

%files
/opt/python/%{pythonversion}/bin/c_rehash
/opt/python/%{pythonversion}/bin/openssl
/opt/python/%{pythonversion}/etc/pki/tls/
/opt/python/%{pythonversion}/include/openssl/*.h
/opt/python/%{pythonversion}/share/doc/openssl
/opt/python/%{pythonversion}/lib/pkgconfig/libcrypto.pc
/opt/python/%{pythonversion}/lib/pkgconfig/libssl.pc
/opt/python/%{pythonversion}/lib/pkgconfig/openssl.pc
%if "%{tpls_libs}" == "static"
%exclude /opt/python/%{pythonversion}/lib/engines-3/afalg.so
%exclude /opt/python/%{pythonversion}/lib/engines-3/capi.so
%exclude /opt/python/%{pythonversion}/lib/engines-3/loader_attic.so
%exclude /opt/python/%{pythonversion}/lib/engines-3/padlock.so
%exclude /opt/python/%{pythonversion}/lib/ossl-modules/legacy.so
/opt/python/%{pythonversion}/lib/libcrypto.a
%exclude /opt/python/%{pythonversion}/lib/libcrypto.so
%exclude /opt/python/%{pythonversion}/lib/libcrypto.so.3
/opt/python/%{pythonversion}/lib/libssl.a
%exclude /opt/python/%{pythonversion}/lib/libssl.so
%exclude /opt/python/%{pythonversion}/lib/libssl.so.3
%else
/opt/python/%{pythonversion}/lib/engines-3/afalg.so
/opt/python/%{pythonversion}/lib/engines-3/capi.so
/opt/python/%{pythonversion}/lib/engines-3/loader_attic.so
/opt/python/%{pythonversion}/lib/engines-3/padlock.so
/opt/python/%{pythonversion}/lib/ossl-modules/legacy.so
%exclude /opt/python/%{pythonversion}/lib/libcrypto.a
/opt/python/%{pythonversion}/lib/libcrypto.so
/opt/python/%{pythonversion}/lib/libcrypto.so.3
%exclude /opt/python/%{pythonversion}/lib/libssl.a
/opt/python/%{pythonversion}/lib/libssl.so
/opt/python/%{pythonversion}/lib/libssl.so.3
%endif
/opt/python/%{pythonversion}/share/man/man1/*.1ossl
/opt/python/%{pythonversion}/share/man/man3/*.3ossl
/opt/python/%{pythonversion}/share/man/man5/*.5ossl
/opt/python/%{pythonversion}/share/man/man7/*.7ossl

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.20.0-1
- Initial package.
