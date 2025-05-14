#  NGC: Normalized Genome Compressor
This project provides an interactive platform for researchers and developers to explore benchmark results from different genome compressors across various datasets (including DNA and small genomes). Users can delve into key performance metrics through dynamic charts and tables, facilitating easier comparison and informed decision-making.

### Key Features:

* **Interactive Visualizations:**
    * Generate and display various chart types, including bar charts and scatter plots, to represent benchmark data.
    * Visualize critical metrics such as WACR (Whole-genome Average Compression Ratio), Total Decompression Time, Peak Compression/Decompression Memory Usage, Compression/Decompression CPU Usage, and Compression Size.
    * Interactive features like zoom and dynamic updates for enhanced data exploration.

* **Data Comparison:**
    * Compare different compressors side-by-side.
    * Analyze performance across different genome types and datasets.
    * Group bar charts by compressor with type-based color distinctions for clarity.

* **User-Friendly Interface (Frontend built with React/Next.js - *inferred*):**
    * Intuitive navigation with "Back to Home" links and clear page layouts.
    * Quick selectors for benchmarks, genome types, and metrics.
    * Enhanced UI components with animations and transitions.



## Supporting Platform

Web access - All
Backend Testing - Linux x64

## Tech Stack

- Backend: Python
- Database: MongoDB
- Frontend: NextJs
- Testing: C++


## Supported File Formats

- FASTA / Multi-FASTA
- FASTQ
- Raw sequence files

## Compression and Decompression Methods

The general-purpose compressors:

- 7-zip (https://www.7-zip.org)
- paq8px (https://github.com/hxim/paq8px)
- bsc (https://github.com/IlyaGrebnov/libbsc)
- gzip (https://www.gnu.org/software/gzip/)
- zstd (https://github.com/facebook/zstd.git)
- bzip2 (http://sourceware.org/bzip2)
- zpaq (http://mattmahoney.net/dc/zpaq.html)
- cmix (https://github.com/byronknoll/cmix)

## Requirements
1. Install 7zip using command
    ```sh
    $ sudo apt install 7zip
    ```
2. Install gzip using command
    ```sh
    $ sudo apt install gzip
    ```
3. Other general purpose executables come with main repository

4. GCC compiler version: 11 (works with >=9.0)

5. To compress DNA files place original files in dna/raw/ folder.

## Installation Process for Executables (Please create/download executables as per the system specifications)

- paq8px
```sh
    $ git clone https://github.com/hxim/paq8px.git
    $ cd paq8px/build
    $ cmake ..
    $ make
```
- bsc (Please consider using the process given in the following link to generate an executable file.)
```sh
    $ https://github.com/AnshuOishik/GraSS
```

- zstd
```sh
    $ git clone https://github.com/facebook/zstd.git
    $ cd zstd/programs
    $ make
```
- bzip2
```sh
   $ git clone git://sourceware.org/git/bzip2.git
   $ cd bzip2
   $ make
```
- zpaq: Download (zpaq v7.15) from the following link, then create an execution file for Linux using make.
```sh
    https://www.mattmahoney.net/dc/zpaq.html
```
- cmix (clang++17 version required)
```sh
    $ git clone https://github.com/byronknoll/cmix
    $ cd cmix
    $ make
```
  
## Installation process of the proposed method (NGC)

1. Clone the repository:
    ```sh
   $ git clone https://github.com/Arno2003/NGC.git
   $ cd NGC-main
    ```

## Compilation & Run

To compile, use makefile

```sh
    $ cd build
    $ cmake ..
    $ make
```

To run, use the below script:

```sh
    $ cd build
    $ ./NGC <input_file_path>
```

    
## Tested System Specification

Ubuntu 18.04.1 LTS (64-bit) Intel Xeon CPUs (E5-2643 v3 @ 3.4 GHz, 6 cores) 128 GB RAM 

## Compression Methods Settings for Best Compression Ratio
1. 7-zip: Uses LZMA2 with maximum compression level "-mx" = 9, an 8 GB dictionary, and multithreading enabled.
2. paq8px: Using flag (level) 12 for high compression ratios.
3. bsc: Compresses using bsc with the "-e2" flag for best adaptive entropy encoding and "-b2047" for maximum block size.
4. gzip: Maximum compression enforced by the level 9.
5. zstd: In ultra compression mode with "--ultra", level 22 and number of threads 4 to achieve the highest compression ratio.
6. bzip2: Using maximum compression level 9.
7. zpaq: Uses zpaq at method level 5 with threads set to twice the number of CPUs.
8. cmix: Default settings.