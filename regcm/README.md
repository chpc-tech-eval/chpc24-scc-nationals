# RegCM-Lengau-SCC-Nationals 2024

# Building and Running the Model on LENGAU

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
https://github.com/ICTP/RegCM/projects?query=is%3Aopen
```

## Untar the tarball
```
tar -zxvf 5.0.0.tar.gz
```

## Create the Configure Script
Once the model is on disk, you should create the configure script with the following command:
```
./bootstrap.sh
```
The generated configure script allows for various options to conditionally activate specific parts of the code, enable different I/O options, or optimize for HPC platforms.

## Setting the NetCDF Path
To avoid using an incorrect version of NetCDF, set the path to your NetCDF installation:
```
export PATH=<path to netcdf>/bin:$PATH
```
## Configuring the Build System
To configure the build system using the GNU Make program, you can simply type:
```
./configure --with-netcdf 
```
This should suffice on most systems.

## Build the Model Executables
To compile the model executables and copy them to the bin directory, ensure that the GNU Make program is in your path. You can then execute the following commands:
```
make -j 4  #Adjust number of cores as needed
make install
```
These commands will compile the model and install the necessary binaries as specified. If all goes well then congratulations! You can now go to next step and run a simulation. 

Here's the sample build script for LENGAU:
```
#!/bin/bash

# Source the Intel compiler and MPI environment variables

# Load Required Modules
module load chpc/parallel_studio_xe/2020u1
module load chpc/earth/netcdf/4.7.4/intel2020u1

# Define Paths
export NETCDF=/apps/chpc/earth/NetCDF-c461-f444-intel2020

# Compiler Settings
export CC=icc
export CXX=icc
export FC=ifort

# Compiler Flags
export FCFLAGS="-m64 -I$DIR/netcdf/include -I$DIR/grib2/include"
export FFLAGS=$FCFLAGS
export CFLAGS=$FCFLAGS

# MPI Compilers
export MPICC=/apps/compilers/intel/parallel_studio_xe_2020_update1/compilers_and_libraries/linux/mpi/intel64/bin/mpicc
export MPIF90=/apps/compilers/intel/parallel_studio_xe_2020_update1/compilers_and_libraries/linux/mpi/intel64/bin/mpiifort

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
## Access global datasets

The first step to run a test simulation is to obtain static data to localize model DOMAIN and Atmosphere and Ocean global model dataset to build initial and boundary conditions ICBC to run a local area simulation. ICTP maintains a public accessible web repository of datasets on: http://users.ictp.it/pubregcm/RegCM4/globedat.htm
As of now you are requested to download required global data on your local disk storage before any run attempt. In the future, the ICTP ESP team has planned to make available an OpenDAP THREDDS Server to give remote access to global dataset for creating DOMAIN and ICBC without the need to download the global dataset, but just the required subset in space and time, using the ICTP web server capabilities to create that subset. 

1. **Global dataset directory layout**  
```
export ICTP_DATASITE=http://clima-dods.ictp.it/regcm4
```
The command sets the environment variable ```ICTP_DATASITE``` to the ```URL http://clima-dods.ictp.it/regcm4```. This environment variable is likely used by the RegCM model or related scripts to locate specific datasets or resources hosted at the ICTP (International Centre for Theoretical Physics) data site. By setting this variable, scripts or applications running RegCM can dynamically reference this URL to download or access required data files without needing hard-coded paths in each script. This setup is particularly useful for automating data access in simulations that require large datasets stored on remote servers.

```
cd $REGCM_GLOBEDAT
$> mkdir SURFACE CLM SST AERGLOB EIN15
```
You are suggested to establish a convenient location for global datasets on your local storage. Keep in mind that required space for a year of global data can be as large as 8 GBytes.

2. **Static Surface Dataset**

The model needs to be localized on a particular DOMAIN. The needed information are topography, land type classification and optionally lake depth (to run the Hostetler lake model) and soil texture classification (to run the chemistry option with DUST enabled). This means downloading four files, which are global archives at 30second horizontal resolution on a global latitude-longitude grid of the above data.
```
cd $REGCM_GLOBEDAT
cd SURFACE
cd $REGCM_GLOBEDAT
cd SURFACE
curl -o GTOPO_DEM_30s.nc ${ICTP_DATASITE}/SURFACE/GTOPO_DEM_30s.nc
curl -o GLCC_BATS_30s.nc ${ICTP_DATASITE}/SURFACE/GLCC_BATS_30s.nc
curl -o GLZB_SOIL_30s.nc ${ICTP_DATASITE}/SURFACE/GLZB_SOIL_30s.nc
```
3. **Sea Surface Temperature**

The model needs a global SST dataset to feed the model with ocean temperature. You have multiple choices for
SST data, but we will for now for our test run download just CAC OISST weekly for the period 1981 - present.
```
cd $REGCM_GLOBEDAT
cd SST
CDCSITE="ftp.cdc.noaa.gov/pub/Datasets/noaa.oisst.v2"
curl -o sst.wkmean.1981-1989.nc \
> ftp://$CDCSITE/sst.wkmean.1981-1989.nc
curl -o sst.wkmean.1990-present.nc \
> ftp://$CDCSITE/sst.wkmean.1990-present.nc
```
4. **Atmosphere and Land temperature Global Dataset**
The model needs to build initial and boundary conditions for the regional scale, interpolating on the RegCM grid the data from a Global Climatic Model output. The GCM dataset can come from any of the supported models, but we will for now for our test run download just the EIN15 dataset for the year 1990 (Jan 01 00:00:00 UTC to Dec 31 18:00:00 UTC)
```
cd $REGCM_GLOBEDAT
cd EIN15
mkdir 1990
cd 1990
for type in air hgt rhum uwnd vwnd; do  
  for hh in 00 06 12 18; do  
    curl -o "${type}.1990.${hh}.nc" "${ICTP_DATASITE}/EIN15/1990/${type}.1990.${hh}.nc"
  done
done
```
With these datasets, we are now ready to go through the RegCM Little Tutorial in the next chapter of this User Guide.


