Name:           tpls-%{tpls_flavor}-fftw
Version:        3.3.10
Release:        1%{?dist}

Summary:        A Fast Fourier Transform library
License:        GPLv2+
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz

BuildRequires:  %{tpls_rpm_fc}  >= %{tpls_comp_minver}

%description
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

%prep
%setup -q -n fftw-%{version}

%build



%{expand: %setup_tpls_env}

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

%if "%{tpls_compiler}" == "intel"
sed -i 's|-fopenmp|-qopenmp|g' configure
%elif  "%{tpls_compiler}" == "nvidia"
sed -i 's|-fopenmp|-mp|g' configure
%endif

for ((i=0; i<2; i++)) ; do
mkdir build_${prec_name[i]} && cd build_${prec_name[i]}
%{tpls_env} ../configure \
			--prefix=%{tpls_prefix} \
%if "%{tpls_libs}" == "static"
            --enable-static  \
            --disable-shared \
%else
            --enable-shared  \
            --disable-static \
%endif
            --disable-dependency-tracking \
            --enable-openmp \
            --disable-threads \
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
%make_install
	cd ..
done
%{tpls_remove_la_files}

%check

prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad
for ((i=0; i<2; i++)) ; do
	cd build_${prec_name[i]}
	make %{?_smp_mflags} check
	cd ..
done



%files
%{tpls_prefix}/bin/fftw-wisdom
%{tpls_prefix}/bin/fftw-wisdom-to-conf
%{tpls_prefix}/bin/fftwf-wisdom
%{tpls_prefix}/include/fftw3.f
%{tpls_prefix}/include/fftw3.f03
%{tpls_prefix}/include/fftw3.h
%{tpls_prefix}/include/fftw3l.f03
%{tpls_prefix}/include/fftw3q.f03
%{tpls_prefix}/lib/cmake/fftw3/FFTW3Config.cmake
%{tpls_prefix}/lib/cmake/fftw3/FFTW3ConfigVersion.cmake
%{tpls_prefix}/lib/cmake/fftw3/FFTW3fConfig.cmake
%{tpls_prefix}/lib/cmake/fftw3/FFTW3fConfigVersion.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libfftw3.a
%{tpls_prefix}/lib/libfftw3_omp.a
%{tpls_prefix}/lib/libfftw3f.a
%{tpls_prefix}/lib/libfftw3f_omp.a
%else
%{tpls_prefix}/lib/libfftw3.so
%{tpls_prefix}/lib/libfftw3.so.*
%{tpls_prefix}/lib/libfftw3_omp.so
%{tpls_prefix}/lib/libfftw3_omp.so.*
%{tpls_prefix}/lib/libfftw3f.so
%{tpls_prefix}/lib/libfftw3f.so.*
%{tpls_prefix}/lib/libfftw3f_omp.so
%{tpls_prefix}/lib/libfftw3f_omp.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/fftw3.pc
%{tpls_prefix}/lib/pkgconfig/fftw3f.pc
%{tpls_prefix}/share/info/dir
%{tpls_prefix}/share/info/fftw3.info
%{tpls_prefix}/share/info/fftw3.info-1
%{tpls_prefix}/share/info/fftw3.info-2
%{tpls_prefix}/share/man/man1/fftw-wisdom-to-conf.1
%{tpls_prefix}/share/man/man1/fftw-wisdom.1
%{tpls_prefix}/share/man/man1/fftwf-wisdom.1


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.3.10-1
- Initial Package

