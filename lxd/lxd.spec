# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 1
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if 0%{?centos} == 7
# centos doesn't (yet) define build macros for golang
%define gobuild(o:) %{expand:
  go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}'" -a -v -x %{?**};
}
# Define commands for testing
%define gotestflags      -buildmode pie -compiler gc
%define gotestextldflags %__global_ldflags %{?__golang_extldflags}
%define gotest() go test %{gotestflags} -ldflags "${LDFLAGS:-} -extldflags '%{gotestextldflags}'" %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         lxc
%global repo            lxd
# https://github.com/lxc/lxd
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

Name:           lxd
Version:        3.12
Release:        0.1%{?dist}
Summary:        Container hypervisor based on LXC
License:        ASL 2.0
URL:            https://linuxcontainers.org/lxd
Source0:        https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.socket
Source2:        %{name}.service
Source3:        lxd-containers.service
Source4:        lxd.dnsmasq
Source5:        lxd.logrotate
Source6:        shutdown
Source7:        lxd.sysctl
Source8:        lxd.profile
Patch0:         lxd-3.8-de-translation-newline-1.patch
Patch1:         lxd-3.8-ptbr-translation-newline.patch

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:  aarch64 %{arm} ppc64le s390x x86_64
%endif

# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

BuildRequires:  chrpath
BuildRequires:  gettext
BuildRequires:  help2man
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig(lxc)
BuildRequires:  systemd
# tclsh required by embedded sqlite3 build
BuildRequires:  tcl
# required by embedded dqlite build
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  libuv-devel

Requires: acl
Requires: dnsmasq
Requires: ebtables
Requires: iptables
Requires: lxd-client = %{version}-%{release}
Requires: lxcfs
Requires: rsync
Requires: shadow-utils >= 4.1.5
Requires: squashfs-tools
Requires: tar
Requires: xdelta
Requires: xz
%{?systemd_requires}
Requires(pre): container-selinux >= 2:2.38
Requires(pre): shadow-utils
# Do not require bundled libraries
%global __requires_exclude libsqlite3.so.0
%global __requires_exclude %{__requires_exclude}|libdqlite.so.0

Provides: bundled(libsqlite3.so.0())
Provides: bundled(libdqlite.so.0())
# Do not auto-provide .so files in the application-specific library directory
%global __provides_exclude_from %{_libdir}/%{name}/.*\\.so

%description
Container hypervisor based on LXC
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the LXD daemon.

%if 0%{?with_devel}
%package devel
Summary:        Container hypervisor based on LXC - Source Libraries
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  btrfs-progs
BuildRequires:  dnsmasq
%endif

Provides:       golang(%{import_path}/client) = %{version}-%{release}
Provides:       golang(%{import_path}/lxc/config) = %{version}-%{release}
Provides:       golang(%{import_path}/lxc/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/cluster) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/config) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/db) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/db/cluster) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/db/node) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/db/query) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/db/schema) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/endpoints) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/maas) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/migration) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/node) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/state) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/sys) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/task) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/template) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/types) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd/util) = %{version}-%{release}
Provides:       golang(%{import_path}/lxd-benchmark/benchmark) = %{version}-%{release}
Provides:       golang(%{import_path}/shared) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/api) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/cancel) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/cmd) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/eagain) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/generate/db) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/generate/file) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/generate/lex) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/i18n) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/idmap) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/ioprogress) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/log15) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/log15/stack) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/log15/term) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/logger) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/logging) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/osarch) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/simplestreams) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/subtest) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/termios) = %{version}-%{release}
Provides:       golang(%{import_path}/shared/version) = %{version}-%{release}

%if 0%{?with_bundled}
# Avoid duplicated Provides of bundled libraries
Autoprov:       0
Provides:       lxd-devel = %{version}-%{release}

