%define scls_oflags -O3

Name:           scls-%{scls_flavor}-fftw
Version:        3.3.10
Release:        1%{?dist}

Summary:        A Fast Fourier Transform library
License:        GPLv2+
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz

BuildRequires:  %{scls_rpm_fc}  >= %{scls_comp_minver}

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%description
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

%prep
%setup -q -n fftw-%{version}

%build

%{expand: %setup_scls_env}

# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

# Corresponding flags
prec_flags[0]=--enable-single
prec_flags[1]=--enable-double
prec_flags[2]=--enable-long-double
prec_flags[3]=--enable-quad-precision

for ((i=0; i<2; i++)) ; do
    prec_flags[i]+=" --enable-sse2 --enable-avx --enable-avx2"
done

%if "%{scls_compiler}" == "intel"
sed -i 's|-fopenmp|-qopenmp|g' configure
%elif  "%{scls_compiler}" == "nvidia"
sed -i 's|-fopenmp|-mp|g' configure
%endif

for ((i=0; i<2; i++)) ; do
mkdir build_${prec_name[i]} && cd build_${prec_name[i]}

%{scls_env} \
MPICC=%{scls_mpicc} \
PATH=%{scls_prefix}/bin:$PATH \
CFLAGS+=" %{scls_oflags}"  \
CXXFLAGS+=" %{scls_oflags}"  \
../configure \
			--prefix=%{scls_prefix} \
%if "%{scls_libs}" == "static"
            --enable-static  \
            --disable-shared \
%else
            --enable-shared  \
            --disable-static \
%endif
            --disable-dependency-tracking \
            --enable-openmp \
            --disable-threads \
            --enable-mpi \
            ${prec_flags[i]}
            
    make %{?_smp_mflags}
    cd ..
done  

%install
# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad
for ((i=0; i<2; i++)) ; do
	cd build_${prec_name[i]}
PATH=%{scls_prefix}/bin:$PATH %make_install
	cd ..
done
%{scls_remove_la_files}

%check
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad
for ((i=0; i<2; i++)) ; do
	cd build_${prec_name[i]}
	PATH=%{scls_prefix}/bin:$PATH make %{?_smp_mflags} check
	cd ..
done

%files
%{scls_prefix}/bin/fftw-wisdom
%{scls_prefix}/bin/fftw-wisdom-to-conf
%{scls_prefix}/bin/fftwf-wisdom
%{scls_prefix}/include/fftw*.f
%{scls_prefix}/include/fftw*.f03
%{scls_prefix}/include/fftw*.h
%{scls_prefix}/lib/cmake/fftw3/FFTW3Config.cmake
%{scls_prefix}/lib/cmake/fftw3/FFTW3ConfigVersion.cmake
%{scls_prefix}/lib/cmake/fftw3/FFTW3fConfig.cmake
%{scls_prefix}/lib/cmake/fftw3/FFTW3fConfigVersion.cmake
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libfftw3.a
%{scls_prefix}/lib/libfftw3_omp.a
%{scls_prefix}/lib/libfftw3f.a
%{scls_prefix}/lib/libfftw3f_omp.a
%{scls_prefix}/lib/libfftw3_mpi.a
%{scls_prefix}/lib/libfftw3f_mpi.a
%else
%{scls_prefix}/lib/libfftw3.so
%{scls_prefix}/lib/libfftw3.so.*
%{scls_prefix}/lib/libfftw3_omp.so
%{scls_prefix}/lib/libfftw3_omp.so.*
%{scls_prefix}/lib/libfftw3f.so
%{scls_prefix}/lib/libfftw3f.so.*
%{scls_prefix}/lib/libfftw3f_omp.so
%{scls_prefix}/lib/libfftw3f_omp.so.*
%{scls_prefix}/lib/libfftw3_mpi.so
%{scls_prefix}/lib/libfftw3_mpi.so.*
%{scls_prefix}/lib/libfftw3f_mpi.so
%{scls_prefix}/lib/libfftw3f_mpi.so.*
%endif
%{scls_prefix}/lib/pkgconfig/fftw3.pc
%{scls_prefix}/lib/pkgconfig/fftw3f.pc
%{scls_prefix}/share/info/dir
%{scls_prefix}/share/info/fftw3.info
%{scls_prefix}/share/info/fftw3.info-1
%{scls_prefix}/share/info/fftw3.info-2
%{scls_prefix}/share/man/man1/fftw-wisdom-to-conf.1
%{scls_prefix}/share/man/man1/fftw-wisdom.1
%{scls_prefix}/share/man/man1/fftwf-wisdom.1


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 1.0.1-1
- Initial Package

