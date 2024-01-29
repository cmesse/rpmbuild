Name:           tpls-%{tpls_flavor}-petsc
Version:        3.20.3
Release:        1%{?dist}
Summary:        Portable Extensible Toolkit for Scientific Computation

License:        BSD-2-Clause
URL:            [URL to project homepage]
Source:         https://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc-%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  tpls-%{tpls_flavor}-gmp
BuildRequires:  tpls-%{tpls_flavor}-mpfr
BuildRequires:  tpls-%{tpls_flavor}-fftw
BuildRequires:  tpls-%{tpls_flavor}-hdf5
BuildRequires:  tpls-%{tpls_flavor}-metis
BuildRequires:  tpls-%{tpls_flavor}-mumps
BuildRequires:  tpls-%{tpls_flavor}-scotch

%description
PETSc is a suite of data structures and routines for the scalable
(parallel) solution of scientific applications modeled by partial 
differential equations.


%prep
%setup -q -n petsc-%{version}

%build
./configure \
    --prefix=%{tpls_prefix} \
	--enable-cxx \
%if "%{tpls_libs}" == "static"
	--enable-static \
	--disable-shared \
    --with-pic=false \
%else
	--disable-static \
	--enable-shared \
    --with-pic=true \
%endif
    --CPP=<prog>
	--CC=<prog>
	--CFLAGS=<string>
	--CC_LINKER_FLAGS=<string>
	--CXXPP=<prog>
	--CXX=<prog>
	--CXXFLAGS=<string>
	--FC=<prog>
	--FFLAGS=<string>
	--FC_LINKER_FLAGS=<string>
    --CUDAC=<prog>
    --CUDAFLAGS=<string>
    --CUDAC_LINKER_FLAGS=<string>
	--LDFLAGS=<string>
    --AR=<prog>
    --AR_FLAGS=<string>
	--with-blas-lib=<
	--with-lapack-lib=
	--with-64-bit-blas-indices=0
	--with-boost=0
	--with-cmake=<bool>
	--with-cmake-pkg-config=<dir>
    --with-cuda-dir=<dir>
    --with-cuda-pkg-config=<dir>
    --with-cuda-include=<dirs>
    --with-cuda-lib=<libraries: e.g. [/Users/..../libcuda.a,...]>
    --with-fftw-dir=<dir>
    --with-gmp=<bool>
    --with-gmp-dir=<dir>
    --with-hdf5-dir=<dir>
    --with-hwloc-dir=<dir>
    --with-metis-dir=<dir>
    --with-mpfr-dir=<dir>
    --with-mpi-dir=<dir>
    --with-mumps-dir=<dir>
    --with-ptscotch-dir=<dir>
    --with-scalapack-dir=<dir>
    --with-strumpack-dir=<dir>
    --with-suitesparse-dir=<dir>
    --with-superlu-dir=<dir>
     
%install
%make_install

%files
[files to include in the package, e.g., /usr/bin/myapp]

%changelog
* [date] [packager] - [version]-1
- Initial package.
