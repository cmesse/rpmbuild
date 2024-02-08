#/usr/bin/env python3
import os
import sys
import yaml


def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def flavor(config):
    flavor_order = ['host','compiler','mpi', 'math' ]

    flav =  '-'.join([str(config['flavor'][key]) for key in flavor_order])


    libs = config['flavor']['libs']

    if libs == "static":
        flav = "{:s}-static".format(flav)


    int = config['flavor']['int']

    if int == "64" :
        flav = "{:s}-ilp64".format(flav)
    return flav

def prefix(config):
    return '/opt/scls/{:s}'.format( flavor(config) )

def ld_library_path(config):
    path = '{:s}/lib'.format( prefix(config) )
    math = str(config['flavor']['math'])
    compiler = str(config['flavor']['compiler'])
	
    if math != 'lapack' :
        path += ':{:s}/lib'.format( mklroot( config ) )
    if math == 'cuda' :

        cudaver = str( str(config['system']['cuda']))

        cuda = '/opt/nvidia/hpc_sdk/Linux_x86_64/{:s}/cuda'.format( str( cudaver ) )
        math = '/opt/nvidia/hpc_sdk/Linux_x86_64/{:s}/math_libs'.format(str(cudaver))

        path += ':{:s}/lib64'.format(cuda)
        path += ':{:s}/lib64'.format(math)

    if compiler != "gnu" :
        path += ':{:s}/lib'.format(config['system']['comp'])
		
    return path

def omplib(config):
    compiler = str(config['flavor']['compiler'])
    comproot = str(config['system']['comp'])
    libs     = str(config['flavor']['libs'])

    if compiler == 'gnu':
        return ' -lgomp'
    elif compiler == 'nvidia':
        return ' -mp'
    elif libs == 'static' :
        return '{:s}/lib/libiomp5.a'.format( comproot )
    else:
        return '{:s}/lib/libiomp5.so'.format(comproot)

def ompflag(config):
    compiler = str(config['flavor']['compiler'])
    comproot = str(config['system']['comp'])

    if compiler == 'gnu':
        return ' -fopenmp'
    elif compiler == 'nvidia':
        return ' -mp'
    else:
        return ' -qopenmp'.format(comproot)

def mklroot(config):
    return str(config['system']['mkl'])
    
def mpiroot(config):
    return str(config['system']['mpi'])

def mkl_scalapack(config):
    if int(config['flavor']['int']) == 32 :
        return 'mkl_scalapack_lp64'
    else:
        return 'mkl_scalapack_ilp64'


def mkl_intel(config):
    if int(config['flavor']['int']) == 32 :
        return 'mkl_intel_lp64'
    else:
        return 'mkl_intel_ilp64'


def mkl_thread(config):
    compiler = str(config['flavor']['compiler'])
    if compiler == 'gnu':
        return 'mkl_gnu_thread'
    elif compiler == 'nvidia':
        return 'mkl_pgi_thread'
    else:
        return 'mkl_intel_thread'


def mkl_blacs(config):
    intsize = int(config['flavor']['int'])
    mpi = str(config['flavor']['mpi'])

    if mpi == 'openmpi' :
        if intsize == 32 :
            return 'mkl_blacs_openmpi_lp64'
        else:
            return 'mkl_blacs_openmpi_ilp64'
    else:
        if intsize == 32 :
            return 'mkl_blacs_intelmpi_lp64'
        else:
            return 'mkl_blacs_intelmpi_ilp64'


def mkl_linker_flags( config ) :
    libs  = str(config['flavor']['libs'])
    pref = mklroot(config)
    if libs == 'static':
        return ' -Wl,--start-group {:s}/lib/lib{:s}.a {:s}/lib/lib{:s}.a {:s}/lib/libmkl_core.a -Wl,--end-group {:s} -lpthread -lm -ldl'.format(
            pref,mkl_intel(config), pref,mkl_thread(config),pref,omplib(config) )
    else:
        return '-l{:s} -l{:s} -lmkl_core {:s}  -lpthread -lm -ldl'.format(
            mkl_intel(config), mkl_thread(config),omplib(config) )


