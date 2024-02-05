%define scls_oflags -O2

Name:           scls-%{scls_flavor}-petsc
Version:        3.20.4
Release:        1%{?dist}
Summary:        Portable Extensible Toolkit for Scientific Computation

License:        BSD-2-Clause
URL:            https://petsc.org/
Source:         https://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc-%{version}.tar.gz

BuildRequires:  %{scls_rpm_cc}   >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_cxx}  >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_fc}   >= %{scls_comp_minver}

%if "%{scls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{scls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{scls_comp_minver}
%endif

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

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  scls-%{scls_flavor}-gmp
BuildRequires:  scls-%{scls_flavor}-mpfr
BuildRequires:  scls-%{scls_flavor}-fftw
BuildRequires:  scls-%{scls_flavor}-hdf5
BuildRequires:  scls-%{scls_flavor}-metis
BuildRequires:  scls-%{scls_flavor}-scotch
BuildRequires:  scls-%{scls_flavor}-googletest

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%if "%{scls_math}" != "lapack"
BuildRequires: intel-oneapi-mkl
BuildRequires: intel-oneapi-mkl-devel
Requires:      intel-oneapi-mkl
%endif

%description
PETSc is a suite of data structures and routines for the scalable
(parallel) solution of scientific applications modeled by partial 
differential equations.


%package examples
Summary:       Examples for PETSC
Requires:      scls-%{scls_flavor}-petsc == %{version}

%description examples
Examples for PETSC

%prep
%setup -q -n petsc-%{version}

%build
%{expand: %setup_scls_env}



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
    --prefix=%{scls_prefix} \
	--enable-cxx \
%if "%{scls_libs}" == "static"
	--enable-static \
	--disable-shared \
    --with-pic=false \
%else
	--disable-static \
	--enable-shared \
    --with-pic=true \
%endif
    --CPP="%{scls_cc} -E" \
	--CC=%{scls_mpicc} \
	--CXXCPP=="%{scls_cxx} -E" \
	--CXX=%{scls_mpicxx} \
	--CFLAGS="%{scls_cflags} %{scls_oflags}" \
	--CXXFLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_math}" == "cuda"
	--CUDAC=%{scls_nvcc} \
    --CUDAFLAGS="-I%{scls_cudamath}/include -I%{scls_cuda}/include" \
%endif
	--FC=%{scls_mpifort} \
	--FFLAGS="%{scls_fcflags}" \
%if "%{scls_compiler}" == "gnu"
	--CC_LINKER_FLAGS="%{scls_ldflags} -lgfortran" \
	--CXX_LINKER_FLAGS="%{scls_ldflags} -lgfortran" \
%else
	--CC_LINKER_FLAGS="%{scls_ldflags}" \
	--CXX_LINKER_FLAGS="%{scls_ldflags}" \
%endif
%if   "%{scls_mpi}" == "openmpi"
    --with-mpiexec=%{scls_prefix}/bin/orterun \
    --with-mpi-include=%{scls_prefix}/include \
%if "%{scls_libs}" == "static"
    --with-mpi-lib=%{scls_prefix}/lib/libmpi.a \
    --LDFLAGS="%{scls_ldflags} -lopen-rte -lopen-pal -lm -lpciaccess -lz -lpthread -ldl"\
%else
    --with-mpi-lib=%{scls_prefix}/lib/libmpi.so \
    --LDFLAGS="%{scls_ldflags}"\
%endif
    --with-mpiexec=%{scls_mpiexec} \
%elif   "%{scls_mpi}" == "mpich"
    --with-mpi-include=%{scls_prefix}/include \
%if "%{scls_libs}" == "static"
    --with-mpi-lib=%{scls_prefix}/lib/libmpi.a \
%else
    --with-mpi-lib=%{scls_prefix}/lib/libmpi.so \
%endif
    --LDFLAGS="%{scls_ldflags} -latomic -lpthread -ldl -latomic -lpthread -ldl"\
%elif   "%{scls_mpi}" == "openmpi"
    --with-mpi-include=%{scls_mpiroot}/include \
%if "%{scls_libs}" == "static"
    --with-mpi-lib="%{scls_mpiroot}/lib/libmpi.a" \
%else
    --with-mpi-lib="%{scls_mpiroot}/lib/libmpi.so" \
%endif
    --LDFLAGS="%{scls_ldflags}"\
%endif
%if "%{scls_math}" == "cuda"
    --CUDAC=%{scls_nvcc} \
%if  "%{scls_compiler}" == "intel"
    --CUDAFLAGS="%{scls_nvccflags}" \
%endif
%endif
%if "%{scls_math}" == "lapack"
	--with-blas-lib=%{scls_blas} \
	--with-lapack-lib=%{scls_lapack} \
	--with-scalapack-include=%{scls_prefix}/include \
	--with-scalapack-lib=%{scls_scalapack} \