# generated from dist/MANIFEST
Provides:       bundled(golang(github.com/armon/go-metrics)) = f0300d1749da6fa982027e449ec0c7a145510c3c
Provides:       bundled(golang(github.com/armon/go-metrics/circonus)) = f0300d1749da6fa982027e449ec0c7a145510c3c
Provides:       bundled(golang(github.com/armon/go-metrics/datadog)) = f0300d1749da6fa982027e449ec0c7a145510c3c
Provides:       bundled(golang(github.com/armon/go-metrics/prometheus)) = f0300d1749da6fa982027e449ec0c7a145510c3c
Provides:       bundled(golang(github.com/boltdb/bolt)) = fd01fc79c553a8e99d512a07e8e0c63d4a3ccfc5
Provides:       bundled(golang(github.com/boltdb/bolt/cmd/bolt)) = fd01fc79c553a8e99d512a07e8e0c63d4a3ccfc5
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/candidtest)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/params)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/ussodischarge)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/ussologin)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/cmd/dqlite)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/bindings)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/client)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/connection)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/logging)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/protocol)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/registry)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/replication)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/store)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/trace)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/internal/transaction)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/recover)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/recover/delete)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/recover/dump)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/go-dqlite/testdata)) = 3eab944668d7af5d0fc69ddb387ffda76300541c
Provides:       bundled(golang(github.com/CanonicalLtd/raft-http)) = 4c2dd679d3b46c11b250d63ae43467d4c4ab0962
Provides:       bundled(golang(github.com/CanonicalLtd/raft-membership)) = 3846634b0164affd0b3dfba1fdd7f9da6387e501
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/election)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/event)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/fsms)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/logging)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/network)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/cpuguy83/go-md2man)) = f79a8a8ca69da163eee19ab442bedad7a35bba5a
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/md2man)) = f79a8a8ca69da163eee19ab442bedad7a35bba5a
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/vendor/github.com/russross/blackfriday/v2)) = f79a8a8ca69da163eee19ab442bedad7a35bba5a
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/vendor/github.com/shurcooL/sanitized_anchor_name)) = f79a8a8ca69da163eee19ab442bedad7a35bba5a
Provides:       bundled(golang(github.com/dustinkirkland/golang-petname)) = d3c2ba80e75eeef10c5cf2fc76d2c809637376b3
Provides:       bundled(golang(github.com/dustinkirkland/golang-petname/cmd/petname)) = d3c2ba80e75eeef10c5cf2fc76d2c809637376b3
Provides:       bundled(golang(github.com/flosch/pongo2)) = 79872a7b27692599b259dc751bed8b03581dd0de
Provides:       bundled(golang(github.com/gogo/protobuf/codec)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/conformance)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/conformance/internal/conformance_proto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/gogoproto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/gogoreplace)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/io)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/jsonpb)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/jsonpb/jsonpb_test_proto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/compare)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/defaultcheck)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/description)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/embedcheck)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/enumstringer)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/equal)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/face)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/gostring)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/marshalto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/oneofcheck)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/populate)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/size)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/stringer)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/testgen)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/union)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/plugin/unmarshal)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/proto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-combo)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gofast)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/descriptor)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogofast)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogofaster)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/generator)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/generator/internal/remap)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/grpc)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/plugin)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogoslick)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/deprecated)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/extension_base)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/extension_extra)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/extension_user)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/grpc)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/import_public)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/import_public/importing)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/import_public/sub)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/imports)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/imports/fmt)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/imports/test_a_1)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/imports/test_a_2)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/imports/test_b_1)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/my_test)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/testdata/proto3)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gogotypes)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-gen-gostring)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/protoc-min-version)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/proto/proto3_proto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/proto/test_proto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/sortkeys)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/asymetric-issue125)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/cachedsize)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/casttype)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/casttype/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/casttype/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/casttype/combos/neither)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/casttype/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/castvalue)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/castvalue/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/castvalue/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/castvalue/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/custom)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/custombytesnonstruct)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/custom-dash-type)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/dashfilename)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/data)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/defaultconflict)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/deterministic)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/embedconflict)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/empty-issue70)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/enumcustomname)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/enumdecl)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/enumdecl_all)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/enumprefix)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/enumstringer)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/example)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/filedotname)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/fuzztests)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/group)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/importcustom-issue389/imported)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/importcustom-issue389/importing)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/importdedup)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/importdedup/subpkg)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/importduplicate)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/importduplicate/proto)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/importduplicate/sortkeys)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/indeximport-issue72)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/indeximport-issue72/index)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/int64support)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue260)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue261)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue262)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue270)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue312)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue312/events)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue322)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue330)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue34)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue411)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue42order)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue435)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue438)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue444)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue449)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue498)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue503)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue530)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/issue8)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/jsonpb-gogo)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapdefaults)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapdefaults/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapdefaults/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapdefaults/combos/neither)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapdefaults/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapsproto2)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapsproto2/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapsproto2/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapsproto2/combos/neither)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mapsproto2/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/merge)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/mixbench)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/moredefaults)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/nopackage)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof3)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof3/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof3/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof3/combos/neither)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof3/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof/combos/neither)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneof/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/oneofembed)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/packed)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/proto3extension)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/protosize)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/required)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/sizerconflict)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/sizeunderscore)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/stdtypes)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/tags)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/theproto3)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/theproto3/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/theproto3/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/theproto3/combos/neither)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/theproto3/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/typedecl)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/typedecl_all)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/typedeclimport)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/typedeclimport/subpkg)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/types/combos/both)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/types/combos/marshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/types/combos/neither)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/types/combos/unmarshaler)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/unmarshalmerge)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/unrecognized)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/unrecognizedgroup)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/test/xxxfields)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/types)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/vanity)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/vanity/command)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/vanity/test)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/vanity/test/fast)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/vanity/test/faster)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/vanity/test/slick)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/gogo/protobuf/version)) = 382325bbbb4d1c850eec1f3ec92a1a16f502d68b
Provides:       bundled(golang(github.com/golang/protobuf/descriptor)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/jsonpb)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/jsonpb/jsonpb_test_proto)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/proto)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/descriptor)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/generator)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/generator/internal/remap)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/grpc)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/plugin)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/deprecated)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_base)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_extra)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_user)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/grpc)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/import_public)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/import_public/importing)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/import_public/sub)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/fmt)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_a_1)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_a_2)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_b_1)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/issue780_oneof_conflict)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/multi)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/my_test)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/proto3)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/proto/proto3_proto)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/proto/test_proto)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/ptypes)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/any)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/duration)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/empty)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/struct)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/timestamp)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/wrappers)) = d3c38a4eb4970272b87a425ae00ccc4548e2f9bb
Provides:       bundled(golang(github.com/google/uuid)) = 0cd6bf5da1e1c83f8b45653022c74f71af0538a4
Provides:       bundled(golang(github.com/gorilla/mux)) = c5c6c98bc25355028a63748a498942a6398ccd22
Provides:       bundled(golang(github.com/gorilla/websocket)) = 0ec3d1bd7fe50c503d6df98ee649d81f4857c564
Provides:       bundled(golang(github.com/gorilla/websocket/examples/autobahn)) = 0ec3d1bd7fe50c503d6df98ee649d81f4857c564
Provides:       bundled(golang(github.com/gorilla/websocket/examples/chat)) = 0ec3d1bd7fe50c503d6df98ee649d81f4857c564
Provides:       bundled(golang(github.com/gorilla/websocket/examples/command)) = 0ec3d1bd7fe50c503d6df98ee649d81f4857c564
Provides:       bundled(golang(github.com/gorilla/websocket/examples/echo)) = 0ec3d1bd7fe50c503d6df98ee649d81f4857c564
Provides:       bundled(golang(github.com/gorilla/websocket/examples/filewatch)) = 0ec3d1bd7fe50c503d6df98ee649d81f4857c564
Provides:       bundled(golang(github.com/gosexy/gettext)) = 74466a0a0c4a62fea38f44aa161d4bbfbe79dd6b
Provides:       bundled(golang(github.com/gosexy/gettext/_examples)) = 74466a0a0c4a62fea38f44aa161d4bbfbe79dd6b
Provides:       bundled(golang(github.com/gosexy/gettext/go-xgettext)) = 74466a0a0c4a62fea38f44aa161d4bbfbe79dd6b
Provides:       bundled(golang(github.com/hashicorp/go-immutable-radix)) = 27df80928bb34bb1b0d6d0e01b9e679902e7a6b5
Provides:       bundled(golang(github.com/hashicorp/golang-lru)) = 7087cb70de9f7a8bc0a10c375cb0d2280a8edf9c
Provides:       bundled(golang(github.com/hashicorp/golang-lru/simplelru)) = 7087cb70de9f7a8bc0a10c375cb0d2280a8edf9c
Provides:       bundled(golang(github.com/hashicorp/go-msgpack/codec)) = be3a5be7ee2202386d02936a19ae4fbde1c77800
Provides:       bundled(golang(github.com/hashicorp/logutils)) = a335183dfd075f638afcc820c90591ca3c97eba6
Provides:       bundled(golang(github.com/hashicorp/raft)) = 6e5ba93211eaf8d9a2ad7e41ffad8c6f160f9fe3
Provides:       bundled(golang(github.com/hashicorp/raft/bench)) = d9517af3f8d2d25aaf55786b8fef505736940c5a
Provides:       bundled(golang(github.com/hashicorp/raft-boltdb)) = 6e5ba93211eaf8d9a2ad7e41ffad8c6f160f9fe3
Provides:       bundled(golang(github.com/hashicorp/raft/fuzzy)) = d9517af3f8d2d25aaf55786b8fef505736940c5a
Provides:       bundled(golang(github.com/jaypipes/pcidb)) = adf5a9192458392195b34ec0677172bd69e95b82
Provides:       bundled(golang(github.com/juju/clock)) = 9c5c9712527c7986f012361e7d13756b4d99543d
Provides:       bundled(golang(github.com/juju/clock/monotonic)) = 9c5c9712527c7986f012361e7d13756b4d99543d
Provides:       bundled(golang(github.com/juju/clock/testclock)) = 9c5c9712527c7986f012361e7d13756b4d99543d
Provides:       bundled(golang(github.com/juju/collections/deque)) = 9be91dc79b7c185fa8b08e7ceceee40562055c83
Provides:       bundled(golang(github.com/juju/collections/set)) = 9be91dc79b7c185fa8b08e7ceceee40562055c83
Provides:       bundled(golang(github.com/juju/errors)) = e65537c515d77e35697c471d6c2755375cb3adc4
Provides:       bundled(golang(github.com/juju/go4/bytereplacer)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/cloud/cloudlaunch)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/cloud/google/gceutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/cloud/google/gcsutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/ctxutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/errorutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/fault)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/jsonconfig)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/legal)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/lock)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/net/throttle)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/oauthutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/osutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/readerutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/strutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/syncutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/syncutil/singleflight)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/syncutil/syncdebug)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/types)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/wkfs)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/wkfs/gcs)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/go4/writerutil)) = 40d72ab9641a2a8c36a9c46a51e28367115c8e59
Provides:       bundled(golang(github.com/juju/gomaasapi)) = 8a8cec793ba70659ba95f1b9a491ba807169bfc3
Provides:       bundled(golang(github.com/juju/gomaasapi/example)) = 8a8cec793ba70659ba95f1b9a491ba807169bfc3
Provides:       bundled(golang(github.com/juju/gomaasapi/templates)) = 8a8cec793ba70659ba95f1b9a491ba807169bfc3
Provides:       bundled(golang(github.com/juju/httprequest)) = 77d36ac4b71a6095506c0617d5881846478558cb
Provides:       bundled(golang(github.com/juju/httprequest/cmd/httprequest-generate-client)) = 77d36ac4b71a6095506c0617d5881846478558cb
Provides:       bundled(golang(github.com/juju/loggo)) = d976af380377adda50b2d34279f1dec3507504ac
Provides:       bundled(golang(github.com/juju/loggo/example)) = d976af380377adda50b2d34279f1dec3507504ac
Provides:       bundled(golang(github.com/juju/loggo/loggocolor)) = d976af380377adda50b2d34279f1dec3507504ac
Provides:       bundled(golang(github.com/juju/persistent-cookiejar)) = d5e5a8405ef9633c84af42fbcc734ec8dd73c198
Provides:       bundled(golang(github.com/juju/schema)) = 64a6158e90710d0a16c6bd3cf0a6be6b2e80193c
Provides:       bundled(golang(github.com/juju/utils)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/arch)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/bzr)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/cache)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/cert)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/debugstatus)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/deque)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/du)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/exec)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/featureflag)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/filepath)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/filestorage)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/fs)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/hash)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/jsonhttp)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/keyvalues)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/mgokv)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/os)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/parallel)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/proxy)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/readpass)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/registry)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/series)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/set)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/shell)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/ssh)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/ssh/testing)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/symlink)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/tailer)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/tar)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/uptime)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/voyeur)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/winrm)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/utils/zip)) = bf9cc5bdd62dabc40b7f634b39a5e2dc44d44c45
Provides:       bundled(golang(github.com/juju/version)) = b64dbd566305c836274f0268fa59183a52906b36
Provides:       bundled(golang(github.com/juju/webbrowser)) = efb9432b2bcb671b0cf2237468e209d10e2ac373
Provides:       bundled(golang(github.com/julienschmidt/httprouter)) = 26a05976f9bf5c3aa992cc20e8588c359418ee58
Provides:       bundled(golang(github.com/mattn/go-colorable)) = 3a70a971f94a22f2fa562ffcc7a0eb45f5daf045
Provides:       bundled(golang(github.com/mattn/go-colorable/cmd/colorable)) = 3a70a971f94a22f2fa562ffcc7a0eb45f5daf045
Provides:       bundled(golang(github.com/mattn/go-colorable/_example/escape-seq)) = 3a70a971f94a22f2fa562ffcc7a0eb45f5daf045
Provides:       bundled(golang(github.com/mattn/go-colorable/_example/logrus)) = 3a70a971f94a22f2fa562ffcc7a0eb45f5daf045
Provides:       bundled(golang(github.com/mattn/go-colorable/_example/title)) = 3a70a971f94a22f2fa562ffcc7a0eb45f5daf045
Provides:       bundled(golang(github.com/mattn/go-isatty)) = c2a7a6ca930a4cd0bc33a3f298eb71960732a3a7
Provides:       bundled(golang(github.com/mattn/go-runewidth)) = 703b5e6b11ae25aeb2af9ebb5d5fdf8fa2575211
Provides:       bundled(golang(github.com/mattn/go-sqlite3)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/custom_func)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/hook)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/limit)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/mod_regexp)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/mod_vtable)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/simple)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/trace)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/_example/vtable)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/mattn/go-sqlite3/upgrade)) = 31f5bb843b7852e28d5a66d1d539c042c3bb623a
Provides:       bundled(golang(github.com/miekg/dns)) = 73601d4aed9d844322611759d7f3619110b7c88e
Provides:       bundled(golang(github.com/miekg/dns/dnsutil)) = 73601d4aed9d844322611759d7f3619110b7c88e
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/acme)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/acme/autocert)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/acme/autocert/internal/acmetest)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/argon2)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/bcrypt)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/blake2b)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/blake2s)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/blowfish)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/bn256)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/cast5)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/chacha20poly1305)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/cryptobyte)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/cryptobyte/asn1)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/curve25519)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ed25519)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ed25519/internal/edwards25519)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/hkdf)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/internal/chacha20)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/internal/subtle)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/md4)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/nacl/auth)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/nacl/box)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/nacl/secretbox)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/nacl/sign)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ocsp)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/openpgp)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/openpgp/armor)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/openpgp/clearsign)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/openpgp/elgamal)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/openpgp/errors)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/openpgp/packet)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/openpgp/s2k)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/otr)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/pbkdf2)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/pkcs12)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/pkcs12/internal/rc2)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/poly1305)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ripemd160)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/salsa20)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/salsa20/salsa)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/scrypt)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/sha3)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ssh)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ssh/agent)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ssh/knownhosts)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ssh/terminal)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ssh/test)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/ssh/testdata)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/tea)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/twofish)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/xtea)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/crypto/xts)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/bpf)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/context)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/context/ctxhttp)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/dict)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/dns/dnsmessage)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/html)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/html/atom)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/html/charset)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/http2)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/http2/h2c)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/http2/h2demo)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/http2/h2i)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/http2/hpack)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/http/httpguts)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/http/httpproxy)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/icmp)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/idna)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/internal/iana)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/internal/nettest)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/internal/socket)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/internal/socks)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/internal/sockstest)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/internal/timeseries)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/ipv4)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/ipv6)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/lif)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/nettest)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/netutil)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/proxy)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/publicsuffix)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/route)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/trace)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/webdav)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/webdav/internal/xml)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/websocket)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/net/xsrftoken)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sync/errgroup)) = 73601d4aed9d844322611759d7f3619110b7c88e
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sync/semaphore)) = 73601d4aed9d844322611759d7f3619110b7c88e
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sync/singleflight)) = 73601d4aed9d844322611759d7f3619110b7c88e
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sync/syncmap)) = 73601d4aed9d844322611759d7f3619110b7c88e
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/cpu)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/plan9)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/unix)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/unix/linux)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/windows)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/windows/registry)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/windows/svc)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/windows/svc/debug)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/windows/svc/eventlog)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/windows/svc/example)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/miekg/dns/vendor/golang.org/x/sys/windows/svc/mgr)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(github.com/mitchellh/go-homedir)) = af06845cf3004701891bf4fdb884bfe4920b3727
Provides:       bundled(golang(github.com/mpvl/subtest)) = f6e4cfd4b9ea1beb9fb5d53afba8c30804a02ae7
Provides:       bundled(golang(github.com/olekukonko/tablewriter)) = f82d31373321de71ad0289113725564fe180a301
Provides:       bundled(golang(github.com/olekukonko/tablewriter/csv2table)) = f82d31373321de71ad0289113725564fe180a301
Provides:       bundled(golang(github.com/pborman/uuid)) = 8b1b92947f46224e3b97bb1a3a5b0382be00d31e
Provides:       bundled(golang(github.com/pkg/errors)) = 27936f6d90f9c8e1145f11ed52ffffbfdb9e0af7
Provides:       bundled(golang(github.com/Rican7/retry)) = 272ad122d6e5ce1be757544007cf8bcd1c9c9ab0
Provides:       bundled(golang(github.com/Rican7/retry/backoff)) = 272ad122d6e5ce1be757544007cf8bcd1c9c9ab0
Provides:       bundled(golang(github.com/Rican7/retry/jitter)) = 272ad122d6e5ce1be757544007cf8bcd1c9c9ab0
Provides:       bundled(golang(github.com/Rican7/retry/strategy)) = 272ad122d6e5ce1be757544007cf8bcd1c9c9ab0
Provides:       bundled(golang(github.com/rogpeppe/fastuuid)) = d61b6ae132d93dcb396be506396bf9a5127a41aa
Provides:       bundled(golang(github.com/ryanfaerman/fsm)) = 3dc1bc0980272fd56d81167a48a641dab8356e29
Provides:       bundled(golang(github.com/spf13/cobra)) = 67fc4837d267bc9bfd6e47f77783fcc3dffc68de
Provides:       bundled(golang(github.com/spf13/cobra/cobra)) = 67fc4837d267bc9bfd6e47f77783fcc3dffc68de
Provides:       bundled(golang(github.com/spf13/cobra/cobra/cmd)) = 67fc4837d267bc9bfd6e47f77783fcc3dffc68de
Provides:       bundled(golang(github.com/spf13/cobra/doc)) = 67fc4837d267bc9bfd6e47f77783fcc3dffc68de
Provides:       bundled(golang(github.com/spf13/pflag)) = 24fa6976df40757dce6aea913e7b81ade90530e1
Provides:       bundled(golang(github.com/stretchr/testify)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/assert)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/_codegen)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/http)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/mock)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/require)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/suite)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/vendor/github.com/davecgh/go-spew/spew)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/vendor/github.com/pmezard/go-difflib/difflib)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/stretchr/testify/vendor/github.com/stretchr/objx)) = 34c6fa2dc70986bccbbffcc6130f6920a924b075
Provides:       bundled(golang(github.com/syndtr/gocapability/capability)) = d98352740cb2c55f81556b63d4a1ec64c5a319c2
Provides:       bundled(golang(github.com/syndtr/gocapability/capability/enumgen)) = d98352740cb2c55f81556b63d4a1ec64c5a319c2
Provides:       bundled(golang(golang.org/x/crypto/acme)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/acme/autocert)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/acme/autocert/internal/acmetest)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/argon2)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/bcrypt)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/blake2b)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/blake2s)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/blowfish)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/bn256)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/cast5)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/chacha20poly1305)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte/asn1)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/curve25519)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ed25519)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ed25519/internal/edwards25519)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/hkdf)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/internal/chacha20)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/internal/subtle)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/md4)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/nacl/auth)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/nacl/box)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/nacl/secretbox)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/nacl/sign)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ocsp)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/openpgp)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/armor)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/clearsign)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/elgamal)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/errors)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/packet)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/s2k)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/otr)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/pbkdf2)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/pkcs12)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/pkcs12/internal/rc2)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/poly1305)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ripemd160)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/salsa20)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/salsa20/salsa)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/scrypt)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/sha3)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ssh)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ssh/agent)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ssh/knownhosts)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ssh/terminal)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ssh/test)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/ssh/testdata)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/tea)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/twofish)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/xtea)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/crypto/xts)) = 38d8ce5564a5b71b2e3a00553993f1b9a7ae852f
Provides:       bundled(golang(golang.org/x/net/bpf)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/context)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/context/ctxhttp)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/dict)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/dns/dnsmessage)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/html)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/html/atom)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/html/charset)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/http2)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/http2/h2c)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/http2/h2demo)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/http2/h2i)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/http2/hpack)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/http/httpguts)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/http/httpproxy)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/icmp)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/idna)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/internal/iana)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/internal/socket)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/internal/socks)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/internal/sockstest)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/internal/timeseries)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/ipv4)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/ipv6)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/lif)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/nettest)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/netutil)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/proxy)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/publicsuffix)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/route)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/trace)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/webdav)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/webdav/internal/xml)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/websocket)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/net/xsrftoken)) = eb5bcb51f2a31c7d5141d810b70815c05d9c9146
Provides:       bundled(golang(golang.org/x/sys/cpu)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/plan9)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/unix)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/unix/linux)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/windows)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/windows/registry)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/windows/svc)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/windows/svc/debug)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/windows/svc/eventlog)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/windows/svc/example)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(golang.org/x/sys/windows/svc/mgr)) = 81d4e9dc473e5e8c933f2aaeba2a3d81efb9aed2
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/candidtest)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/params)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/ussodischarge)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/ussologin)) = 8d331dd5664bea29ab3762e226b14cfc49fbe22a
Provides:       bundled(golang(gopkg.in/errgo.v1)) = b20caedf0710d0988e92b5f2d76843ad1f231f2d
Provides:       bundled(golang(gopkg.in/httprequest.v1)) = 7f3c32e65ad57476ba9675100248f4f87f6ffb9c
Provides:       bundled(golang(gopkg.in/httprequest.v1/cmd/httprequest-generate-client)) = 7f3c32e65ad57476ba9675100248f4f87f6ffb9c
Provides:       bundled(golang(gopkg.in/juju/environschema.v1)) = 7359fc7857abe2b11b5b3e23811a9c64cb6b01e0
Provides:       bundled(golang(gopkg.in/juju/environschema.v1/form)) = 7359fc7857abe2b11b5b3e23811a9c64cb6b01e0
Provides:       bundled(golang(gopkg.in/juju/environschema.v1/form/cmd/formtest)) = 7359fc7857abe2b11b5b3e23811a9c64cb6b01e0
Provides:       bundled(golang(gopkg.in/juju/names.v2)) = fd59336b4621bc2a70bf96d9e2f49954115ad19b
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/attach)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/attach_with_pipes)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/checkpoint)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/clone)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/concurrent_create)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/concurrent_destroy)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/concurrent_shutdown)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/concurrent_start)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/concurrent_stop)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/concurrent_stress)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/config)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/console)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/create)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/create_snapshot)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/destroy)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/destroy_snapshots)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/device_add_remove)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/execute)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/freeze)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/interfaces)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/ipaddress)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/limit)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/list)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/list_keys)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/list_snapshots)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/reboot)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/rename)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/restore_snapshot)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/shutdown)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/start)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/stats)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/stop)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples/unfreeze)) = 2f350e4a298005190e893375fcc96ed8546fa35d
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/checkers)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/dbrootkeystore)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/example)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/example/meeting)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/internal/macaroonpb)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/mgorootkeystore)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/postgresrootkeystore)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakerytest)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/cmd/bakery-keygen)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/httpbakery)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/httpbakery/agent)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/httpbakery/form)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/internal/httputil)) = a0743b6619d68bbf8dc5cabbb49738b846f06080
Provides:       bundled(golang(gopkg.in/macaroon.v2)) = 1679699b0b723e05f9f16c45b4c6cbd46adb2c78
Provides:       bundled(golang(gopkg.in/mgo.v2)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/bson)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/dbtest)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/json)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/sasl)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/scram)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/txn)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/retry.v1)) = 87155f248cf6ea9e38ae7613f9ea1e5bb397ac83
Provides:       bundled(golang(gopkg.in/robfig/cron.v2)) = be2e0b0deed5a68ffee390b4583a13aff8321535
Provides:       bundled(golang(gopkg.in/tomb.v2)) = d5d1b5820637886def9eef33e03a27a9f166942c
Provides:       bundled(golang(gopkg.in/yaml.v2)) = 51d6538a90f86fe93ac480b35f37b2be17fef232
%endif

