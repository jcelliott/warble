warble
======

### Dependencies ###

* python (2.7)
* matplotlib (1.2.1)
* aubio (0.4.0-alpha)
  * libsndfile
  * libsamplerate
  * FFTW
  * SWIG (to build python modules)

#### Error building libsndfile on osx ####
* I ended up commenting out #include <Carbon.h> in programs/sndfile-play.c
* built fine on linux

#### Error building aubio: ####
* Download release version from website (0.3.2)
  * Add libm to linker flags: LDFLAGS=-lm make 
* or download latest from repo (0.4.0-alpha)
  * Add libm to linker flags: LDFLAGS=-lm ./waf build

TODO
====

* add tests!
* add a real options parser
* intonation filtering based on time
* weight pitches based on duration or pitch change
* smoothing (averaging) filter
