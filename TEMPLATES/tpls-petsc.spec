Name:           tpls-%{tpls_flavor}-petsc
Version:        3.20.4
Release:        1%{?dist}
Summary:        Portable Extensible Toolkit for Scientific Computation

License:        BSD-2-Clause
URL:            https://petsc.org/
Source:         https://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc-%{version}.tar.gz

BuildRequires:  %{tpls_rpm_cc}   >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_cxx}  >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_fc}   >= %{tpls_comp_minver}

%if "%{tpls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{tpls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{tpls_comp_minver}
%endif

%if "%{tpls_gpu}" == "lapack"
BuildRequires:  tpls-%{tpls_flavor}-blas
BuildRequires:  tpls-%{tpls_flavor}-lapack
BuildRequires:  tpls-%{tpls_flavor}-scalapack
Requires:       tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-lapack
Requires:       tpls-%{tpls_flavor}-scalapack
%else
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%endif

%if   "%{tpls_mpi}" == "openmpi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%endif


BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  tpls-%{tpls_flavor}-gmp
BuildRequires:  tpls-%{tpls_flavor}-mpfr
BuildRequires:  tpls-%{tpls_flavor}-fftw
BuildRequires:  tpls-%{tpls_flavor}-metis
BuildRequires:  tpls-%{tpls_flavor}-scotch
BuildRequires:  tpls-%{tpls_flavor}-strumpack

%description
PETSc is a suite of data structures and routines for the scalable
(parallel) solution of scientific applications modeled by partial 
differential equations.


%package examples
Summary:       Examples for PETSC
Requires:      tpls-%{tpls_flavor}-petsc == %{version}

%description examples
Examples for PETSC

%prep
%setup -q -n petsc-%{version}

%build
%{expand: %setup_tpls_env}

echo comp: "%{tpls_compiler}"
unset CC
unset CXX
unset FC
unset F77
unset CFLAGS
unset CXXFLAGS
unset FFLAGS
unset CPP
unset AR
unset PETSC_DIR
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
    --CPP="%{tpls_cc} -E" \
	--CC=%{tpls_mpicc} \
	--CXXCPP=="%{tpls_cxx} -E" \
	--CXX=%{tpls_mpicxx} \
	--CFLAGS="%{tpls_cflags}" \
	--CXXFLAGS="%{tpls_cxxflags}" \
%if "%{tpls_gpu}" == "cuda"
	--CUDAC=%{tpls_nvcc} \
    --CUDAFLAGS="-I%{tpls_cudamath}/include -I%{tpls_cuda}/include" \
%endif
	--FC=%{tpls_mpifort} \
	--FFLAGS="%{tpls_fcflags}" \
%if "%{tpls_compiler}" == "gnu"
	--CC_LINKER_FLAGS="-lgfortran" \
	--CXX_LINKER_FLAGS="-lgfortran" \
%endif
%if   "%{tpls_mpi}" == "openmpi"
    --with-mpiexec=%{tpls_prefix}/bin/orterun \
    --with-mpi-include=%{tpls_prefix}/include \
%if "%{tpls_libs}" == "static"
    --with-mpi-lib=%{tpls_prefix}/lib/libmpi.a \
    --LDFLAGS="%{tpls_ldflags} -lopen-rte -lopen-pal -lm -lpciaccess -lz -lpthread -ldl"\
%else
    --with-mpi-lib=%{tpls_prefix}/lib/libmpi.so \
    --LDFLAGS="%{tpls_ldflags}"\
%endif
%elif   "%{tpls_mpi}" == "mpich"
    --with-mpiexec=%{tpls_prefix}/bin/mpiexec.hydra \
    --with-mpi-include=%{tpls_prefix}/include \
%if "%{tpls_libs}" == "static"
    --with-mpi-lib=%{tpls_prefix}/lib/libmpi.a \
%else
    --with-mpi-lib=%{tpls_prefix}/lib/libmpi.so \
%endif
    --LDFLAGS="%{tpls_ldflags} -latomic -lpthread -ldl -latomic -lpthread -ldl"\
%elif   "%{tpls_mpi}" == "openmpi"
    --with-mpiexec=%{tpls_mpiroot}/bin/mpiexec.hydra \
    --with-mpi-include=%{tpls_mpiroot}/include \
%if "%{tpls_libs}" == "static"
    --with-mpi-lib="%{tpls_mpiroot}/lib/libmpi.a" \
%else
    --with-mpi-lib="%{tpls_mpiroot}/lib/libmpi.so" \
%endif
    --LDFLAGS="%{tpls_ldflags}"\
%endif
%if "%{tpls_gpu}" == "cuda"
    --CUDAC=%{tpls_nvcc} \
%if  "%{tpls_compiler}" == "intel"
    --CUDAFLAGS="%{tpls_nvccflags}" \
%endif
%elif "%{tpls_gpu}" == "rocm"
    --with-hip-dir=%{tpls_prefix} \
