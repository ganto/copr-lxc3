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
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -tags="$BUILDTAGS rpm_crashtraceback" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         lxc
%global repo            lxd
# https://github.com/lxc/lxd
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

Name:           lxd
Version:        3.2
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
Source8:        lxd.wrapper
Source9:        lxd.profile
# Fix issue with TestEndpoints on Fedora <= 27
Patch0:         lxd-2.20-000-Fix-TestEndpoints_LocalUnknownUnixGroup-test.patch
# Restore Go-1.8 compatibility of CanonicalLtd/raft-test for CentOS 7
Patch1:         raft-test-618695c-Restore-Go-1.8-compatibility.patch

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:  x86_64 aarch64 ppc64le s390x
%endif

# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

BuildRequires:  help2man
BuildRequires:  libacl-devel
BuildRequires:  pkgconfig(lxc)
BuildRequires:  systemd
# tclsh required by embedded sqlite3 build
BuildRequires:  tcl

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

Provides: bundled(libsqlite3.so.0())

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
Provides:       golang(%{import_path}/lxd/debug) = %{version}-%{release}
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
Provides:       bundled(golang(github.com/armon/go-metrics)) = 58588f401c2cc130a7308a52ca3bc6c0a76db04b
Provides:       bundled(golang(github.com/armon/go-metrics/circonus)) = 58588f401c2cc130a7308a52ca3bc6c0a76db04b
Provides:       bundled(golang(github.com/armon/go-metrics/datadog)) = 58588f401c2cc130a7308a52ca3bc6c0a76db04b
Provides:       bundled(golang(github.com/armon/go-metrics/prometheus)) = 58588f401c2cc130a7308a52ca3bc6c0a76db04b
Provides:       bundled(golang(github.com/boltdb/bolt)) = fd01fc79c553a8e99d512a07e8e0c63d4a3ccfc5
Provides:       bundled(golang(github.com/boltdb/bolt/cmd/bolt)) = fd01fc79c553a8e99d512a07e8e0c63d4a3ccfc5
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/candidtest)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/params)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/ussodischarge)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(github.com/CanonicalLtd/candidclient/ussologin)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/cmd/dqlite)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/internal/connection)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/internal/protocol)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/internal/registry)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/internal/replication)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/internal/store)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/internal/trace)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/internal/transaction)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/recover)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/recover/delete)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/recover/dump)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/dqlite/testdata)) = e5bc052920ea9aabf43aeee5ce3c517289c5a7c6
Provides:       bundled(golang(github.com/CanonicalLtd/go-grpc-sql)) = 72fa8515823be4fdc723721a5423ca6b98ec62c0
Provides:       bundled(golang(github.com/CanonicalLtd/go-grpc-sql/internal/protocol)) = 72fa8515823be4fdc723721a5423ca6b98ec62c0
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/custom_func)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/hook)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/limit)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/mod_regexp)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/mod_vtable)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/simple)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/trace)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/_example/vtable)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/go-sqlite3/tool)) = 4b194c2b1130b08d976c8b85de2be160ad8040af
Provides:       bundled(golang(github.com/CanonicalLtd/raft-http)) = 4c2dd679d3b46c11b250d63ae43467d4c4ab0962
Provides:       bundled(golang(github.com/CanonicalLtd/raft-membership)) = 3846634b0164affd0b3dfba1fdd7f9da6387e501
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test)) = 618695cb5f84b38bad7594076912d8be46b43fed
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/election)) = 618695cb5f84b38bad7594076912d8be46b43fed
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/event)) = 618695cb5f84b38bad7594076912d8be46b43fed
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/fsms)) = 618695cb5f84b38bad7594076912d8be46b43fed
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/logging)) = 618695cb5f84b38bad7594076912d8be46b43fed
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/network)) = 618695cb5f84b38bad7594076912d8be46b43fed
Provides:       bundled(golang(github.com/cpuguy83/go-md2man)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/md2man)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/vendor/github.com/russross/blackfriday)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/vendor/github.com/shurcooL/sanitized_anchor_name)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/dustinkirkland/golang-petname)) = d3c2ba80e75eeef10c5cf2fc76d2c809637376b3
Provides:       bundled(golang(github.com/dustinkirkland/golang-petname/cmd/petname)) = d3c2ba80e75eeef10c5cf2fc76d2c809637376b3
Provides:       bundled(golang(github.com/flosch/pongo2)) = 67f4ff8560dfa2b00920118f228c0a2f68760631
Provides:       bundled(golang(github.com/golang/protobuf/conformance)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/conformance/internal/conformance_proto)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/descriptor)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/jsonpb)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/jsonpb/jsonpb_test_proto)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/proto)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/descriptor)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/generator)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/generator/internal/remap)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/grpc)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/plugin)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/deprecated)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_base)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_extra)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_user)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/grpc)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/import_public)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/import_public/sub)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/fmt)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_a_1)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_a_2)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_b_1)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/multi)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/my_test)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/proto3)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/proto/proto3_proto)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/proto/test_proto)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/ptypes)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/any)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/duration)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/empty)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/struct)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/timestamp)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/wrappers)) = 9f81198da99b79e14d70ca2c3cc1bbe44c6e69b6
Provides:       bundled(golang(github.com/gorilla/mux)) = cb4698366aa625048f3b815af6a0dea8aef9280a
Provides:       bundled(golang(github.com/gorilla/websocket)) = 5ed622c449da6d44c3c8329331ff47a9e5844f71
Provides:       bundled(golang(github.com/gorilla/websocket/examples/autobahn)) = 5ed622c449da6d44c3c8329331ff47a9e5844f71
Provides:       bundled(golang(github.com/gorilla/websocket/examples/chat)) = 5ed622c449da6d44c3c8329331ff47a9e5844f71
Provides:       bundled(golang(github.com/gorilla/websocket/examples/command)) = 5ed622c449da6d44c3c8329331ff47a9e5844f71
Provides:       bundled(golang(github.com/gorilla/websocket/examples/echo)) = 5ed622c449da6d44c3c8329331ff47a9e5844f71
Provides:       bundled(golang(github.com/gorilla/websocket/examples/filewatch)) = 5ed622c449da6d44c3c8329331ff47a9e5844f71
Provides:       bundled(golang(github.com/gosexy/gettext)) = 74466a0a0c4a62fea38f44aa161d4bbfbe79dd6b
Provides:       bundled(golang(github.com/gosexy/gettext/_examples)) = 74466a0a0c4a62fea38f44aa161d4bbfbe79dd6b
Provides:       bundled(golang(github.com/gosexy/gettext/go-xgettext)) = 74466a0a0c4a62fea38f44aa161d4bbfbe79dd6b
Provides:       bundled(golang(github.com/hashicorp/go-immutable-radix)) = 7f3cd4390caab3250a57f30efdb2a65dd7649ecf
Provides:       bundled(golang(github.com/hashicorp/golang-lru)) = 0fb14efe8c47ae851c0034ed7a448854d3d34cf3
Provides:       bundled(golang(github.com/hashicorp/golang-lru/simplelru)) = 0fb14efe8c47ae851c0034ed7a448854d3d34cf3
Provides:       bundled(golang(github.com/hashicorp/go-msgpack/codec)) = fa3f63826f7c23912c15263591e65d54d080b458
Provides:       bundled(golang(github.com/hashicorp/logutils)) = 0dc08b1671f34c4250ce212759ebd880f743d883
Provides:       bundled(golang(github.com/hashicorp/raft)) = a3fb4581fb07b16ecf1c3361580d4bdb17de9d98
Provides:       bundled(golang(github.com/hashicorp/raft/bench)) = a3fb4581fb07b16ecf1c3361580d4bdb17de9d98
Provides:       bundled(golang(github.com/hashicorp/raft-boltdb)) = 6e5ba93211eaf8d9a2ad7e41ffad8c6f160f9fe3
Provides:       bundled(golang(github.com/hashicorp/raft/fuzzy)) = a3fb4581fb07b16ecf1c3361580d4bdb17de9d98
Provides:       bundled(golang(github.com/juju/collections/deque)) = 90152009b5f349bb218a9bf4a6034dd8437c031b
Provides:       bundled(golang(github.com/juju/collections/set)) = 90152009b5f349bb218a9bf4a6034dd8437c031b
Provides:       bundled(golang(github.com/juju/errors)) = c7d06af17c68cd34c835053720b21f6549d9b0ee
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
Provides:       bundled(golang(github.com/juju/gomaasapi)) = abe11904dd8cd40f0777b7704ae60348a876542e
Provides:       bundled(golang(github.com/juju/gomaasapi/example)) = abe11904dd8cd40f0777b7704ae60348a876542e
Provides:       bundled(golang(github.com/juju/gomaasapi/templates)) = abe11904dd8cd40f0777b7704ae60348a876542e
Provides:       bundled(golang(github.com/juju/httprequest)) = 77d36ac4b71a6095506c0617d5881846478558cb
Provides:       bundled(golang(github.com/juju/httprequest/cmd/httprequest-generate-client)) = 77d36ac4b71a6095506c0617d5881846478558cb
Provides:       bundled(golang(github.com/juju/loggo)) = 584905176618da46b895b176c721b02c476b6993
Provides:       bundled(golang(github.com/juju/loggo/example)) = 584905176618da46b895b176c721b02c476b6993
Provides:       bundled(golang(github.com/juju/loggo/loggocolor)) = 584905176618da46b895b176c721b02c476b6993
Provides:       bundled(golang(github.com/juju/persistent-cookiejar)) = d5e5a8405ef9633c84af42fbcc734ec8dd73c198
Provides:       bundled(golang(github.com/juju/schema)) = e4f08199aa80d3194008c0bd2e14ef5edc0e6be6
Provides:       bundled(golang(github.com/juju/utils)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/arch)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/bzr)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/cache)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/cert)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/clock)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/clock/monotonic)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/debugstatus)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/deque)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/du)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/exec)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/featureflag)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/filepath)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/filestorage)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/fs)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/hash)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/jsonhttp)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/keyvalues)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/mgokv)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/os)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/parallel)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/proxy)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/readpass)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/registry)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/series)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/set)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/shell)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/ssh)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/ssh/testing)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/symlink)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/tailer)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/tar)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/uptime)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/voyeur)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/winrm)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/utils/zip)) = c746c6e86f4fb2a04bc08d66b7a0f7e900d9cbab
Provides:       bundled(golang(github.com/juju/version)) = b64dbd566305c836274f0268fa59183a52906b36
Provides:       bundled(golang(github.com/juju/webbrowser)) = 54b8c57083b4afb7dc75da7f13e2967b2606a507
Provides:       bundled(golang(github.com/julienschmidt/httprouter)) = adbc77eec0d91467376ca515bc3a14b8434d0f18
Provides:       bundled(golang(github.com/mattn/go-colorable)) = efa589957cd060542a26d2dd7832fd6a6c6c3ade
Provides:       bundled(golang(github.com/mattn/go-colorable/cmd/colorable)) = efa589957cd060542a26d2dd7832fd6a6c6c3ade
Provides:       bundled(golang(github.com/mattn/go-colorable/_example/escape-seq)) = efa589957cd060542a26d2dd7832fd6a6c6c3ade
Provides:       bundled(golang(github.com/mattn/go-colorable/_example/logrus)) = efa589957cd060542a26d2dd7832fd6a6c6c3ade
Provides:       bundled(golang(github.com/mattn/go-colorable/_example/title)) = efa589957cd060542a26d2dd7832fd6a6c6c3ade
Provides:       bundled(golang(github.com/mattn/go-isatty)) = 6ca4dbf54d38eea1a992b3c722a76a5d1c4cb25c
Provides:       bundled(golang(github.com/mattn/go-runewidth)) = ce7b0b5c7b45a81508558cd1dba6bb1e4ddb51bb
Provides:       bundled(golang(github.com/mpvl/subtest)) = f6e4cfd4b9ea1beb9fb5d53afba8c30804a02ae7
Provides:       bundled(golang(github.com/olekukonko/tablewriter)) = d4647c9c7a84d847478d890b816b7d8b62b0b279
Provides:       bundled(golang(github.com/olekukonko/tablewriter/csv2table)) = d4647c9c7a84d847478d890b816b7d8b62b0b279
Provides:       bundled(golang(github.com/pborman/uuid)) = c65b2f87fee37d1c7854c9164a450713c28d50cd
Provides:       bundled(golang(github.com/pkg/errors)) = 816c9085562cd7ee03e7f8188a1cfd942858cded
Provides:       bundled(golang(github.com/rogpeppe/fastuuid)) = 6724a57986aff9bff1a1770e9347036def7c89f6
Provides:       bundled(golang(github.com/ryanfaerman/fsm)) = 3dc1bc0980272fd56d81167a48a641dab8356e29
Provides:       bundled(golang(github.com/spf13/cobra)) = 1e58aa3361fd650121dceeedc399e7189c05674a
Provides:       bundled(golang(github.com/spf13/cobra/cobra)) = 1e58aa3361fd650121dceeedc399e7189c05674a
Provides:       bundled(golang(github.com/spf13/cobra/cobra/cmd)) = 1e58aa3361fd650121dceeedc399e7189c05674a
Provides:       bundled(golang(github.com/spf13/cobra/doc)) = 1e58aa3361fd650121dceeedc399e7189c05674a
Provides:       bundled(golang(github.com/spf13/pflag)) = 3ebe029320b2676d667ae88da602a5f854788a8a
Provides:       bundled(golang(github.com/stretchr/testify)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/assert)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/_codegen)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/http)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/mock)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/require)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/suite)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/vendor/github.com/davecgh/go-spew/spew)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/vendor/github.com/pmezard/go-difflib/difflib)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/stretchr/testify/vendor/github.com/stretchr/objx)) = f35b8ab0b5a2cef36673838d662e249dd9c94686
Provides:       bundled(golang(github.com/syndtr/gocapability/capability)) = 33e07d32887e1e06b7c025f27ce52f62c7990bc0
Provides:       bundled(golang(github.com/syndtr/gocapability/capability/enumgen)) = 33e07d32887e1e06b7c025f27ce52f62c7990bc0
Provides:       bundled(golang(golang.org/x/crypto/acme)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/acme/autocert)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/argon2)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/bcrypt)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/blake2b)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/blake2s)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/blowfish)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/bn256)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/cast5)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/chacha20poly1305)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte/asn1)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/curve25519)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ed25519)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ed25519/internal/edwards25519)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/hkdf)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/internal/chacha20)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/internal/subtle)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/md4)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/nacl/auth)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/nacl/box)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/nacl/secretbox)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/nacl/sign)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ocsp)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/openpgp)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/openpgp/armor)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/openpgp/clearsign)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/openpgp/elgamal)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/openpgp/errors)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/openpgp/packet)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/openpgp/s2k)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/otr)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/pbkdf2)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/pkcs12)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/pkcs12/internal/rc2)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/poly1305)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ripemd160)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/salsa20)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/salsa20/salsa)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/scrypt)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/sha3)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ssh)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ssh/agent)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ssh/knownhosts)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ssh/terminal)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ssh/test)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/ssh/testdata)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/tea)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/twofish)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/xtea)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/crypto/xts)) = a49355c7e3f8fe157a85be2f77e6e269a0f89602
Provides:       bundled(golang(golang.org/x/net/bpf)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/context)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/context/ctxhttp)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/dict)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/dns/dnsmessage)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/html)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/html/atom)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/html/charset)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/http2)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/http2/h2demo)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/http2/h2i)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/http2/hpack)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/http/httpguts)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/http/httpproxy)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/icmp)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/idna)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/internal/iana)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/internal/nettest)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/internal/socket)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/internal/socks)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/internal/sockstest)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/internal/timeseries)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/ipv4)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/ipv6)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/lif)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/nettest)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/netutil)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/proxy)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/publicsuffix)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/route)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/trace)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/webdav)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/webdav/internal/xml)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/websocket)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/net/xsrftoken)) = afe8f62b1d6bbd81f31868121a50b06d8188e1f9
Provides:       bundled(golang(golang.org/x/sys/cpu)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/plan9)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/unix)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/unix/linux)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/windows)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/windows/registry)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/windows/svc)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/windows/svc/debug)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/windows/svc/eventlog)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/windows/svc/example)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/sys/windows/svc/mgr)) = ad87a3a340fa7f3bed189293fbfa7a9b7e021ae1
Provides:       bundled(golang(golang.org/x/text)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/cases)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/cmd/gotext)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/extract)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/extract_http)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/extract_http/pkg)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/rewrite)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/collate)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/collate/build)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/collate/tools/colcmp)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/currency)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/date)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/charmap)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/htmlindex)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/ianaindex)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/internal)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/internal/enctest)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/internal/identifier)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/japanese)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/korean)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/simplifiedchinese)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/traditionalchinese)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/unicode)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/encoding/unicode/utf32)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/feature/plural)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/catmsg)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/cldrtree)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/cldrtree/testdata/test1)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/cldrtree/testdata/test2)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/colltab)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/export/idna)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/format)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/gen)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/gen/bitfield)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/language)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/language/compact)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/number)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/stringset)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/tag)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/testtext)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/triegen)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/ucd)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/internal/utf8internal)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/language)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/language/display)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/message)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/message/catalog)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/message/pipeline)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/message/pipeline/testdata/ssa)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/message/pipeline/testdata/test1)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/number)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/runes)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/search)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/secure)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/secure/bidirule)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/secure/precis)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/transform)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/unicode)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/unicode/bidi)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/unicode/cldr)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/unicode/norm)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/unicode/rangetable)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/unicode/runenames)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(golang.org/x/text/width)) = 5cec4b58c438bd98288aeb248bab2c1840713d21
Provides:       bundled(golang(google.golang.org/genproto)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/annotations)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/configchange)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/distribution)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/httpbody)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/label)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/metric)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/monitoredres)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/serviceconfig)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/servicecontrol/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/servicemanagement/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/appengine/legacy)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/appengine/logging/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/appengine/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/assistant/embedded/v1alpha1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/assistant/embedded/v1alpha2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/admin/cluster/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/admin/table/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/admin/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bytestream)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/audit)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/bigquery/datatransfer/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/bigquery/logging/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/billing/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dataproc/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dataproc/v1beta2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dialogflow/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dialogflow/v2beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/functions/v1beta2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/iot/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/language/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/language/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/language/v1beta2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/location)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/ml/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/common)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/v1alpha)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/v1beta)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/redis/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/resourcemanager/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/runtimeconfig/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/speech/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/speech/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/speech/v1p1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/support/common)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/support/v1alpha1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/tasks/v2beta2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/texttospeech/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/texttospeech/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1beta2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1p1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/vision/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/vision/v1p1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/vision/v1p2beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/websecurityscanner/v1alpha)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/container/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/container/v1alpha1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/container/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/admin/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/admin/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/v1beta3)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/build/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudbuild/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/clouddebugger/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/clouderrorreporting/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudprofiler/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudtrace/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudtrace/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/containeranalysis/v1alpha1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/remoteexecution/v1test)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/remoteworkers/v1test2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/sourcerepo/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/source/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/example/library/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/firestore/admin/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/firestore/v1beta1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/genomics/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/genomics/v1alpha2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/home/graph/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/iam/admin/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/iam/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/iam/v1/logging)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/logging/type)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/logging/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/longrunning)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/monitoring/v3)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/privacy/dlp/v2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/pubsub/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/pubsub/v1beta2)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/rpc/code)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/rpc/errdetails)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/rpc/status)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/spanner/admin/database/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/spanner/admin/instance/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/spanner/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/storagetransfer/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/streetview/publish/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/color)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/date)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/dayofweek)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/latlng)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/money)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/postaladdress)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/timeofday)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/googleapis/watcher/v1)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/protobuf/api)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/protobuf/field_mask)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/protobuf/ptype)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/genproto/protobuf/source_context)) = 32ee49c4dd805befd833990acba36cb75042378c
Provides:       bundled(golang(google.golang.org/grpc)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/balancer)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/balancer/base)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/balancer/grpclb)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/balancer/grpclb/grpc_lb_v1)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/balancer/roundrobin)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/benchmain)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/benchresult)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/grpc_testing)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/latency)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/primitives)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/server)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/stats)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/benchmark/worker)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/channelz/grpc_channelz_v1)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/channelz/service)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/codes)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/connectivity)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/authinfo)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/conn)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/handshaker)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/handshaker/service)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/proto/grpc_gcp)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/testutil)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/credentials/oauth)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/encoding)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/encoding/gzip)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/encoding/proto)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/greeter_client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/greeter_server)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/helloworld)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/mock_helloworld)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/oauth/client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/oauth/server)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/mock_routeguide)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/routeguide)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/server)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/rpc_errors/client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/examples/rpc_errors/server)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/grpclog)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/grpclog/glogger)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/health)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/health/grpc_health_v1)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/internal)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/internal/backoff)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/internal/channelz)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/internal/grpcrand)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/internal/leakcheck)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/interop)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/interop/alts/client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/interop/alts/server)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/interop/client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/interop/grpc_testing)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/interop/http2)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/interop/server)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/keepalive)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/metadata)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/naming)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/peer)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/reflection)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/reflection/grpc_reflection_v1alpha)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/reflection/grpc_testing)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/reflection/grpc_testingv3)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/resolver)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/resolver/dns)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/resolver/manual)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/resolver/passthrough)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/stats)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/stats/grpc_testing)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/status)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/stress/client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/stress/grpc_testing)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/stress/metrics_client)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/tap)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/test)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/test/bufconn)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/test/codec_perf)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/testdata)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/test/grpc_testing)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(google.golang.org/grpc/transport)) = ba63e52faf1676ef8bb26b6e0ba5acf78ff3b8e8
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/candidtest)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/params)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/ussodischarge)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/ussologin)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/errgo.v1)) = c17903c6b19d5dedb9cfba9fa314c7fae63e554f
Provides:       bundled(golang(gopkg.in/httprequest.v1)) = 1a21782420ea13c3c6fb1d03578f446b3248edb1
Provides:       bundled(golang(gopkg.in/httprequest.v1/cmd/httprequest-generate-client)) = 1a21782420ea13c3c6fb1d03578f446b3248edb1
Provides:       bundled(golang(gopkg.in/juju/environschema.v1)) = 7359fc7857abe2b11b5b3e23811a9c64cb6b01e0
Provides:       bundled(golang(gopkg.in/juju/environschema.v1/form)) = 7359fc7857abe2b11b5b3e23811a9c64cb6b01e0
Provides:       bundled(golang(gopkg.in/juju/environschema.v1/form/cmd/formtest)) = 7359fc7857abe2b11b5b3e23811a9c64cb6b01e0
Provides:       bundled(golang(gopkg.in/juju/names.v2)) = fd59336b4621bc2a70bf96d9e2f49954115ad19b
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2)) = 1c13b43ccb43defbf04a8b4b931e4bb18fd481e6
Provides:       bundled(golang(gopkg.in/lxc/go-lxc.v2/examples)) = 1c13b43ccb43defbf04a8b4b931e4bb18fd481e6
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/checkers)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/dbrootkeystore)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/example)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/example/meeting)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/internal/macaroonpb)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/mgorootkeystore)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakery/postgresrootkeystore)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/bakerytest)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/cmd/bakery-keygen)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/httpbakery)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/httpbakery/agent)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/httpbakery/form)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon-bakery.v2/internal/httputil)) = 94012773d2874a067572bd16d7d11ae02968b47b
Provides:       bundled(golang(gopkg.in/macaroon.v2)) = bed2a428da6e56d950bed5b41fcbae3141e5b0d0
Provides:       bundled(golang(gopkg.in/mgo.v2)) = 3f83fa5005286a7fe593b055f0d7771a7dce4655
Provides:       bundled(golang(gopkg.in/mgo.v2/bson)) = 3f83fa5005286a7fe593b055f0d7771a7dce4655
Provides:       bundled(golang(gopkg.in/mgo.v2/dbtest)) = 3f83fa5005286a7fe593b055f0d7771a7dce4655
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/json)) = 3f83fa5005286a7fe593b055f0d7771a7dce4655
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/sasl)) = 3f83fa5005286a7fe593b055f0d7771a7dce4655
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/scram)) = 3f83fa5005286a7fe593b055f0d7771a7dce4655
Provides:       bundled(golang(gopkg.in/mgo.v2/txn)) = 3f83fa5005286a7fe593b055f0d7771a7dce4655
Provides:       bundled(golang(gopkg.in/retry.v1)) = 2d7c7c65cc71d024968d9ff4385d5e7ad3a83fcc
Provides:       bundled(golang(gopkg.in/tomb.v2)) = d5d1b5820637886def9eef33e03a27a9f166942c
Provides:       bundled(golang(gopkg.in/yaml.v2)) = 5420a8b6744d3b0345ab293f6fcba19c978f1183
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

