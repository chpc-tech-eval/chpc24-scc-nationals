# This is for the RegCM Benchmark

# Building and Running RegCM

The model code is written in Fortran, utilizing features up to the 2008 standard. To compile the model, you will need:

- A working **Fortran compiler**
- **GNU Make**
- **Autotools** (autoconf, automake, libtool) to create the `configure` script

## Required Libraries

1. **HDF5**  
   - [Source Code](https://www.hdfgroup.org/downloads/hdf5/)  
   - Provided by The HDF Group, this library ensures long-term access and usability of HDF data, supporting users of HDF technologies.

2. **NetCDF**  
   - [NetCDF Downloads](https://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html)  
   - Essential for handling array-oriented scientific data, commonly used in climate and weather models.

3. **MPI**  
   - [OpenMPI](https://www.open-mpi.org/)  
   - Any MPI implementation will work, though OpenMPI is a popular choice.

## Obtaining the Code

The procedure to obtain the code is straightforward using Git:

```bash
git clone https://github.com/ICTP/RegCM.git
```
## Switching to the Target Branch
For ISC24, participants are requested to switch to the target branch:
```
cd RegCM
git checkout ISC24
```
## Creating the Configure Script
Once the model is on disk, you should create the configure script with the following command:
```
autoreconf -f -i
```
This command is also included in the bootstrap.sh script, which provides additional options if the autotools are installed in a non-standard path.

The generated configure script allows for various options to conditionally activate specific parts of the code, enable different I/O options, or optimize for HPC platforms that ICTP has supported over the years. Note that not all legacy platform/compiler combinations are still relevant, supported, or tested, especially if ICTP no longer has access to them.

## Setting the NetCDF Path
To avoid using an incorrect version of NetCDF, set the path to your NetCDF installation:
```
export PATH=<path to netcdf>/bin:$PATH
```
## Configuring the Build System
To configure the build system using the GNU Make program, you can simply type:
```
./configure
```
This should suffice on most systems.

## Configure Script Functionality

The `configure` script will (ideally) identify a compatible combination of the Fortran compiler and the required libraries. If the necessary libraries are not installed on the system but the user has access to a functioning compiler toolchain, an example script is available to download and install NetCDF and OpenMPI in user-accessible directories:

```bash
./Tools/Scripts/prereq_install.sh
```
## Compiling the Model Executables
To compile the model executables and copy them to the bin directory, ensure that the GNU Make program is in your path. You can then execute the following commands:
```
make version
make install
```
These commands will compile the model and install the necessary binaries as specified.

Here's the sample build script for LENGAU:
```
#!/bin/bash

# Source the Intel compiler and MPI environment variables

# Load Required Modules
module load chpc/parallel_studio_xe/2020u1
module load chpc/earth/netcdf/4.7.4/intel2020u1

# Define Paths
export REGCMDIR=/home/apps/chpc/earth/REGCM
export DIR=$REGCMDIR/LIBRARIES
export NETCDF=/apps/chpc/earth/NetCDF-c461-f444-intel2020

# Compiler Settings
export CC=icc
export CXX=icc
export FC=ifort
export F77=ifort

# Compiler Flags
export FCFLAGS="-m64 -I$DIR/netcdf/include -I$DIR/grib2/include"
export FFLAGS=$FCFLAGS
export CFLAGS=$FCFLAGS

# MPI Compilers
export MPICC=/apps/compilers/intel/parallel_studio_xe_2020_update1/compilers_and_libraries/linux/mpi/intel64/bin/mpicc
export MPIF90=/apps/compilers/intel/parallel_studio_xe_2020_update1/compilers_and_libraries/linux/mpi/intel64/bin/mpiifort
export MPIF77=$MPIF90

# Library Paths
export PKG_CONFIG_PATH=$DIR/grib2/lib/pkgconfig:$DIR/netcdf/lib/pkgconfig
export PATH=$NETCDF/bin:$DIR/grib2/bin:$PATH
export LD_LIBRARY_PATH=$DIR/grib2/lib:$NETCDF/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=$LIBRARY_PATH:$NETCDF/lib

# NetCDF and HDF5 Settings
export NETCDF_classic=1
export NETCDF4=1
export PNETCDF=$NETCDF
export HDF5=$NETCDF

# System Limits
ulimit -s unlimited
```