%description devel
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains library sources intended for
building other packages which use the import path
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:        Unit tests for %{name} package
BuildArch:      noarch
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

# test subpackage tests code from devel subpackage
Requires:       %{name}-devel = %{version}-%{release}

%if ! 0%{?with_bundled}
Requires:       golang(github.com/mattn/go-sqlite3)
Requires:       golang(github.com/mpvl/subtest)
Requires:       golang(github.com/stretchr/testify/assert) >= 1.2.0
Requires:       golang(github.com/stretchr/testify/require) >= 1.2.0
Requires:       golang(github.com/stretchr/testify/suite) >= 1.2.0
%endif

%description unit-test-devel
%{summary}.

This package contains unit tests for project providing packages
with %{import_path} prefix.
%endif

%package client
Summary:        Container hypervisor based on LXC - Client

Requires:       gettext

%description client
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the command line client.

%package tools
Summary:        Container hypervisor based on LXC - Extra Tools

%description tools
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains extra tools provided with LXD.
 - fuidshift - A tool to map/unmap filesystem uids/gids
 - lxc-to-lxd - A tool to migrate LXC containers to LXD
 - lxd-benchmark - A LXD benchmark utility

%package p2c
Summary:        A physical to container migration tool
#Requires:       netcat
Requires:       rsync

