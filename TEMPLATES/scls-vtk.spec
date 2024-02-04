%define scls_oflags -O2

%global vtk_major 9
%global vtk_minor 3
%global vtk_patch 0

Name:           scls-%{scls_flavor}-vtk
Version:        %{vtk_major}.%{vtk_minor}.%{vtk_patch}
Release:        1%{?dist}
Summary:        The Visualization Toolkit - A high level 3D visualization library

License:        BSD-3-Clause
URL:            https://vtk.org/
Source0:        Source0: https://www.vtk.org/files/release/VTK-%{vtk_major}.%{vtk_minor}/VTK-%{version}.tar.gz

BuildRequires:  scls-%{scls_flavor}-cmake


BuildRequires:  libXcursor-devel
BuildRequires:  libXext-devel

%if "%{scls_math}" == "cuda"
BuildRequires: nvhpc-%{scls_cuda_version}
BuildRequires: nvhpc-%{scls_cuda_version}-cuda-multi
Requires:      nvhpc-%{scls_cuda_version}
Requires:      nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).



%prep
%setup -q -n VTK-%{version}

%build

%{expand: %setup_scls_env}

mkdir build && cd build
%{scls_env} \
%if "%{scls_math}" == "cuda"
%if "%{scls_libs}" == "static"
LDFLAGS+=" -L%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64" \
%else
LDFLAGS+=" -L%{scls_cudamath}/lib64 -Wl,-rpath,%{scls_cudamath}/lib64 -L%{scls_cuda}/lib64 -Wl,-rpath,%{scls_cuda}/lib64" \
%endif
%endif
%{scls_cmake} \
    -DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
%endif
	-DCMAKE_BUILD_TYPE=Release \
	-DVTK_BUILD_DOCUMENTATION=OFF \
	-DVTK_BUILD_EXAMPLES=OFF \
	-DVTK_BUILD_SCALED_SOA_ARRAYS=OFF \
	-DVTK_BUILD_SPHINX_DOCUMENTATION=OFF \
%if "%{scls_math}" == "cuda"
	-DVTK_USE_CUDA=ON \
    -DCMAKE_CUDA_COMPILER=%{scls_nvcc} \
    -DCMAKE_CUDA_FLAGS="%{scls_nvccflags}" \
	-DCMAKE_CUDA_ARCHITECTURES="%{scls_cuda_architectures}" \
%else
	-DVTK_USE_CUDA=OFF \
%endif
	-DVTK_SMP_IMPLEMENTATION_TYPE=OpenMP \
	-DVTK_USE_MPI=OFF \
	-DVTK_WRAP_JAVA=OFF \
	-DVTK_WRAP_PYTHON=OFF \
	..
	
	

make %{?_smp_mflags}

%install
cd build && %make_install
%{scls_remove_la_files}



%files
%{scls_prefix}/bin/vtk*
%{scls_prefix}/include/vtk-%{vtk_major}.%{vtk_minor}
%{scls_prefix}/lib/cmake/vtk-%{vtk_major}.%{vtk_minor}
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libvtk*.a
%else
%{scls_prefix}/lib/libvtk*.so
%{scls_prefix}/lib/libvtk*.so.*
%endif
%{scls_prefix}/share/vtk-%{vtk_major}.%{vtk_minor}
%{scls_prefix}/share/licenses/VTK
%{scls_prefix}/lib/vtk-%{vtk_major}.%{vtk_minor}/hierarchy/VTK

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 9.3.0-1
- Initial Package
