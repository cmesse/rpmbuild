%define          pythonversion  3.12.1
%define          tpls_host cascadelake
%define          pybin /opt/python/%{pythonversion}/bin/python3
%define          comproot /opt/intel/oneapi/compiler/latest
%define          mklroot  /opt/intel/oneapi/mkl/latest

Name:           tpls-%{tpls_host}-numpy
Version:        1.26.2
Release:        1%{?dist}
Summary:        Python Numpy Library compiled against MKL

License:        BSD
URL:            https://numpy.org
Source0:        https://github.com/numpy/numpy/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  intel-oneapi-compiler-dpcpp-cpp
BuildRequires:  intel-oneapi-compiler-fortran
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
BuildRequires:  tpls-%{tpls_host}-python == %{pythonversion}

Requires:       tpls-%{tpls_host}-python == %{pythonversion}
Requires:       intel-oneapi-mkl

%description
NumPy is the fundamental package for scientific computing in Python. 
It is a Python library that provides a multidimensional array object, 
various derived objects (such as masked arrays and matrices), and an
assortment of routines for fast operations on arrays, including
mathematical, logical, shape manipulation, sorting, selecting, I/O,
discrete Fourier transforms, basic linear algebra, basic statistical
operations, random simulation and much more.

%prep
%setup -q -n numpy-%{version}

pushd numpy/core/src/npysort/x86-simd-sort
tar xvf numpy_x86-simd-sort_missing.tar.xz -C .
popd

%build


# create a virtual environment
if [ -d %{buildroot}/opt/python/%{pythonversion} ] ; then
   rm -rf %{buildroot}/opt/python/%{pythonversion}
fi
%{pybin} -m venv  %{buildroot}/opt/python/%{pythonversion}
source  %{buildroot}/opt/python/%{pythonversion}/bin/activate
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
python3 -m pip install setuptools
python3 -m pip install Cython pybind11

# create the site.cfg file
echo "[mkl]" > site.cfg
echo "include_dirs = %{mklroot}/include" >> site.cfg
echo "library_dirs = %{mklroot}/lib" >> site.cfg
echo "libraries    = mkl_rt" >> site.cfg

# make sure that the compiler is set
if [ "$SETVARS_COMPLETED" != "1" ]; then \
	source /opt/intel/oneapi/setvars.sh intel64; \
fi;

PATH=/opt/intel/oneapi/compiler/latest/bin:$PATH \
CC=icx \
CXX=icpx \
FC=ifx \
F77=ifx \
FF=ifx \
LDFLAGS="-L/opt/python/%{pythonversion}/lib -L/opt/intel/oneapi/mkl/latest/lib -L/opt/intel/oneapi/compiler/latest/lib  -Wl,-rpath,/opt/python/%{pythonversion}/lib  -Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib -Wl,-rpath,/opt/intel/oneapi/compiler/latest/lib" \
CFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC -qmkl=parallel" \
CXXFLAGS="-O3 -fp-model precise -march=%{tpls_host}  -std=c++17 -fPIC  -qmkl=parallel " \
python setup.py build

%install
PATH=/opt/intel/oneapi/compiler/latest/bin:$PATH \
CC=icx \
CXX=icpx \
FC=ifx \
F77=ifx \
FF=ifx \
LDFLAGS="-L/opt/python/%{pythonversion}/lib -L/opt/intel/oneapi/mkl/latest/lib -L/opt/intel/oneapi/compiler/latest/lib  -Wl,-rpath,/opt/python/%{pythonversion}/lib  -Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib -Wl,-rpath,/opt/intel/oneapi/compiler/latest/lib" \
CFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC -qmkl=parallel" \
CXXFLAGS="-O3 -fp-model precise -march=%{tpls_host} -fPIC -std=c++17 -qmkl=parallel" \
python setup.py install


%post
source  %{buildroot}/opt/python/%{pythonversion}/bin/activate
pip3 uninstall Cython
pip3 uninstall py11
pip3 uninstall pybind11
pip3 uninstall setuptools

%files


%changelog
* Tue Dec 19 2023 Christian Messe <cmesse@lbl.gov> - 1.26.2-1
- Initial Package