%description p2c
Physical to container migration tool

This tool lets you turn any Linux filesystem (including your current one)
into a LXD container on a remote LXD host.

It will setup a clean mount tree made of the root filesystem and any
additional mount you list, then transfer this through LXD's migration
API to create a new container from it.

%package doc
Summary:        Container hypervisor based on LXC - Documentation
BuildArch:      noarch

%description doc
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains user documentation.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%build
%if 0%{?with_bundled}
src_dir=$(pwd)/dist

# build embedded libsqlite3
pushd dist/sqlite
%configure --enable-replication --disable-amalgamation --disable-tcl --libdir=%{_libdir}/%{name}
make %{?_smp_mflags}
popd

# build embedded dqlite
pushd dist/dqlite
autoreconf -i
PKG_CONFIG_PATH="${src_dir}/sqlite/" %configure --libdir=%{_libdir}/%{name}
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -I${src_dir}/sqlite" LDFLAGS="-L${src_dir}/sqlite"
popd

mkdir _output
pushd _output
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(dirs +1 -l) src/%{import_path}
popd

# Move bundled libraries to vendor directory for proper devel packaging
mv dist/src vendor

ln -s vendor src
export GOPATH=$(pwd)/_output:$(pwd):%{gopath}
%else
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

export GOPATH=$(pwd):%{gopath}
%endif