def mkl_mpi_linker_flags( config ) :
    libs  = str(config['flavor']['libs'])
    pref = mklroot(config)
    if libs == 'static':
        return '{:s}/lib/lib{:s}.a  -Wl,--start-group {:s}/lib/lib{:s}.a {:s}/lib/lib{:s}.a {:s}/lib/libmkl_core.a -Wl,--end-group {:s}/lib/lib{:s}.a {:s} -lpthread -lm -ldl'.format(
            pref,mkl_scalapack(config),pref,mkl_intel(config), pref,mkl_thread(config),pref,pref,mkl_blacs(config), omplib(config) )
    else:
        return '-l{:s} -l{:s} -l{:s} -lmkl_core -l{:s} {:s} -lpthread -lm -ldl'.format(
            mkl_scalapack(config), mkl_intel(config), mkl_thread(config), mkl_blacs(config), omplib(config) )


def write_flavor(file, config):
    file.write('#######################################################################\n')
    file.write('# FLAVOR SPECIFIC DEFINES                                             #\n')
    file.write('#######################################################################\n\n')
    file.write('%define scls_flavor {:s}\n\n'.format(flavor(config)))
    file.write('%define scls_host {:s}\n'.format(str(config['flavor']['host'])))
    file.write('%define scls_compiler {:s}\n'.format(str(config['flavor']['compiler'])))
    file.write('%define scls_mpi {:s}\n'.format(str(config['flavor']['mpi'])))
    file.write('%define scls_math {:s}\n'.format(str(config['flavor']['math'])))
    file.write('%define scls_libs {:s}\n'.format(str(config['flavor']['libs'])))
    file.write('%define scls_index_size {:s}\n'.format(str(config['flavor']['int'])))
    file.write('%define scls_comp_minver {:s}\n\n'.format(str(config['rpm']['version'])))
    file.write('%define scls_rpm_cc {:s}\n'.format(str(config['rpm']['cc'])))
    file.write('%define scls_rpm_cxx {:s}\n'.format(str(config['rpm']['cxx'])))
    file.write('%define scls_rpm_fc {:s}\n'.format(str(config['rpm']['fc'])))

    if  bool(config['rpm']['auto_req_prov']) :
        file.write('%define scls_auto_req_prov yes\n')
    else:
        file.write('%define scls_auto_req_prov no\n')

def write_paths(file, config):

    cuda = str(config['system']['cuda'])

    file.write('\n# important paths\n')

    file.write('%define scls_prefix {:s}\n'.format(prefix(config)))
    file.write('%define scls_includes {:s}/includes\n'.format(prefix(config)))
    file.write('%define scls_libdir {:s}/lib\n'.format(prefix(config)))

    file.write('%define scls_comproot {:s}\n'.format( str(config['system']['comp'])) )
    file.write('%define scls_mklroot  {:s}\n'.format(str(config['system']['mkl'])))
    file.write('%define scls_cuda      /opt/nvidia/hpc_sdk/Linux_x86_64/{:s}/cuda\n'.format(str(cuda)))
    file.write('%define scls_cudamath  /opt/nvidia/hpc_sdk/Linux_x86_64/{:s}/math_libs\n'.format(str(cuda)))
    file.write('%define scls_cuda_version  {:s}\n'.format(str(cuda).replace('.', '-')))
    file.write('%define scls_cuda_architectures  50;52;53;60;61;62;70;72;75;80;86;87;90\n')
    file.write('%define scls_cuda_arch           50,52,53,60,61,62,70,72,75,80,86,87,90\n')
    file.write('%define scls_ld_library_path  {:s}\n'.format(ld_library_path(config)))

def write_binaries(file,config):
    file.write('\n# compiler executables\n')
    binaries = ['cc', 'cxx', 'fc', 'ar', 'ld' ]
    for key in binaries:
        file.write('%define scls_{:s} {:s}\n'.format( key, str(config['binaries'][key] ) ) )

    file.write('%define scls_cpp {:s} -E\n'.format( key, str(config['binaries']['cc'] ) ) )
    file.write('%define scls_cxxcpp {:s} -E\n'.format( key, str(config['binaries']['cxx'] ) ) )

