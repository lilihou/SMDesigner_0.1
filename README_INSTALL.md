# **SMDesigner Installation and System Requirements**
## Download the package file:
[SMDesigner-1.0.0.tar.gz](https://github.com/lilihou/SMDesigner_0.1/blob/main/dist/SMDesigner-1.0.0.tar.gz)
## System Requirements

### Operating System:
SMDesigner is a Python-based program requiring the external software R2R, written in C and Perl. It must be run on UNIX, Linux, or macOS, or within a compatible environment such as Cygwin or WSL on Windows.
### Compiler:
R2R, written in C and Perl, requires the GNU C compiler (gcc) and GNU C++ compiler (g++). Ensure your PATH environment variable includes a directory with a Perl executable.
### Dependencies:
R2R (Weinberg and Breaker, 2011) for marking RNA structure features.
Infernal library package: Infernal, required by R2R.
#### SMDesigner has been successfully tested on UNIX, macOS, Cygwin, and WSL on Windows.

## Using SMDesigner with R2R
### If R2R is already installed:
Download the package SMDesigner-1.0.0.tar.gz from here.
Install with pip:
'''bash
pip install <download-path>/SMDesigner-1.0.0.tar.gz
Test the installation:
'''bash
SMDesigner
test
### if R2R is not installed:
SMDesigner includes an automatic installer for R2R during the first run. If the installation fails due to environmental requirements, install R2R manually following instructions from [R2R's SourceForge page](https://sourceforge.net/projects/weinberg-r2r/).
## Installation Examples

### For macOS:
#### Check for required tools:
'''bash
gcc --version  
g++ --version  
autoconf --version  
automake --version  
If not installed, use Homebrew:
'''bash
xcode-select --install  
brew install autoconf automake  
Install Homebrew if necessary:
'''bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  
#### Using Conda (recommended):
Create a new environment:
'''bash
conda create --name myenv  
conda activate myenv 
Install Infernal and Python:
'''bash
conda install -c bioconda infernal  
conda install python=3.x  
Install SMDesigner:
'''bash
pip install <path>/SMDesigner-1.0.0.tar.gz  
Verify installation:
'''bash
SMDesigner  
test  
### For Cygwin (Windows):
Install Cygwin:
During installation, include these essential packages: gcc, make, wget, tar, gzip, perl, vim, and curl.
Install SMDesigner:
'''bash
pip install <path>/SMDesigner-1.0.0.tar.gz  
				Add the installation directory to PATH in .bashrc:
				'''bash
				echo 'export PATH=$PATH:/cygdrive/c/path/to/SMDesigner' >> ~/.bashrc  
    source ~/.bashrc  
Run SMDesigner:
'''bash
SMDesigner  
test
## Debugging Installation Issues

### Infernal installation on macOS:
Ensure the correct architecture (osx-64) using:
'''bash
conda info | grep platform  
### R2R installation on Cygwin:
If the automatic installer fails, check R2R’s location with:
'''bash
where r2r  
Ensure the path is correctly set in the environment.
## Notes:
For Cygwin: Convert Windows paths to Unix-style paths (e.g., C:\Users\... to /cygdrive/c/Users/...).
Follow instructions carefully for each system to avoid installation errors.


