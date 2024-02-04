%define scls_oflags -O3

Name:           scls-%{scls_flavor}-zfp
Version:        1.0.1
Release:        1%{?dist}
Summary:        Library for compressed numerical arrays with high throughput R/W random access

License:        BSD-3-Clause
URL:            https://computation.llnl.gov/projects/floating-point-compression
Source0:        https://github.com/LLNL/zfp/archive/%{version}/zfp-%{version}.tar.gz
Patch0:         zfp_no_cuda_version_check.patch

BuildRequires:  scls-%{scls_flavor}-cmake

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

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
%{scls_env} \
%{scls_cmake} .. \
    -DCMAKE_C_COMPILER_AR=%{scls_ar} \
    -DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
	-DZFP_ENABLE_PIC=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
	-DZFP_ENABLE_PIC=ON \
%if "%{scls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif
%endif
	-DCMAKE_BUILD_TYPE=Release \
%if "%{scls_math}" == "cuda"
	-DZFP_WITH_CUDA=ON \
	-DCUDA_NVCC_EXECUTABLE=%{scls_nvcc} \
%if "%{scls_compiler}" == "intel"
	-DCUDA_NVCC_FLAGS="%{scls_nvccflags} -allow-unsupported-compiler" \
%else
	-DCUDA_NVCC_FLAGS="%{scls_nvccflags}" \
%endif
	-DCMAKE_CUDA_ARCHITECTURES="50;52;53;60;61;62;70;72;75;80;86;87;90" \
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
%{scls_prefix}/bin/zfp
%{scls_prefix}/include/zfp.h
%{scls_prefix}/include/zfp.hpp
%{scls_prefix}/include/zfp
%{scls_prefix}/lib/cmake/zfp
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libzfp.a
%else
%{scls_prefix}/lib/libzfp.so
%{scls_prefix}/lib/libzfp.so.*
%endif

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 1.0.1-1
- Initial Package