%description client
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the command line client.

%package tools
Summary:        Container hypervisor based on LXC - Extra Tools

%if 0%{?rhel}
BuildRequires:  python34-lxc
Requires:       python34-lxc
%else
BuildRequires:  python3-lxc
Requires:       python3-lxc
%endif

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

%if 0%{?fedora} && 0%{?fedora} < 28
%patch0 -p1
%endif

pushd dist/src/github.com/CanonicalLtd/raft-test
%patch1 -p1
popd

%build
%if 0%{?with_bundled}
# build embedded libsqlite3
pushd dist/sqlite
%configure --enable-replication
make %{?_smp_mflags}
popd
export CGO_CPPFLAGS="-I$(pwd)/dist/sqlite"
export CGO_LDFLAGS="-L$(pwd)/dist/sqlite/.libs"

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

# avoid error when linking lxd: "flag provided but not defined: -Wl,-z,relro"
unset LDFLAGS

BUILDTAGS="libsqlite3" %gobuild -o _bin/lxd %{import_path}/lxd
%gobuild -o _bin/lxc %{import_path}/lxc
%gobuild -o _bin/fuidshift %{import_path}/fuidshift
%gobuild -o _bin/lxd-benchmark %{import_path}/lxd-benchmark
%gobuild -o _bin/lxd-p2c %{import_path}/lxd-p2c

