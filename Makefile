export

OS = $(shell uname -s)
REL_PROFILE ?= pkg
# The version-release used for package
PKG_VSN ?= 3.0-rc.5
# Tag or branch to clone emqx-rel project
REL_TAG ?= v3.0-rc.5
# Default tag for all emqx-rel dependencies
EMQX_DEPS_DEFAULT_VSN ?= v3.0-rc.5
# Override the default
# emqx_vsn = v3.0.0
##
## Support RPM and Debian based linux systems
##
ifeq ($(OS),Linux)
	ARCH          = $(shell uname -m)
	ISRPM         = $(shell cat /etc/redhat-release 2> /dev/null)
	ISDEB         = $(shell cat /etc/debian_version 2> /dev/null)
	ISSLES        = $(shell cat /etc/SuSE-release 2> /dev/null)
	ifneq ($(ISRPM),)
	OSNAME        = RedHat
	PKGERDIR      = rpm
	BUILDDIR      = rpmbuild
else
	ifneq ($(ISDEB),)
	OSNAME        = Debian
	PKGERDIR      = deb
	BUILDDIR      = debuild
else
	ifneq ($(ISSLES),)
	OSNAME        = SLES
	PKGERDIR      = rpm
	BUILDDIR      = rpmbuild
endif  # SLES
endif  # deb
endif  # rpm
endif  # linux

.PHONY: ostype

## Call platform dependent makefile
ostype:clean
	$(if $(PKGERDIR),,$(error "Operating system '$(OS)' not supported"))
	cd $(PKGERDIR) && $(MAKE)

clean:
	rm -rf package
	make -C rpm clean

.PHONY: rpm
rpm:
	make -C rpm