# don't use LDFLAGS='-Wl,-z relro ' from redhat-rpm-config to avoid error:
# "flag provided but not defined: -Wl,-z,relro"
unset LDFLAGS

# LXD depends on a patched, bundled sqlite with replication capabilities
export CGO_CPPFLAGS="-I${src_dir}/sqlite/ -I${src_dir}/dqlite/include/"
export CGO_LDFLAGS="-L${src_dir}/sqlite/.libs/ -L${src_dir}/dqlite/.libs/ -Wl,-rpath,%{_libdir}/%{name}"
export LD_LIBRARY_PATH="${src_dir}/sqlite/.libs/:${src_dir}/dqlite/.libs/"

BUILDTAGS="libsqlite3" %gobuild -o _bin/lxd %{import_path}/lxd
%gobuild -o _bin/lxc %{import_path}/lxc
%gobuild -o _bin/fuidshift %{import_path}/fuidshift
%gobuild -o _bin/lxd-benchmark %{import_path}/lxd-benchmark
%gobuild -o _bin/lxd-p2c %{import_path}/lxd-p2c
%gobuild -o _bin/lxc-to-lxd %{import_path}/lxc-to-lxd

# build translations
rm -f po/zh_Hans.po    # remove invalid locale
make %{?_smp_mflags} build-mo