# generate man-pages
LD_LIBRARY_PATH=dist/sqlite/.libs _bin/lxd manpage .
_bin/lxc manpage .
help2man _bin/fuidshift -n "uid/gid shifter" --no-info > fuidshift.1
help2man _bin/lxd-benchmark -n "The container lightervisor - benchmark" --no-info --version-string=%{version} --no-discard-stderr > lxd-benchmark.1
help2man _bin/lxd-p2c -n "Physical to container migration tool" --no-info --version-string=%{version} > lxd-p2c.1
help2man scripts/lxc-to-lxd -n "Convert LXC containers to LXD" --no-info --version-string=%{version} > lxc-to-lxd.1

%install
# install binaries
install -D -p -m 0755 _bin/lxc %{buildroot}%{_bindir}/lxc
install -D -p -m 0755 _bin/fuidshift %{buildroot}%{_bindir}/fuidshift
install -D -p -m 0755 _bin/lxd-benchmark %{buildroot}%{_bindir}/lxd-benchmark
install -D -p -m 0755 _bin/lxd-p2c %{buildroot}%{_bindir}/lxd-p2c
install -D -p -m 0755 _bin/lxd %{buildroot}%{_libexecdir}/%{name}/lxd

# install extra script
install -D -p -m 0755 scripts/lxc-to-lxd %{buildroot}%{_bindir}/lxc-to-lxd

