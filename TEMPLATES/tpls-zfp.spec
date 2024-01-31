Name:           tpls-%{tpls_flavor}-zfp
Version:        1.0.1
Release:        1%{?dist}
Summary:        Library for compressed numerical arrays with high throughput R/W random access

License:        BSD-3-Clause
URL:            https://computation.llnl.gov/projects/floating-point-compression
Source0:        https://github.com/LLNL/%{name}/archive/%{version}/zfp-%{version}.tar.gz
Patch0:         zfp_no_cuda_version_check.patch

BuildRequires:  tpls-%{tpls_flavor}-cmake

%description
This is zfp, an open source C/C++ library for compressed numerical arrays
that support high throughput read and write random access. zfp was written by
Peter Lindstrom at Lawrence Livermore National Laboratory, and is loosely
based on the algorithm described in the following paper:

Peter Lindstrom
"Fixed-Rate Compressed Floating-Point Arrays"
IEEE Transactions on Visualization and Computer Graphics,
  20(12):2674-2683, December 2014
doi:10.1109/TVCG.2014.2346458

zfp was originally designed for floating-point data only, but has been
extended to also support integer data, and could for instance be used to
compress images and quantized volumetric data. To achieve high compression
ratios, zfp uses lossy but optionally error-bounded compression. Although
bit-for-bit lossless compression of floating-point data is not always
possible, zfp is usually accurate to within machine epsilon in near-lossless
mode.

zfp works best for 2D and 3D arrays that exhibit spatial coherence, such as
smooth fields from physics simulations, images, regularly sampled terrain
surfaces, etc. Although zfp also provides a 1D array class that can be used
for 1D signals such as audio, or even unstructured floating-point streams,
the compression scheme has not been well optimized for this use case, and
rate and quality may not be competitive with floating-point compressors
designed specifically for 1D streams.



%prep
%setup -q -n zfp-%{version}
%patch0 -p1

%build
mkdir build && cd build
%{tpls_env} \
%{tpls_cmake} .. \
    -DCMAKE_C_COMPILER_AR=%{tpls_ar} \
    -DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
	-DZFP_ENABLE_PIC=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
	-DZFP_ENABLE_PIC=ON \
%if "%{tpls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
%endif
%endif
	-DCMAKE_BUILD_TYPE=Release \
%if "%{tpls_gpu}" == "cuda"
	-DZFP_WITH_CUDA=ON \
	-DCUDA_NVCC_EXECUTABLE=%{tpls_nvcc} \
	-DCUDA_NVCC_FLAGS=%{tpls_nvccflags} \
%else
	-DZFP_WITH_CUDA=OFF \
%endif


%make_build

%check
cd build
%make_build test

%install
cd build
%make_install

%files
%{tpls_prefix}/bin/zfp
%{tpls_prefix}/include/zfp.h
%{tpls_prefix}/include/zfp.hpp
%{tpls_prefix}/include/zfp
%{tpls_prefix}/lib/cmake/zfp
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libzfp.a
%else
%{tpls_prefix}/lib/libzfp.so
%{tpls_prefix}/lib/libzfp.so.*
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 1.0.1-1
- Initial Package


