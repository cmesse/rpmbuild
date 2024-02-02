%define  opensslversion 3.2.0
%define  pythonversion  3.12.1
%define          pybin /opt/python/%{pythonversion}/bin/python3

%global pybasever 3.12

%define  tpls_host cascadelake

Name:           tpls-%{tpls_host}-python
Version:        3.12.1
Release:        1%{?dist}
Summary:        Summary: Python %{version} interpreter compiled with icx
License:        Python-2.0.1
URL:            https://www.python.org/

Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz 

Patch0:         python-3.12.1-shebang.patch

Requires:  intel-oneapi-mkl
Requires:  tpls-%{tpls_host}-openssl == %{opensslversion}

BuildRequires:  intel-oneapi-compiler-dpcpp-cpp
BuildRequires:  intel-oneapi-compiler-fortran
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
BuildRequires:  intel-oneapi

%description
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

%prep
%setup -q -n Python-%{version}
%patch0 -p1


%build

if [ "$SETVARS_COMPLETED" != "1" ]; then \
  source /opt/intel/oneapi/setvars.sh intel64; \
fi;

sed -i 's| -V -qversion -version||g' ./configure

for f in ./Lib/cgi.py ./Lib/test/test_getpath.py ; do
	sed -i 's|/usr/local/bin/python|/opt/python/%{version}/bin/python3|g' $f ;
done

export CC=icx
export CXX=icpx
export CPP="icx -E"
export CXXCPP="icpx -E"
export FC="ifx -rpath /opt/intel/oneapi/mkl/latest/lib:/opt/intel/oneapi/compiler/latest/lib"
export F77=$FC

CFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC  -qmkl=parallel " \
CXXFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC  -qmkl=parallel " \
LIBS="-lpthread /opt/intel/oneapi/compiler/latest/lib/libimf.so /opt/intel/oneapi/compiler/latest/lib/libirc.so -L/opt/python/%{version}/lib -L/opt/intel/oneapi/mkl/latest/lib -L/opt/intel/oneapi/compiler/latest/lib -Wl,-rpath,/opt/python/%{version}/lib -Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib -Wl,-rpath,/opt/intel/oneapi/compiler/latest/lib/" \
./configure \
	--prefix=/opt/python/%{version} \
	--enable-shared \
	--with-openssl=/opt/python/%{version} \
	--enable-optimizations \
	--with-computed-gotos \
	--with-libm=/opt/intel/oneapi/compiler/latest/lib/libimf.so \
    --with-ensurepip=install
    
%make_build

%install
%make_install

pushd %{buildroot}/opt/python/%{version}/bin
ln -s /opt/python/%{version}/bin/python%{pybasever} python
popd

%files
/opt/python/%{version}/bin/2to3
/opt/python/%{version}/bin/2to3-%{pybasever}
/opt/python/%{version}/bin/idle3
/opt/python/%{version}/bin/idle%{pybasever}
/opt/python/%{version}/bin/pip3
/opt/python/%{version}/bin/pip%{pybasever}
/opt/python/%{version}/bin/pydoc3
/opt/python/%{version}/bin/pydoc%{pybasever}
/opt/python/%{version}/bin/python
/opt/python/%{version}/bin/python3
/opt/python/%{version}/bin/python3-config
/opt/python/%{version}/bin/python%{pybasever}
/opt/python/%{version}/bin/python%{pybasever}-config
/opt/python/%{version}/include/python%{pybasever}
/opt/python/%{version}/lib/python%{pybasever}
/opt/python/%{version}/lib/libpython3.so
/opt/python/%{version}/lib/libpython%{pybasever}.so
/opt/python/%{version}/lib/libpython%{pybasever}.so.1.0
/opt/python/%{version}/lib/pkgconfig/python-%{pybasever}-embed.pc
/opt/python/%{version}/lib/pkgconfig/python-%{pybasever}.pc
/opt/python/%{version}/lib/pkgconfig/python3-embed.pc
/opt/python/%{version}/lib/pkgconfig/python3.pc
/opt/python/%{version}/share/man/man1/python3.1
/opt/python/%{version}/share/man/man1/python%{pybasever}.1



%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.20.0-1
- Initial package.
