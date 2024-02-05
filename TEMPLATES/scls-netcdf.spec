%define scls_oflags -O2

Name:           scls-%{scls_flavor}-netcdf
Version:        4.9.2
Release:        1%{?dist}
Summary:        Libraries for the Unidata network Common Data Form

License:        NetCDF
URL:            http://www.unidata.ucar.edu/software/netcdf/
Source0:        https://downloads.unidata.ucar.edu/netcdf-c/%{version}/netcdf-c-%{version}.tar.gz

BuildRequires:  scls-%{scls_flavor}-cmake
BuildRequires:  scls-%{scls_flavor}-hdf5

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

BuildRequires:  libcurl-devel
Requires:  libcurl
Requires:  scls-%{scls_flavor}-hdf5

%description
NetCDF (network Common Data Form) is an interface for array-oriented 
data access and a freely-distributed collection of software libraries 
for C, Fortran, C++, and perl that provides an implementation of the 
interface.  The NetCDF library also defines a machine-independent 
format for representing scientific data.  Together, the interface, 
library, and format support the creation, access, and sharing of 
scientific data. The NetCDF software was developed at the Unidata 
Program Center in Boulder, Colorado.

NetCDF data is: 

   o Self-Describing: A NetCDF file includes information about the
     data it contains.

   o Network-transparent:  A NetCDF file is represented in a form that
     can be accessed by computers with different ways of storing
     integers, characters, and floating-point numbers.

   o Direct-access:  A small subset of a large dataset may be accessed
     efficiently, without first reading through all the preceding
     data.

   o Appendable:  Data can be appended to a NetCDF dataset along one
     dimension without copying the dataset or redefining its
     structure. The structure of a NetCDF dataset can be changed,
     though this sometimes causes the dataset to be copied.

   o Sharable:  One writer and multiple readers may simultaneously
     access the same NetCDF file.


%prep
%setup -q -n netcdf-c-%{version}

%build
%{expand: %setup_scls_env}

mkdir build && cd build
%{scls_env} \
%{scls_cmake} \
	-DCMAKE_C_AR=%{scls_ar} \
    -DCMAKE_C_COMPILER=%{scls_mpicc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
    -DMPIEXEC_EXECUTABLE=%{scls_mpiexec} \
	-DENABLE_DAP=OFF \
	-DENABLE_DAP2=OFF \
	-DENABLE_DAP4=OFF \
	-DENABLE_EXAMPLES=OFF \
	-DENABLE_HDF4=OFF \
	-DENABLE_HDF5=ON \
	-DENABLE_LIBXML2=OFF \
	-DENABLE_DISKLESS=OFF \
	-DENABLE_PLUGINS=OFF \
	-DENABLE_NCZARR=OFF \
	-DENABLE_FILTER_TESTING=OFF \
	-DHDF5_C_COMPILER_EXECUTABLE=%{scls_prefix}/bin/h5cc \
	-DHDF5_C_INCLUDE_DIR=%{scls_prefix}/include \
	-DHDF5_DIFF_EXECUTABLE=%{scls_prefix}/bin/h5diff \
	-DHDF5_DIR=%{scls_prefix} \
%if "%{scls_libs}" == "static"
	-DHDF5_hdf5_LIBRARY_RELEASE=%{scls_prefix}/lib/libhdf5.a \
	-DHDF5_hdf5_hl_LIBRARY_RELEASE=%{scls_prefix}/lib/libhdf5_hl.a \
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DHDF5_hdf5_LIBRARY_RELEASE=%{scls_prefix}/lib/libhdf5.so \
	-DHDF5_hdf5_hl_LIBRARY_RELEASE=%{scls_prefix}/lib/libhdf5_hl.so \
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%if "%{scls_compiler}" == "intel"
%if "%{scls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mpiproot}/lib -Wl,-rpath,%{scls_mpiproot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_mpiproot}/lib -Wl,-rpath,%{scls_mpiroot}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif	
%endif
	..

%make_build

#%check
#cd build
#%if "%{scls_compiler}" == "intel"
#%if "%{scls_mpi}" == "intelmpi"
#LD_LIBRARY_PATH="%{scls_prefix}/lib:%{scls_mpiroot}/lib:%{scls_comproot}/lib"  %make_build test
#%else
#LD_LIBRARY_PATH="%{scls_prefix}/lib:%{scls_comproot}/lib"  %make_build test
#%endif
#%else
#LD_LIBRARY_PATH="%{scls_prefix}/lib"  %make_build test
#%endif

%install
cd build
%make_install
 
%files
%{scls_prefix}/bin/nc-config
%{scls_prefix}/bin/nccopy
%{scls_prefix}/bin/ncdump
%{scls_prefix}/bin/ncgen
%{scls_prefix}/bin/ncgen3
%{scls_prefix}/include/netcdf.h
%{scls_prefix}/include/netcdf_aux.h
%{scls_prefix}/include/netcdf_dispatch.h
%{scls_prefix}/include/netcdf_filter.h
%{scls_prefix}/include/netcdf_filter_build.h
%{scls_prefix}/include/netcdf_json.h
%{scls_prefix}/include/netcdf_mem.h
%{scls_prefix}/include/netcdf_meta.h
%{scls_prefix}/include/netcdf_par.h
%{scls_prefix}/lib/cmake/netCDF
%{scls_prefix}/lib/libnetcdf.settings
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libnetcdf.a
%else
%{scls_prefix}/lib/libnetcdf.so
%{scls_prefix}/lib/libnetcdf.so.*
%endif
%{scls_prefix}/lib/pkgconfig/netcdf.pc
%{scls_prefix}/share/man/man1/nccopy.1
%{scls_prefix}/share/man/man1/ncdump.1
%{scls_prefix}/share/man/man1/ncgen.1
%{scls_prefix}/share/man/man1/ncgen3.1
%{scls_prefix}/share/man/man3/netcdf.3

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 4.9.2-1
- Initial Package