# generate man-pages
_bin/lxd manpage .
_bin/lxc manpage .
help2man _bin/fuidshift -n "uid/gid shifter" --no-info > fuidshift.1
help2man _bin/lxd-benchmark -n "The container lightervisor - benchmark" --no-info --version-string=%{version} --no-discard-stderr > lxd-benchmark.1
help2man _bin/lxd-p2c -n "Physical to container migration tool" --no-info --version-string=%{version} > lxd-p2c.1
help2man _bin/lxc-to-lxd -n "Convert LXC containers to LXD" --no-info --version-string=%{version} > lxc-to-lxd.1

%install
# install binaries
install -D -p -m 0755 _bin/lxc %{buildroot}%{_bindir}/lxc
install -D -p -m 0755 _bin/fuidshift %{buildroot}%{_bindir}/fuidshift
install -D -p -m 0755 _bin/lxd-benchmark %{buildroot}%{_bindir}/lxd-benchmark
install -D -p -m 0755 _bin/lxd-p2c %{buildroot}%{_bindir}/lxd-p2c
install -D -p -m 0755 _bin/lxd %{buildroot}%{_bindir}/%{name}
install -D -p -m 0755 _bin/lxc-to-lxd %{buildroot}%{_bindir}/lxc-to-lxd

# extra configs
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxd
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/lxd
install -D -p -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysctl.d/10-lxd-inotify.conf
install -D -p -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/profile.d/lxd.sh