%endif
%if "%{tpls_gpu}" == "lapack"
	--with-blas-lib=%{tpls_blas} \
	--with-lapack-lib=%{tpls_lapack} \
	--with-scalapack-include=%{tpls_prefix}/include \
	--with-scalapack-lib=%{tpls_scalapack} \
%else
	--with-blas-lib="%{tpls_mkl_linker_flags}" \
	--with-lapack-lib="%{tpls_mkl_linker_flags}" \
	--with-scalapack-include=%{tpls_mklroot}/include \
	--with-scalapack-lib="%{tpls_mkl_mpi_linker_flags}" \
%endif
%if "%{tpls_int}" == "32"
	--with-64-bit-blas-indices=0 \
%else
	--with-64-bit-blas-indices=1 \
%endif
    --with-butterflypack-dir=%{tpls_prefix} \
    --with-cmake-dir=%{tpls_prefix} \
    --with-fftw-dir=%{tpls_prefix} \
    --with-gmp-dir=%{tpls_prefix} \
    --with-googletest-dir=%{tpls_prefix} \
    --with-hdf5-dir=%{tpls_prefix} \
    --with-hwloc-dir=%{tpls_prefix} \
    --with-mpfr-dir=%{tpls_prefix} \
    --with-metis-include=%{tpls_prefix}/include \
    --with-parmetis-include=%{tpls_prefix}/include \
    --with-zfp-include=%{tpls_prefix}/include \
    --with-strumpack-include=%{tpls_prefix}/include \
%if "%{tpls_libs}" == "static"
    --with-metis-lib="%{tpls_prefix}/lib/libmetis.a" \
    --with-scotch-lib="%{tpls_prefix}/lib/libscotch.a,%{tpls_prefix}/lib/libscotcherr.a" \
    --with-parmetis-lib="%{tpls_prefix}/lib/libparmetis.a" \
    --with-zfp-lib="%{tpls_prefix}/lib/libzfp.a" \
    --with-strumpack-lib="%{tpls_prefix}/lib/libstrumpack.a" \
%else
    --with-metis-lib="%{tpls_prefix}/lib/libmetis.so" \
    --with-scotch-lib="%{tpls_prefix}/lib/libscotch.so,%{tpls_prefix}/lib/libscotcherr.so" \
    --with-parmetis-lib="%{tpls_prefix}/lib/libparmetis.so" \
    --with-zfp-lib="%{tpls_prefix}/lib/libzfp.so" \
    --with-strumpack-lib="%{tpls_prefix}/lib/libstrumpack.so" \
%endif
%if "%{tpls_compiler}" == "gnu"
    --with-openmp-include=/usr/include/ \
    --with-openmp-lib=/usr/lib64/libgomp.so.1 \
%endif
%if "%{tpls_compiler}" == "intel"
    --with-openmp-include=%{tpls_comproot}/include \
%if "%{tpls_libs}" == "static"
    --with-openmp-lib=%{tpls_comproot}/lib/libiomp5.a \
%else
    --with-openmp-lib=%{tpls_comproot}/lib/libiomp5.so \
%endif
%endif
%if  "%{tpls_compiler}" == "nvidia"
    --with-openmp-include=%{tpls_comproot}/include \
%if "%{tpls_libs}" == "static"
    --with-openmp-lib=%{tpls_comproot}/lib/libnvomp.a \
%else
    --with-openmp-lib=%{tpls_comproot}/lib/libnvomp.so \
%endif
%endif
    --with-zlib-include=/usr/include \
    --with-zlib-lib=/usr/lib64/libz.so

%make_build

%install
#make PETSC_DIR=%{buildroot}%{tpls_prefix} PETSC_ARCH=arch-linux-c-opt install
unset PETSC_DIR
%make_install PETSC_ARCH=arch-linux-c-opt

for f in $(grep "/usr/bin" %{buildroot}%{tpls_prefix}/lib/petsc/bin -rHl ); do
    echo "checking $f"
    sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python|g' \
           -e 's|#!/usr/bin/python3|#!/usr/bin/python3|g' \
           -e 's|#!/usr/bin/python|#!/usr/bin/python3|g' $f
done

%files
%{tpls_prefix}/include/petsc*.h
%{tpls_prefix}/include/petsc*.hpp
%{tpls_prefix}/include/petsc*.mod
%{tpls_prefix}/include/petsc
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libpetsc.a
%else
%{tpls_prefix}/lib/libpetsc.so
%{tpls_prefix}/lib/libpetsc.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/PETSc.pc
%{tpls_prefix}/lib/pkgconfig/petsc.pc
%{tpls_prefix}/lib/petsc
%{tpls_prefix}/share/petsc/matlab
%{tpls_prefix}/share/petsc/saws
%{tpls_prefix}/share/petsc/suppressions
%{tpls_prefix}/share/petsc/bin
%{tpls_prefix}/share/petsc/*.py

%files examples
%{tpls_prefix}/share/petsc/CMakeLists.txt
%{tpls_prefix}/share/petsc/Makefile*
%{tpls_prefix}/share/petsc/datafiles
%{tpls_prefix}/share/petsc/examples
%{tpls_prefix}/share/petsc/xml

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.20.4-1
- Initial Package