def write_mpi_binaries(file,config):
    file.write('\n# MPI wrappers\n')
    libs = str(config['flavor']['libs'])
    mpi = str(config['flavor']['mpi'])
    if mpi == 'intelmpi' :
        pref = mpiroot(config)
        file.write('%define scls_mpicc   {:s}/bin/mpiicx\n'.format(pref ))
        file.write('%define scls_mpicxx  {:s}/bin/mpiicpx\n'.format(pref))
        file.write('%define scls_mpifort {:s}/bin/mpiifx\n'.format(pref))
        file.write('%define scls_mpiroot {:s}\n'.format(pref))
        file.write('%define scls_mpiexec {:s}/bin/mpiexec.hydra\n'.format(pref))

    else:
        pref= prefix( config )
        file.write('%define scls_mpicc   {:s}/bin/mpicc\n'.format(pref ))
        file.write('%define scls_mpicxx  {:s}/bin/mpicxx\n'.format(pref))
        file.write('%define scls_mpifort {:s}/bin/mpifort\n'.format(pref))
        file.write('%define scls_mpiroot {:s}\n'.format(pref))
        file.write('%define scls_mpiexec {:s}/bin/mpiexec\n'.format(pref))

        # Define library types and their extensions based on 'libs'
        lib_ext = '.a' if libs == 'static' else '.so'
        lib_separator = ';'  # Separator used in defining scls_mpilib

        # Define libraries based on 'mpi'
        if mpi == "mpich":
            lib_names = ['libmpicxx', 'libmpifort', 'libmpi']
        else:  # Assuming the else condition is meant for another MPI implementation
            lib_names = ['libmpi_usempif08', 'libmpi_usempi_ignore_tkr', 'libmpi_mpifh', 'libmpi']

        # Build the library paths
        lib_paths = ['{:s}/lib/{:s}{:s}'.format(pref, lib_name, lib_ext) for lib_name in lib_names]

        # Write to file
        file.write('%define scls_mpilibs ' + ' '.join(lib_paths) + '\n')
        file.write('%define scls_mpilib ' + lib_separator.join(lib_paths) + '\n')


def write_compiler_flags( file, config ):
    file.write('\n# Compiler Flags\n')
    # flavor information
    host     = str(config['flavor']['host'])
    compiler = str(config['flavor']['compiler'])
    math      = str(config['flavor']['math'])
    libs     = str(config['flavor']['libs'])
    intsize  = int(config['flavor']['int'])

    # baseflags
    cflags   = str(config['flags']['cc'])
    cxxflags = str(config['flags']['cxx'])
    fcflags  = str(config['flags']['fc'])


    # check if we are building shared libraries
    if libs == 'shared' :
        cflags   += ' -fPIC'
        cxxflags += ' -fPIC'
        fcflags  += ' -fPIC'

    # add the architecture
    cflags   += ' -mtune={:s}'.format(host)
    cxxflags += ' -mtune={:s}'.format(host)
    fcflags  += ' -mtune={:s}'.format(host)

    # check for the MKL interface flag
    if math != 'lapack' and intsize == 64 :
        cflags += ' -DMKL_ILP64'
        cxxflags += ' -DMKL_ILP64'
        fcflags += ' -DMKL_ILP64'

    # special fortran settings
    if compiler == 'gnu' :
        # add 64 bit flag for the x86_64 architecture
        cflags += ' -m64'
        cxxflags += ' -m64'
        fcflags += ' -m64'
        if intsize  == 64 :
            fcflags += ' -fdefault-integer-8'
    else: # for both intel and nvidia compiler
        if intsize == 32 :
            fcflags += ' -i4'
        else:
            fcflags += ' -i8'

    # create the includes
    includes = ' -I{:s}/include'.format( prefix( config ))

    # the ld flags
    ldflags = ' -L{:s}/lib'.format(prefix(config))
    rpath   = ' -Wl,-rpath,{:s}/lib'.format(prefix(config))

    # check if we add the mkl includes
    if math != 'lapack' :
        mkl = mklroot( config )
        includes += ' -I{:s}/include'.format( mkl )
        ldflags += ' -L{:s}/lib'.format( mkl )
        rpath += ' -Wl,-rpath,{:s}/lib'.format(mkl)

    if math == 'cuda' :
        cudaver = str( str(config['system']['cuda']))

        cuda = '/opt/nvidia/hpc_sdk/Linux_x86_64/{:s}/cuda'.format( str( cudaver ) )
        math = '/opt/nvidia/hpc_sdk/Linux_x86_64/{:s}/math_libs'.format(str(cudaver))

        includes += ' -I{:s}/include -I{:s}/include'.format(cuda, math )
        ldflags += ' -L{:s}/lib64 -L{:s}/lib64'.format( cuda, math )
        rpath += ' -Wl,-rpath,{:s}/lib64 -Wl,-rpath,{:s}/lib64'.format( cuda, math )
        file.write('%define scls_nvcc   {:s}/bin/nvcc\n'.format( cuda ) )
        file.write('%define scls_nvccflags  -I{:s}/include -I{:s}/include -I{:s}/include\n'.format(prefix( config ), cuda, math ))

    if libs == 'shared' :
        ldflags += ' {:s}'.format( rpath )
    else:
        # for hwloc
        ldflags += ' -lpciaccess'
    
    # add includes to the flags
    cflags   += includes
    cxxflags += includes
    fcflags  += includes

    # write the flags
    file.write('%define scls_cflags    {:s}\n'.format( cflags ))
    file.write('%define scls_cxxflags  {:s}\n'.format(cxxflags))
    file.write('%define scls_fcflags   {:s}\n'.format(fcflags))
    file.write('%define scls_ldflags   {:s}\n'.format(ldflags))
    file.write('%define scls_arflags   {:s}\n'.format(str(config['flags']['ar'])))
    file.write('%define scls_ompflag   {:s}\n'.format(ompflag(config)))