# install bash completion
install -D -p -m 0644 scripts/bash/lxd-client %{buildroot}%{_datadir}/bash-completion/completions/lxd-client

# install systemd units
install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/

# install shutdown wrapper
install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}
install -p -m 0755 %{SOURCE6} %{buildroot}%{_libexecdir}/%{name}

# install custom libsqlite3/dqlite
install -d -m 0755 %{buildroot}%{_libdir}/%{name}
cp -Pp dist/sqlite/.libs/libsqlite3.so* %{buildroot}%{_libdir}/%{name}/
cp -Pp dist/dqlite/.libs/libdqlite.so* %{buildroot}%{_libdir}/%{name}/
# fix rpath
chrpath -r %{_libdir}/%{name} %{buildroot}%{_libdir}/%{name}/libdqlite.so

# install man-pages
install -d -m 0755 %{buildroot}%{_mandir}/man1
cp -p lxd.1 %{buildroot}%{_mandir}/man1/
cp -p lxc*.1 %{buildroot}%{_mandir}/man1/
cp -p fuidshift.1 %{buildroot}%{_mandir}/man1/
cp -p lxd-benchmark.1 %{buildroot}%{_mandir}/man1/
cp -p lxd-p2c.1 %{buildroot}%{_mandir}/man1/
cp -p lxc-to-lxd.1 %{buildroot}%{_mandir}/man1/

# cache and log directories
install -d -m 0711 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}

