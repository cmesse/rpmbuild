Name:           tpls-%{tpls_flavor}-lapackpp
Version:        2023.11.05
Release:        1%{?dist}
Summary:        LAPACK++: C++ API for the Linear Algebra Package

License:        BSD
URL:            https://icl.utk.edu/slate/
Source0:        https://github.com/icl-utk-edu/lapackpp/releases/download/v2023.11.05/lapackpp-%{version}.tar.gz
Patch0:         lapackpp_no_testsweep_and_blaspp.patch 
Patch1:         lapackpp_fix_colors.patch
Patch2:         lapackpp_fix_cuda_static.patch
Patch3:         lapackpp_fix_cuda_shared.patch
Patch4:         lapackpp_fix_rocm_shared.patch

BuildRequires:  tpls-%{tpls_flavor}-blaspp == %{version}
Requires:       tpls-%{tpls_flavor}-blaspp == %{version}

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-cblas
BuildRequires:  tpls-%{tpls_flavor}-lapack
BuildRequires:  tpls-%{tpls_flavor}-lapacke
Requires:  tpls-%{tpls_flavor}-blas
Requires:  tpls-%{tpls_flavor}-cblas
Requires:  tpls-%{tpls_flavor}-lapack
Requires:  tpls-%{tpls_flavor}-lapacke
%endif

%description
he Linear Algebra PACKage (LAPACK) is a standard software library for numerical linear algebra. It provides routines for solving systems of linear equations and linear least squares problems, eigenvalue problems, and singular value decomposition. It also includes routines to implement the associated matrix factorizations such as LU, QR, Cholesky, etc. LAPACK was originally written in FORTRAN 77, and moved to Fortran 90 in version 3.2 (2008). LAPACK provides routines for handling both real and complex matrices in both single and double precision.

The objective of LAPACK++ is to provide a convenient, performance oriented API for development in the C++ language, that, for the most part, preserves established conventions, while, at the same time, takes advantages of modern C++ features, such as: namespaces, templates, exceptions, etc.

%prep

%setup -q -n lapackpp-%{version}
%patch0 -p1
%patch1 -p1
%if "%{tpls_gpu}" == "cuda"
%if "%{tpls_libs}" == "static"
%patch2 -p1
%else
%patch3 -p1
%endif
%endif
%if "%{tpls_gpu}" == "rocm"
%patch4 -p1
%endif

sed -i 's|-O2||g' make.inc.in 
sed -i 's|@CXXFLAGS@|@CXXFLAGS@ %{tpls_cxxflags} -I%{tpls_prefix}/include|g' make.inc.in 
sed -i 's|@prefix@|%{tpls_prefix}|g' make.inc.in 
sed -i 's|@CXX@|%{tpls_cxx}|g' make.inc.in 
sed -i 's|@LDFLAGS@| @LDFLAGS@ %{tpls_ldflags}|g'  make.inc.in 
%if "%{tpls_libs}" == "static"
sed -i 's|static   =|static   = 1|g' make.inc.in 
%endif

%build

%{expand: %setup_tpls_env}

PATH=%{tpls_prefix}/bin:$PATH \
LDFLAGS="-L/opt/intel/oneapi/mkl/latest/lib -Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib"  \
%if "%{tpls_gpu}" == "cuda"
python3 configure.py blas=mkl gpu_backend=cuda 
%elseif "%{tpls_gpu}" == "rocm"
python3 configure.py blas=mkl gpu_backend=rocm 
%else
%if "%{tpls_libs}" == "static"
BLAS_LIBRARIES=%{tpls_blas_static} LDFLAGS="%{tpls_prefix}/lib/libblaspp.a %{tpls_prefix}/lib/liblapacke.a  %{tpls_prefix}/lib/liblapacks.a %{tpls_prefix}/lib/libcblas.a {tpls_prefix}/lib/lblas.a" python3 configure.py
%else
LD_LIBRARY_PATH="%{tpls_prefix}/lib" LDFLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix} -lblaspp -llapacke -llapack -lcblas -lblas" BLAS_LIBRARIES=%{tpls_blas_shared} python3 configure.py
%endif
%endif

%make_build

%check
LD_LIBRARY_PATH=%{tpls_ld_library_path} make %{?_smp_mflags} check

%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/include/lapack.hh
%{tpls_prefix}/include/lapack/*.h
%{tpls_prefix}/include/lapack/*.hh
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/liblapackpp.a
%else
%{tpls_prefix}/lib/liblapackpp.so
%endif
%{tpls_prefix}/lib/pkgconfig/lapackpp.pc


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2023.11.05-1
- Initial Package