def write_netlib(file,config) :
    file.write('\n# the netlib reference implementations\n')
    libs  = str(config['flavor']['libs'])
    if libs == 'static' :
        blas  = '{:s}/lib/libblas.a'.format(prefix( config ))
        lapack = '{:s}/lib/liblapack.a'.format(prefix(config))
        scalapack = '{:s}/lib/libscalapack.a'.format(prefix(config))
    else:
        blas  = '{:s}/lib/libblas.so'.format(prefix( config ))
        lapack = '{:s}/lib/liblapack.so'.format(prefix(config))
        scalapack = '{:s}/lib/libscalapack.so'.format(prefix(config))

    file.write('%define scls_blas   {:s}\n'.format(blas))
    file.write('%define scls_lapack  {:s}\n'.format(lapack))
    file.write('%define scls_scalapack {:s}\n'.format(scalapack))

def write_mkl(file,config) :
    file.write('\n# the MKL setup\n')
    file.write('%define scls_mkl_linker_flags   {:s}\n'.format(mkl_linker_flags(config)))
    file.write('%define scls_mkl_mpi_linker_flags  {:s}\n'.format(mkl_mpi_linker_flags(config)))


def write_libs(file, config):
    lib_type = 'a' if config['flavor']['libs'] == 'static' else 'so'
    prefix_path = prefix(config)
    libs = ['arpack', 'sbutterflypack', 'dbutterflypack', 'cbutterflypack', 'zbutterflypack', 'parpack', 'superlu', 'parmetis', 'metis', 'zfp', 'ptscotch', 'ptscotcherr', 'ptscotcherrexit',  'scotch', 'scotcherr', 'scotcherrexit', 'slate', 'suitesparse', 'strumpack' ]

    for lib in libs:
        lib_path = f"{prefix_path}/lib/lib{lib}.{lib_type}"
        file.write(f'%define scls_{lib} {lib_path}\n')



def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_yaml_file>")
        sys.exit(1)

    yaml_file =  os.path.expanduser("~") + '/rpmbuild/PYTHON/' + sys.argv[1] + '.yaml' # Get YAML file path from command-line argument
    output_file = '.sclsmacros'  # Output file name
    config = read_yaml(yaml_file)

    # write the configuration
    with open(output_file, 'w') as file:
        write_flavor(file, config)
        write_paths(file, config)
        write_binaries(file, config)
        write_mpi_binaries(file, config)
        write_compiler_flags(file, config)
        write_netlib(file, config)
        write_mkl(file, config)
        write_libs(file, config)

if __name__ == '__main__':
    main()