%else
	--with-blas-lib="%{scls_mkl_linker_flags}" \
	--with-lapack-lib="%{scls_mkl_linker_flags}" \
	--with-scalapack-include=%{scls_mklroot}/include \
	--with-scalapack-lib="%{scls_mkl_mpi_linker_flags}" \
%endif
%if "%{scls_index_size}" == "32"
	--with-64-bit-blas-indices=0 \
%else
	--with-64-bit-blas-indices=1 \
%endif
    --with-cmake-dir=%{scls_prefix} \
    --with-fftw-dir=%{scls_prefix} \
    --with-gmp-dir=%{scls_prefix} \
    --with-googletest-dir=%{scls_prefix} \
    --with-hdf5-dir=%{scls_prefix} \
    --with-hwloc-dir=%{scls_prefix} \
    --with-mpfr-dir=%{scls_prefix} \
    --with-metis-include=%{scls_prefix}/include \
    --with-parmetis-include=%{scls_prefix}/include \
    --with-zfp-include=%{scls_prefix}/include \
%if "%{scls_libs}" == "static"
    --with-metis-lib="%{scls_prefix}/lib/libmetis.a" \
    --with-scotch-lib="%{scls_prefix}/lib/libscotch.a,%{scls_prefix}/lib/libscotcherr.a" \
    --with-parmetis-lib="%{scls_prefix}/lib/libparmetis.a" \
    --with-zfp-lib="%{scls_prefix}/lib/libzfp.a" \
%else
    --with-metis-lib="%{scls_prefix}/lib/libmetis.so" \
    --with-scotch-lib="%{scls_prefix}/lib/libscotch.so,%{scls_prefix}/lib/libscotcherr.so" \
    --with-parmetis-lib="%{scls_prefix}/lib/libparmetis.so" \
    --with-zfp-lib="%{scls_prefix}/lib/libzfp.so" \
%endif
%if "%{scls_compiler}" == "gnu"
    --with-openmp-include=/usr/include/ \
    --with-openmp-lib=/usr/lib64/libgomp.so.1 \
%endif
%if "%{scls_compiler}" == "intel"
    --with-openmp-include=%{scls_comproot}/include \
%if "%{scls_libs}" == "static"
    --with-openmp-lib=%{scls_comproot}/lib/libiomp5.a \
%else
    --with-openmp-lib=%{scls_comproot}/lib/libiomp5.so \
%endif
%endif
%if  "%{scls_compiler}" == "nvidia"
    --with-openmp-include=%{scls_comproot}/include \
%if "%{scls_libs}" == "static"
    --with-openmp-lib=%{scls_comproot}/lib/libnvomp.a \
%else
    --with-openmp-lib=%{scls_comproot}/lib/libnvomp.so \
%endif
%endif
    --with-zlib-include=/usr/include \
    --with-zlib-lib=/usr/lib64/libz.so

%make_build

%install
#make PETSC_DIR=%{buildroot}%{scls_prefix} PETSC_ARCH=arch-linux-c-opt install
unset PETSC_DIR
%make_install PETSC_ARCH=arch-linux-c-opt

for f in $(grep "/usr/bin" %{buildroot}%{scls_prefix}/lib/petsc/bin -rHl ); do
    echo "checking $f"
    sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python|g' \
           -e 's|#!/usr/bin/python3|#!/usr/bin/python3|g' \
           -e 's|#!/usr/bin/python|#!/usr/bin/python3|g' $f
    sed -i 's|python33|python3|g' $f
done

%files
%{scls_prefix}/include/petsc*.h
%{scls_prefix}/include/petsc*.hpp
%{scls_prefix}/include/petsc*.mod
%{scls_prefix}/include/petsc
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libpetsc.a
%else
%{scls_prefix}/lib/libpetsc.so
%{scls_prefix}/lib/libpetsc.so.*
%endif
%{scls_prefix}/lib/pkgconfig/PETSc.pc
%{scls_prefix}/lib/pkgconfig/petsc.pc
%{scls_prefix}/lib/petsc
%{scls_prefix}/share/petsc/matlab
%{scls_prefix}/share/petsc/saws
%{scls_prefix}/share/petsc/suppressions
%{scls_prefix}/share/petsc/bin
%{scls_prefix}/share/petsc/*.py

%files examples
%{scls_prefix}/share/petsc/CMakeLists.txt
%{scls_prefix}/share/petsc/Makefile*
%{scls_prefix}/share/petsc/datafiles
%{scls_prefix}/share/petsc/examples
%{scls_prefix}/share/petsc/xml

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.20.4-1
- Initial Package