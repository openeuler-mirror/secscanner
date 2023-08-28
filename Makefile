# Makefile for source rpm
SPECFILE := secscanner.spec
NAME := secscanner
VERSION := 1.0

.PHONY: help
help:
%:
	@echo "Try make $@ or something like that"
	@exit 1

sources: clean
	git archive --prefix="${NAME}-$(VERSION)/" -o "${NAME}-$(VERSION).tar.gz" HEAD

source: sources
	if test ! -d SOURCES; then mkdir SOURCES; fi
	mv *.tar.gz SOURCES

srpm: source
	if test ! -d BUILD/SRPM; then mkdir -p BUILD/SRPM; fi
	mock  --resultdir BUILD/SRPM --buildsrpm --spec ${SPECFILE} --sources SOURCES
rpm: srpm
	if test ! -d BUILD/RPM; then mkdir -p BUILD/RPM; fi
	mock   --resultdir BUILD/RPM --target noarch --rebuild BUILD/SRPM/secScanner-*.src.rpm
clean ::
	@rm -fr SOURCES BUILD

sandwich:
	@[ `id -u` -ne 0 ] && echo "What? Make it yourself." || echo Okay.

