# Use a base image
FROM ubuntu:latest

# Set the maintainer label
LABEL maintainer="oskar.thaeter@gmail.com"

# Update the package list
RUN apt-get update

# Install software-properties-common to add repositories
RUN apt-get install -y software-properties-common

# Add the Ubuntu Toolchain Test repository for the latest GCC & G++
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test

# Update the package list again
RUN apt-get update

# Install GCC 12 and G++
RUN apt-get install -y gcc-12 g++-12

# Install CMake
RUN apt-get install -y cmake

# Install Git
RUN apt-get install -y git

# Install libtiff
RUN apt-get install -y libtiff-dev

# Install libopenjp2
RUN apt-get install -y libopenjp2-7-dev

# Install libgdal
RUN apt-get install -y libgdal-dev

# Install libproj
RUN apt-get install -y libproj-dev

# Install sqlite3
RUN apt-get install -y sqlite3

# Install libsqlite3
RUN apt-get install -y libsqlite3-dev

# Install curl
RUN apt-get install -y curl

# Install Python and pip, necessary for Conan
RUN apt-get install -y python3 python3-pip

# Install Conan
RUN pip3 install conan==1.62.0

# Set GCC 12 and G++ 12 as the default compilers
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 60 --slave /usr/bin/g++ g++ /usr/bin/g++-12

# Clean up the cache to reduce the image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set a working directory
WORKDIR /usr/src/recipes

# Copy your application's source code and Conanfile into the image
COPY . /usr/src/recipes

# call conan create
RUN conan create /usr/src/recipes/conan-proj/ local/stable -s build_type=Release -s compiler.libcxx=libstdc++11 --build=missing -pr:b=default

RUN conan create /usr/src/recipes/conan-libtiff/ local/stable -s build_type=Release -s compiler.libcxx=libstdc++11 --build=missing -pr:b=default

RUN conan create /usr/src/recipes/conan-openjpeg/ local/stable -s build_type=Release -s compiler.libcxx=libstdc++11 --build=missing -pr:b=default

RUN conan create /usr/src/recipes/conan-gdal/ local/stable -s build_type=Release -s compiler.libcxx=libstdc++11 --build=missing -pr:b=default

RUN conan create /usr/src/recipes/conan-opencv/ local/stable -s build_type=Release -s compiler.libcxx=libstdc++11 --build=missing -pr:b=default

# Set the default command
CMD ["bash"]
