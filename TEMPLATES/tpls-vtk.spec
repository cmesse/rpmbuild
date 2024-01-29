
%global vtk_major 9
%global vtk_minor 3
%global vtk_patch 0

Name:           tpls-%{tpls_flavor}-vtk
Version:        %{vtk_major}.%{vtk_minor}.%{vtk_patch}
Release:        1%{?dist}
Summary:        The Visualization Toolkit - A high level 3D visualization library

License:        BSD-3-Clause
URL:            https://vtk.org/
Source0:        Source0: https://www.vtk.org/files/release/VTK-%{vtk_major}.%{vtk_minor}/VTK-%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake

%if   "%{tpls_mpi}" == "openempi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
BuildRequires:  intel-oneapi-mpi
%endif

BuildRequires:  libXcursor-devel
BuildRequires:  libXext-devel

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

AutoReqProv:    %{tpls_auto_req_prov}

%prep
%setup -q -n VTK-%{version}

%build

%{expand: %setup_tpls_env}

mkdir build && cd build
%{tpls_env} \
%{tpls_cmake} .. \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
%endif
	-DCMAKE_BUILD_TYPE=Release \
	-DVTK_BUILD_DOCUMENTATION=OFF \
	-DVTK_BUILD_EXAMPLES=OFF \
	-DVTK_BUILD_SCALED_SOA_ARRAYS=OFF \
	-DVTK_BUILD_SPHINX_DOCUMENTATION=OFF \
%if "%{tpls_gpu}" == "cuda"
	-DVTK_USE_CUDA=ON \
%else
	-DVTK_USE_CUDA=OFF \
%endif
	-DVTK_SMP_IMPLEMENTATION_TYPE=OpenMP \
	-DVTK_USE_MPI=ON \
	-DVTK_WRAP_JAVA=OFF \
	-DVTK_WRAP_PYTHON=OFF
	
	

make %{?_smp_mflags}

%install
cd build && %make_install
%{tpls_remove_la_files}



%files
%{tpls_prefix}/bin/vtk*
%{tpls_prefix}/include/vtk-%{vtk_major}.%{vtk_minor}
%{tpls_prefix}/lib/cmake/vtk-%{vtk_major}.%{vtk_minor}
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libvtk*.a
%else
%{tpls_prefix}/lib/libvtk*.so
%{tpls_prefix}/lib/libvtk*.so.*
%endif
%{tpls_prefix}/share/vtk-%{vtk_major}.%{vtk_minor}
%{tpls_prefix}/share/licenses/VTK
%{tpls_prefix}/lib/vtk-%{vtk_major}.%{vtk_minor}/hierarchy/VTK

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 9.3.0
- Initial Package