# language files
install -d -m 0755 %{buildroot}%{_datadir}/locale
for mofile in po/*.mo ; do
install -D -p -m 0644 ${mofile} %{buildroot}%{_datadir}/locale/$(basename ${mofile%%.mo})/LC_MESSAGES/%{name}.mo
done
%find_lang lxd

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}%{_includedir}/%{name}
echo "%%dir %%{_includedir}/%%{name}/." >> devel.file-list
cp -pav dist/sqlite/{sqlite3,sqlite3ext}.h %{buildroot}%{_includedir}/%{name}/
cp -pav dist/dqlite/include/dqlite.h %{buildroot}%{_includedir}/%{name}/
echo "%%{_includedir}/%%{name}/*.h" >> devel.file-list

install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
# find all *.s, *.c and *.h cgo development files and generate devel.file-list
for file in $(find . -iname "*.s" -o -iname "*.c" -o -iname "*.h"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go" -o -type f -wholename "./test/deps/s*"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}

# Add libsqlite3 tag to go test
%define gotestflags -buildmode pie -compiler gc -v -tags libsqlite3

# Tests must ignore potential LXD_SOCKET from environment
unset LXD_SOCKET

# Test against the libraries which just built
export CGO_CPPFLAGS="-I%{buildroot}%{_includedir}/%{name}/"
export CGO_LDFLAGS="-L%{buildroot}%{_libdir}/%{name}/"
export LD_LIBRARY_PATH="%{buildroot}%{_libdir}/%{name}/"

%gotest %{import_path}/lxc
# lxc-to-lxd test fails, see ganto/copr-lxc3#10
#%%gotest %%{import_path}/lxc-to-lxd
%gotest %{import_path}/lxd
%gotest %{import_path}/lxd/cluster
%gotest %{import_path}/lxd/config
%gotest %{import_path}/lxd/db
%gotest %{import_path}/lxd/db/cluster
%gotest %{import_path}/lxd/db/node
%gotest %{import_path}/lxd/db/query
%gotest %{import_path}/lxd/db/schema
%gotest %{import_path}/lxd/endpoints
%gotest %{import_path}/lxd/node
%gotest %{import_path}/lxd/task
%gotest %{import_path}/lxd/types
%gotest %{import_path}/lxd/util
%gotest %{import_path}/shared
%gotest %{import_path}/shared/idmap
# test fails, see ganto/copr-lxc3#13
#%%gotest %%{import_path}/shared/generate/db
#%%gotest %%{import_path}/shared/generate/lex
%gotest %{import_path}/shared/osarch
%gotest %{import_path}/shared/version
%endif

%pre
# check for existence of lxd group, create it if not found
getent group %{name} > /dev/null || groupadd -f -r %{name}
exit 0

%post
%systemd_post %{name}.socket
%systemd_post %{name}.service
%systemd_post %{name}-container.service

%preun
%systemd_preun %{name}.socket
%systemd_preun %{name}.service
%systemd_preun %{name}-container.service

%postun
%systemd_postun %{name}.socket
%systemd_postun %{name}.service
%systemd_postun %{name}-container.service

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/dnsmasq.d/lxd
%config(noreplace) %{_sysconfdir}/logrotate.d/lxd
%config(noreplace) %{_sysconfdir}/sysctl.d/10-lxd-inotify.conf
%config(noreplace) %{_sysconfdir}/profile.d/lxd.sh
%{_bindir}/%{name}
%{_unitdir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_mandir}/man1/%{name}.1.gz
%dir %{_localstatedir}/log/%{name}
%defattr(-, root, root, 0711)
%dir %{_localstatedir}/lib/%{name}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license COPYING
%doc AUTHORS
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license COPYING
%endif

%files client -f lxd.lang
%license COPYING
%{_bindir}/lxc
%{_datadir}/bash-completion/completions/lxd-client
%{_mandir}/man1/lxc.*1.gz

%files tools
%license COPYING
%{_bindir}/fuidshift
%{_bindir}/lxd-benchmark
%{_bindir}/lxc-to-lxd
%{_mandir}/man1/fuidshift.1.gz
%{_mandir}/man1/lxd-benchmark.1.gz
%{_mandir}/man1/lxc-to-lxd.1.gz

%files p2c
%license COPYING
%{_bindir}/lxd-p2c
%{_mandir}/man1/lxd-p2c.1.gz

%files doc
%license COPYING
%doc doc/*

%changelog
* Sat Mar 09 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.11-0.1
- Update to 3.11

* Sun Feb 17 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.10-0.1
- Update to 3.10

* Sun Feb 03 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.9-0.1
- Update to 3.9

* Thu Dec 27 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.8-0.1
- Update to 3.8
- Fix build macros for CentOS and simplify build env variables
- Set --libdir and rpath to avoid LD_LIBRARY_PATH wrapper
- Add upstream patch to fix test failure in github.com/lxc/lxd/lxd
- Generate and package gettext translations

* Sun Sep 30 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.5-0.1
- Update to 3.5
- Fix rpath of embedded libdqlite.so
- Finally fix Provides/Requires of embedded libraries

* Mon Sep 17 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.4-0.1
- Update to 3.4
- Run test with 'libsqlite3' tag
- Install headers of embedded libraries
- Don't auto-provide embedded libraries (e.g. sqlite)

* Fri Aug 10 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.3-0.1
- Update to 3.3

* Wed Jun 27 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.2-0.1
- Update to 3.2

* Thu May 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.1-0.3
- Fix build regression with EPEL 7

* Thu May 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.1-0.2
- Fix build error on Fedora 26

* Thu May 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.1-0.1
- Update to 3.1
- Added LXD_SOCKET override to lxd-containers service (mrd@redhat.com)
- Added support for LXD_SOCKET to lxc-to-lxd

* Thu May 10 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.5
- Fix build with golang-1.8.x (e.g. CentOS <=7.4)
- Experimental patch to fix container startup via LXD_SOCKET

* Fri Apr 27 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.4
- Make sure LXD_SOCKET is not set when running %%check

* Tue Apr 24 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.3
- Add upstream patches according to lxd-3.0.0-0ubuntu4
- Add new sub-package lxd-p2c
- Fix lxd.socket path in systemd .service and .socket

* Sun Apr 15 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.2
- Add bundled modules to devel
- Use new LXD_SOCKET option and set it to /run/lxd.socket
- Add upstream patches according to lxd-3.0.0-0ubuntu3

* Mon Apr 02 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.1
- Update to 3.0.0
- Build with bundled go dependencies by default

* Wed Jan 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.21-2
- Fix build with bundled go modules
- Correctly specify scriptlet dependencies
- Run systemd preun scriptlet
- Use /usr/libexec instead of /usr/lib for helper script (GH #11)

* Thu Jan 25 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.21-1
- Update to 2.21 (with patches from 2.21-0ubuntu2)

* Tue Jan 23 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.20-1
- Update to 2.20 (with patches from 2.20-0ubuntu4)
- Major rework of the spec file
- Enable tests

* Fri Nov 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.19-2
- Work-around syntax issue on Fedora 27.
- Runtime detect liblxc version.

* Mon Oct 30 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.19-1
- Update to 2.19.
- Update embedded go-lxc to commit 74fb852
- Drop hard dependency to lxc-2.1
- Various RPM metadata fixes

* Wed Oct 04 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-3
- Link against libsqlite3
- Update go-sqlite3 dependency to fix startup issue on Fedora 26
- Add upstream patches according to lxd-2.18-0ubuntu3

* Thu Sep 28 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-2
- Add upstream patches according to lxd-2.18-0ubuntu2
- Fix xdelta dependency, tighten liblxc version dependency

* Thu Sep 21 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-1
- Version bump to lxd-2.18
- Update embedded go-lxc to commit 89b06ca

* Mon Aug 28 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-3
- Add upstream patches according to lxd-2.17-0ubuntu2

* Thu Aug 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-2
- Fix man pages wrongly added to multiple packages

* Thu Aug 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-1
- Version bump to lxd-2.17

* Wed Jul 26 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.16-1
- Version bump to lxd-2.16

* Wed Jul 19 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-3
- Tweak timeouts for systemd units
- Add upstream patches according to lxd-2.15-0ubuntu6

* Mon Jul 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-2
- Rebuild with latest golang-github-gorilla-websocket

* Mon Jul 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-1
- Version bump to lxd-2.15
- Add upstream patches according to lxd-2.15-0ubuntu4

* Sat Jun 10 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.14-2
- Add some upstream patches according to lxd-2.14-0ubuntu3

* Wed Jun 07 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.14-1
- Version bump to lxd-2.14
- Update embedded go-lxc to commit de2c8bf
- "infinity" for NOFILE doesn't work, set fixed value

* Mon May 01 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.13-1
- Version bump to lxd-2.13
- Add lxc-benchmark to lxd-tools package

* Fri Mar 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.12-1
- Version bump to lxd-2.12
- Update embedded go-lxc to commit 8304875

* Thu Mar 09 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.11-1
- Version bump to lxd-2.11
- Add 'lvm-use-ff-with-vgremove.patch' from lxd-2.11-0ubuntu2

* Tue Mar 07 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.10.1-1
- Version bump to lxd-2.10.1

* Thu Mar 02 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.10-1
- Version bump to lxd-2.10, bump websocket dependency due to build errors

* Fri Feb 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.3-1
- Version bump to lxd-2.9.3

* Tue Feb 21 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.2-1
- Version bump to lxd-2.9.2

* Mon Feb 20 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.1-1
- Version bump to lxd-2.9.1
- Update embedded go-lxc to commit aeb7ce4

* Thu Jan 26 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.8-1
- Version bump to lxd-2.8, fix some gopath requires/provides

* Tue Dec 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.7-1
- Version bump to lxd-2.7, set LXD_DIR to mode 0711
- Add lxc-to-lxd migration script to lxd-tools package

* Wed Dec 14 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-5
- Don't restrict world access to /var/{lib,log}/lxd

* Sun Dec 11 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-4
- Fix cache directory permissions, add more suggested packages

* Sat Dec 10 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-3
- Fix /var/lib/lxd, add shutdown script, new lxd-doc RPM

* Sat Dec 10 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-2
- Big spec file cleanup, fix devel RPM

* Sun Dec 4 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-1
- Initial packaging
