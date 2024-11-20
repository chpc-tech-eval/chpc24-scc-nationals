MATLAB
======

[MATLAB](https://www.mathworks.com/products/matlab.html) _(**MAT**rix **LAB**oratory)_ is a proprietary multi-paradigm programming language and numeric computing environment developed by [MathWorks](https://www.mathworks.com/). MATLAB allows matrix manipulations, plotting of functions and data, implementation of algorithms, creation of user interfaces, and interfacing with programs written in other languages.

This project forms part of the CHPC Student Cluster competition, where participants will apply Parallel computing techniques in the MATLAB environment to speed up their code execution. This problem has been put forward as part of a collaboration between MathWorks, Opti-Num Solutions and the CHPC.

# Installation Instructions

Team Captains have been provided with the URL, Activation Key and Licensing information required to download, install and activate their MATLAB deployments.

1. Use the link provided to navigate to the MATLAB CHPC Workshop Workspace:
   <p align="center"><img alt="Matlab CHPC Workshop Workspace" src="./resources/chpc_matlab_workshop.png" width=600 /></p>

1. Download the 2024B Installation files for Linux:
   <p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/chpc_matlab_linux_2024b.png" width=600 /></p>

1. Copy the files over to your cluster:
   * You can use either [WireGuard](https://github.com/chpc-tech-eval/scc/tree/main/tutorial2#wirguard-vpn-cluster-access) or [ZeroTier](https://github.com/chpc-tech-eval/scc/tree/main/tutorial2#zerotier) as described in the Selection Round content.
   * Alternatively you can use `scp` to transfer the files over `SSH`:
     ```bash
     scp -i <PATH-TO-SSH-KEY> <PATH-TO-MATLAB>/matlab_R2024b_Linux.zip <USER>@<DESTINATION_IP>:<DESTINATION_PATH>
     ```
1. From your **head node** server, `unzip` the MATLAB `.zip` file:
   ```bash
   mkdir <DEST_DIR>

   # Ensure that you system has an appropriate package install to run the unzip program of similar.
   unzip matlab_R2024b_Linux.zip -d <DEST_DIR>
   ```
1. Install all of the [dependencies](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/ubuntu24.04/base-dependencies.txt) required to run the MATLAB installer:
   * DNF / YUM
     ```bash
     # RHEL, Rocky, Alma, CentOS Stream
     sudo dnf install alsa-lib.x86_64 cairo.x86_64 cairo-gobject.x86_64 cups-libs.x86_64 gdk-pixbuf2.x86_64 glib2.x86_64 glibc.x86_64 glibc-langpack-en.x86_64 glibc-locale-source.x86_64 gtk3.x86_64 libICE.x86_64 libXcomposite.x86_64 libXcursor.x86_64 libXdamage.x86_64 libXfixes.x86_64 libXft.x86_64 libXinerama.x86_64 libXrandr.x86_64 libXt.x86_64 libXtst.x86_64 libXxf86vm.x86_64 libcap.x86_64 libdrm.x86_64 libglvnd-glx.x86_64 libsndfile.x86_64 libtool-ltdl.x86_64 libuuid.x86_64 libwayland-client.x86_64 make.x86_64 mesa-libgbm.x86_64 net-tools.x86_64 nspr.x86_64 nss.x86_64 nss-util.x86_64 pam.x86_64 pango.x86_64 procps-ng.x86_64 sudo.x86_64 unzip.x86_64 which.x86_64 zlib.x86_64
     ```
   * APT
     ```bash
     # Debian, Ubuntu
     sudo apt install alsa-lib cairo cairo-gobject cups-libs gdk-pixbuf2 glib2 glibc glibc-langpack-en glibc-locale-source gtk3 libICE libXcomposite libXcursor libXdamage libXfixes libXft libXinerama libXrandr libXt libXtst libXxf86vm libcap libdrm libglvnd-glx libsndfile libtool-ltdl libuuid libwayland-client make mesa-libgbm net-tools nspr nss nss-util pam pango procps-ng sudo unzip which zlib
     ```
   * Pacman
     ```bash
     # Arch
     sudo pacman -S alsa-lib cairo cups gdk-pixbuf2 glib2 glibc glibc-locales gtk3 libice libxcomposite libxcursor libxdamage libxfixes libxft libxinerama libxrandr libxt libxtst libxxf86vm libcap libdrm libglvnd libsndfile libtool make mesa-utils net-tools nspr nss pam pango procps-ng sudo unzip which zlib
     ```
1. X11 Forwarding needs to be configured and enabled on both the client and the server side:
   On your **head node**
   * Enable `X11Forwarding`, by editing `/etc/ssh/sshd_conf` and setting the following option:
     ```conf
     ...
     X11Forwarding yes
     ...
     ```
   * Install `xauth`
     * DNF / YUM
     ```bash
     # RHEL, Rocky, Alma, CentOS Stream
     sudo dnf update -y
     sudo dnf install xauth
     ```
     * APT
     ```bash
     # Debian, Ubuntu
     sudo apt update
     sudo apt install xauth
     ```
     * Pacman
     ```bash
     # Arch
     sudo pacman -Syu
     sudo pacman -S xorg-xauth
     ```
   * Reload your SSH server configuration
     ```bash
     sudo systemctl reload sshd
     ```
1. Open a new terminal on your local workstation and `ssh` onto your head node with the following option(s):
   ```bash
   # The -X switch enables the option ForwardX11
   ssh -X -i <PATH-TO-KEY> <USER>@<HEADNODE_IP>
   ```

> [!WARNING]
> Should you have issues with how the MATLAB GUI is rendered on your local workstation or receive a number of errors, you can try remedy these by enabling the `ForwardX11Trusted` option `-Y` switch, which will prevent your `ssh` connection from being subjected to [X11 Security Extensions](https://www.x.org/wiki/Development/Documentation/Security/).

## Install MATLAB, Simulink and Associated Toolboxes

1. On your **head node** navigate to the folder where you'd `unzipped` the downloaded MATLAB files and run the installer:
   ```bash
   cd <PATH_TO_MATBAL>
   ./install
   ```
1. This will open the MATLAB installation GUI on your local machine.
   Enter your `<EMAIL>` and `<PASSWORD>` associated with the Competition:
   <p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_gui_email.png" width=600 /></p>
1. Select the license associated with CHPC Workshop:
   <p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_gui_select_license.png" width=600 /></p>
1. Select an installation directory:
   <p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_gui_select_install_dir.png" width=600 /></p>
1. Select the products necessary to run the benchmarks.
   The license that you've been provided with grants you access to the full suite of MATLAB products. You are free to experiment with these until the conclusion of the competition. For the purposes of the competition you will require the following at the very least
   * MATLAB
   * Simulink
   * Curve Fitting Toolbox
   * Global Optimization Toolbox
   * MATLAB Coder
   * MATLAB Compiler
   * Optimization Toolbox
   * Parallel Computing Toolbox
   <p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_gui_toolboxes.png" width=600 /></p>
1. Confirm your configuration settings and install.
   The difference between the curated selection of toolboxes above and selection of the entire available suite of tools, is approximately 4 GB downloads (10 GB installed). Should have difficulties with missing libraries consider installing ***everything***.
   <p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_gui_confimration.png" width=600 /></p>
1. Export the `<PATH_TO_MATLAB>` so that it is included as part of your `<PATH>` variable:
   ```bash
   export PATH=<PATH_TO_SOFTWARE_DIR>:$PATH
   ```
1. You can now instantiate the MATLAB GUI and interpreter using
   ```bash
   matlab
   ```
   <p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_montecarlo_new_script.png" width=900 /></p>

You have successfully installed MATLAB!

# Benchmark: Monte Carlo Sampling Simulation (Calculating PI)

Your task is to optimize and parallelize MATLAB code for improved execution speed of a Monte Carlo simulation used to estimate the value of Pi in MATLAB. For approximating the value of Pi consider this stochastic method that populates an array with random values and tests for unit circle inclusion, i.e. we generate a random number along the coordinate $x \in [0, R]$ and another random number along the coordinate $y \in [0, R]$. The ratio of the area of the circle of radius $R$, relative to that of the square of side with length $2R$, can be written as follows:

$\frac{\textnormal{area of circle}}{\text{area of square}} = \frac{\pi r^2}{4r^2} = \frac{\pi}{4}$

## Visualize Problem Statement

In order to better understand the task at hand, save the following MATLAB script at `monteCarloPiVis.m`. This script will randomly generate a pair of $(x, y)$ points on a rectangular grid and test whether the $radius r^2 = x^2 + y^2$ of those randomly generated points lies within a circle. The value of $\pi$ is approximately proportional to the ratio of points within the circle versus those that lie outside of it. The accuracy of this approximation can be improved by increasing the number of random samples.

<p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_montecarlo_plot.png" width=300 /></p>

For now carefully copy and paste the code as it is for now for the purposes of plotting and demonstrating the example. Read through the comments to help you further understand exactly what it is that you are coding. Further descriptions will be given in the next section.

```matlab
function monteCarloPiVis(N)
% Comments in MATLAB are denoted using '%'
% N is the number of samples above where function monteCarloPiVis(N) is declared
% D is the canvas for the plot
D = 1000;

% points are the ones we mark for plotting purposes
% points is initialized to D x D array or "grid"" of zeroes
points = zeros(D);

% Initialize the number of points which satisfy the "within circle radius" check
count = 0;

% Plotting utilities
fig = gcf;
figure(gcf);

% Monte Carlo "for loop", iterating over N samples
% Simplified version without plotting utilities described in the next section.
for i = 1:N
    if mod( i, 5e3 ) == 0
        colormap( [1 1 1; 1 0 0; 0 1 0; 0 0 1] );
        image( points );
        title( sprintf( 'pi=%f', 4*(count/i)) );
        pause( 0.02 )
    end
    x = rand();
    y = rand();
    r = sqrt(x^2 + y^2);
    if r <= 1.0
        points( round(x*(D-1))+1, round(y*(D-1)+1)) = 2;
        count = count + 1;
    else
        points( round(x*(D-1))+1, round(y*(D-1)+1)) = 4;
    end
end
```

In order for your to reproduce the graph above, from the MATLAB GUI click on the "New Script" button copy, paste (using `Ctrl+Y`) and save the above into the "untitled" window. Then run your `monteCarloPiVis(1e6)` script with `N=1 000 000`.
<p align="center"><img alt="Matlab 2024B Linux Installation" src="./resources/matlab_montecarlo_run_vis.png" width=900 /></p>

## Single Core (Serial) Experiment

Save the following MATLAB script as `monteCarloPi.m` and use it to run the experiment on a Single Core. Verify the number of core(s) used to run the task using a terminal multiplexer together with your choice of either `htop` or `btop`.

```matlab
function monteCarloPi(N)
% N is number of samples

tic
count = 0;
for i=1:N
    x = rand();
    y = rand();
    r = sqrt(x^2 + y^2);
    if r<1
        count = count + 1;
    end
end
estimatePi = 4*count/N;
timeTaken = toc;

fprintf("Estimate for pi is %.8f after %f seconds\n", estimatePi, timeTaken)
fprintf("Absolute error is %8.3e\n", abs( estimatePi-pi ))
fprintf("%.2f million samples per second\n", N/timeTaken/1e6 )
end

```

This time you will be running the benchmark without the GUI in a non-interactive mode using:
```bash
matlab -nodisplay -nosplash -nodesktop -nojvm -r "monteCarloPi(1e6)"
```

## Improve Performance Using MATLAB `Parfor`

## Run the Benchmark Over your Entire Cluster Using MPI