# extra configs
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxd
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/lxd
install -D -p -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysctl.d/10-lxd-inotify.conf
install -D -p -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/profile.d/lxd.sh

# install bash completion
install -D -p -m 0644 scripts/bash/lxd-client %{buildroot}%{_datadir}/bash-completion/completions/lxd-client

# install systemd units
install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/

# install wrapper
install -D -p -m 0755 %{SOURCE6} %{buildroot}%{_libexecdir}/%{name}
install -D -p -m 0755 %{SOURCE8} %{buildroot}%{_bindir}/lxd

# install custom libsqlite3
install -d -m 0755 %{buildroot}%{_libdir}/%{name}
cp -Pp dist/sqlite/.libs/libsqlite3.so* %{buildroot}%{_libdir}/%{name}/

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

# source codes for building projects
%if 0%{?with_devel}
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

%if ! 0%{?gotest:1}
%global gotest go test
%endif

# Tests must ignore potential LXD_SOCKET from environment
unset LXD_SOCKET

%gotest %{import_path}/lxc
%gotest %{import_path}/lxd
# Cluster test fails, see ganto/copr-lxc3#7
#%%gotest %%{import_path}/lxd/cluster
%gotest %{import_path}/lxd/config
%gotest %{import_path}/lxd/db
%gotest %{import_path}/lxd/db/cluster
%gotest %{import_path}/lxd/db/node
%gotest %{import_path}/lxd/db/query
%gotest %{import_path}/lxd/db/schema
%gotest %{import_path}/lxd/debug
%gotest %{import_path}/lxd/endpoints
%gotest %{import_path}/lxd/node
%gotest %{import_path}/lxd/task
%gotest %{import_path}/lxd/types
%gotest %{import_path}/lxd/util
%gotest %{import_path}/shared
%gotest %{import_path}/shared/idmap
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

%files client
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
