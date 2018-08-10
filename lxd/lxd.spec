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
Version:        3.3
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
Provides:       bundled(golang(github.com/armon/go-metrics)) = 3c58d8115a78a6879e5df75ae900846768d36895
Provides:       bundled(golang(github.com/armon/go-metrics/circonus)) = 3c58d8115a78a6879e5df75ae900846768d36895
Provides:       bundled(golang(github.com/armon/go-metrics/datadog)) = 3c58d8115a78a6879e5df75ae900846768d36895
Provides:       bundled(golang(github.com/armon/go-metrics/prometheus)) = 3c58d8115a78a6879e5df75ae900846768d36895
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
Provides:       bundled(golang(github.com/CanonicalLtd/go-grpc-sql)) = 181d263025fb02a680c1726752eb27f3a2154e26
Provides:       bundled(golang(github.com/CanonicalLtd/go-grpc-sql/internal/protocol)) = 181d263025fb02a680c1726752eb27f3a2154e26
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
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/election)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/event)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/fsms)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/logging)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/CanonicalLtd/raft-test/internal/network)) = c3345b5e43c2b542007a11093afbbfecedd41648
Provides:       bundled(golang(github.com/cpuguy83/go-md2man)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/md2man)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/vendor/github.com/russross/blackfriday)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/vendor/github.com/shurcooL/sanitized_anchor_name)) = 691ee98543af2f262f35fbb54bdd42f00b9b9cc5
Provides:       bundled(golang(github.com/dustinkirkland/golang-petname)) = d3c2ba80e75eeef10c5cf2fc76d2c809637376b3
Provides:       bundled(golang(github.com/dustinkirkland/golang-petname/cmd/petname)) = d3c2ba80e75eeef10c5cf2fc76d2c809637376b3
Provides:       bundled(golang(github.com/flosch/pongo2)) = 67f4ff8560dfa2b00920118f228c0a2f68760631
Provides:       bundled(golang(github.com/golang/protobuf/conformance)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/conformance/internal/conformance_proto)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/descriptor)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/jsonpb)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/jsonpb/jsonpb_test_proto)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/proto)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/descriptor)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/generator)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/generator/internal/remap)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/grpc)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/plugin)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/deprecated)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_base)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_extra)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/extension_user)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/grpc)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/import_public)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/import_public/sub)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/fmt)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_a_1)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_a_2)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/imports/test_b_1)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/multi)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/my_test)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/protoc-gen-go/testdata/proto3)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/proto/proto3_proto)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/proto/test_proto)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/ptypes)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/any)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/duration)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/empty)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/struct)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/timestamp)) = 93b26e6a70e37abb14f2f88194949312b0592a84
Provides:       bundled(golang(github.com/golang/protobuf/ptypes/wrappers)) = 93b26e6a70e37abb14f2f88194949312b0592a84
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
Provides:       bundled(golang(github.com/juju/collections/deque)) = 9be91dc79b7c185fa8b08e7ceceee40562055c83
Provides:       bundled(golang(github.com/juju/collections/set)) = 9be91dc79b7c185fa8b08e7ceceee40562055c83
Provides:       bundled(golang(github.com/juju/errors)) = 812b06ada1776ad4dd95d575e18ffffe3a9ac34a
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
Provides:       bundled(golang(github.com/julienschmidt/httprouter)) = 348b672cd90d8190f8240323e372ecd1e66b59dc
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
Provides:       bundled(golang(github.com/spf13/cobra)) = 7c4570c3ebeb8129a1f7456d0908a8b676b6f9f1
Provides:       bundled(golang(github.com/spf13/cobra/cobra)) = 7c4570c3ebeb8129a1f7456d0908a8b676b6f9f1
Provides:       bundled(golang(github.com/spf13/cobra/cobra/cmd)) = 7c4570c3ebeb8129a1f7456d0908a8b676b6f9f1
Provides:       bundled(golang(github.com/spf13/cobra/doc)) = 7c4570c3ebeb8129a1f7456d0908a8b676b6f9f1
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
Provides:       bundled(golang(golang.org/x/crypto/acme)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/acme/autocert)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/acme/autocert/internal/acmetest)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/argon2)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/bcrypt)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/blake2b)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/blake2s)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/blowfish)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/bn256)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/cast5)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/chacha20poly1305)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte/asn1)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/curve25519)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ed25519)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ed25519/internal/edwards25519)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/hkdf)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/internal/chacha20)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/internal/subtle)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/md4)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/nacl/auth)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/nacl/box)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/nacl/secretbox)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/nacl/sign)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ocsp)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/openpgp)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/armor)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/clearsign)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/elgamal)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/errors)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/packet)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/openpgp/s2k)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/otr)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/pbkdf2)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/pkcs12)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/pkcs12/internal/rc2)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/poly1305)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ripemd160)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/salsa20)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/salsa20/salsa)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/scrypt)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/sha3)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ssh)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ssh/agent)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ssh/knownhosts)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ssh/terminal)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ssh/test)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/ssh/testdata)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/tea)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/twofish)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/xtea)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/crypto/xts)) = c126467f60eb25f8f27e5a981f32a87e3965053f
Provides:       bundled(golang(golang.org/x/net/bpf)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/context)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/context/ctxhttp)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/dict)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/dns/dnsmessage)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/html)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/html/atom)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/html/charset)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/http2)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/http2/h2demo)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/http2/h2i)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/http2/hpack)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/http/httpguts)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/http/httpproxy)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/icmp)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/idna)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/internal/iana)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/internal/nettest)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/internal/socket)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/internal/socks)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/internal/sockstest)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/internal/timeseries)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/ipv4)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/ipv6)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/lif)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/nettest)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/netutil)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/proxy)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/publicsuffix)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/route)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/trace)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/webdav)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/webdav/internal/xml)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/websocket)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/net/xsrftoken)) = 3673e40ba22529d22c3fd7c93e97b0ce50fa7bdd
Provides:       bundled(golang(golang.org/x/sys/cpu)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/plan9)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/unix)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/unix/linux)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/windows)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/windows/registry)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/windows/svc)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/windows/svc/debug)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/windows/svc/eventlog)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/windows/svc/example)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/sys/windows/svc/mgr)) = e072cadbbdc8dd3d3ffa82b8b4b9304c261d9311
Provides:       bundled(golang(golang.org/x/text)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/cases)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/cmd/gotext)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/extract)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/extract_http)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/extract_http/pkg)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/cmd/gotext/examples/rewrite)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/collate)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/collate/build)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/collate/tools/colcmp)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/currency)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/date)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/charmap)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/htmlindex)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/ianaindex)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/internal)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/internal/enctest)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/internal/identifier)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/japanese)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/korean)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/simplifiedchinese)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/traditionalchinese)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/unicode)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/encoding/unicode/utf32)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/feature/plural)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/catmsg)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/cldrtree)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/cldrtree/testdata/test1)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/cldrtree/testdata/test2)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/colltab)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/export/idna)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/format)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/gen)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/gen/bitfield)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/language)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/language/compact)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/number)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/stringset)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/tag)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/testtext)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/triegen)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/ucd)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/internal/utf8internal)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/language)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/language/display)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/message)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/message/catalog)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/message/pipeline)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/message/pipeline/testdata/ssa)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/message/pipeline/testdata/test1)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/number)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/runes)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/search)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/secure)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/secure/bidirule)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/secure/precis)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/transform)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/unicode)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/unicode/bidi)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/unicode/cldr)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/unicode/norm)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/unicode/rangetable)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/unicode/runenames)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(golang.org/x/text/width)) = 0605a8320aceb4207a5fb3521281e17ec2075476
Provides:       bundled(golang(google.golang.org/genproto)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/annotations)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/configchange)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/distribution)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/httpbody)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/label)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/metric)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/monitoredres)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/serviceconfig)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/servicecontrol/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/api/servicemanagement/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/appengine/legacy)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/appengine/logging/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/appengine/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/assistant/embedded/v1alpha1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/assistant/embedded/v1alpha2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/admin/cluster/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/admin/table/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/admin/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bigtable/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/bytestream)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/audit)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/automl/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/bigquery/datatransfer/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/bigquery/logging/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/billing/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dataproc/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dataproc/v1beta2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dialogflow/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/dialogflow/v2beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/functions/v1beta2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/iot/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/kms/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/language/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/language/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/language/v1beta2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/location)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/ml/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/common)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/v1alpha)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/oslogin/v1beta)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/redis/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/resourcemanager/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/runtimeconfig/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/speech/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/speech/v1p1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/support/common)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/support/v1alpha1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/tasks/v2beta2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/texttospeech/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/texttospeech/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1beta2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/videointelligence/v1p1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/vision/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/vision/v1p1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/vision/v1p2beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/vision/v1p3beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/cloud/websecurityscanner/v1alpha)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/container/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/container/v1alpha1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/container/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/admin/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/admin/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/datastore/v1beta3)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/build/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudbuild/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/clouddebugger/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/clouderrorreporting/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudprofiler/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudtrace/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/cloudtrace/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/containeranalysis/v1alpha1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/remoteexecution/v1test)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/remoteworkers/v1test2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/resultstore/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/sourcerepo/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/devtools/source/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/example/library/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/firestore/admin/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/firestore/v1beta1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/genomics/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/genomics/v1alpha2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/home/graph/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/iam/admin/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/iam/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/iam/v1/logging)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/logging/type)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/logging/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/longrunning)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/monitoring/v3)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/privacy/dlp/v2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/pubsub/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/pubsub/v1beta2)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/rpc/code)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/rpc/errdetails)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/rpc/status)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/spanner/admin/database/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/spanner/admin/instance/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/spanner/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/storagetransfer/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/streetview/publish/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/color)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/date)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/dayofweek)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/latlng)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/money)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/postaladdress)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/type/timeofday)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/googleapis/watcher/v1)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/protobuf/api)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/protobuf/field_mask)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/protobuf/ptype)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/genproto/protobuf/source_context)) = 2a72893556e4d1f6c795a4c039314c9fa751eedb
Provides:       bundled(golang(google.golang.org/grpc)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/balancer)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/balancer/base)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/balancer/grpclb)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/balancer/grpclb/grpc_lb_v1)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/balancer/roundrobin)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/benchmain)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/benchresult)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/grpc_testing)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/latency)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/primitives)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/server)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/stats)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/benchmark/worker)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/channelz/grpc_channelz_v1)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/channelz/service)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/codes)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/connectivity)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/authinfo)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/conn)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/handshaker)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/handshaker/service)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/proto/grpc_gcp)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/alts/core/testutil)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/credentials/oauth)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/encoding)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/encoding/gzip)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/encoding/proto)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/greeter_client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/greeter_server)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/helloworld)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/helloworld/mock_helloworld)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/oauth/client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/oauth/server)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/mock_routeguide)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/routeguide)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/route_guide/server)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/rpc_errors/client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/examples/rpc_errors/server)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/grpclog)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/grpclog/glogger)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/health)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/health/grpc_health_v1)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal/backoff)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal/channelz)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal/envconfig)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal/grpcrand)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal/leakcheck)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal/syscall)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/internal/transport)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/interop)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/interop/alts/client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/interop/alts/server)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/interop/client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/interop/grpc_testing)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/interop/http2)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/interop/server)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/keepalive)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/metadata)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/naming)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/peer)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/reflection)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/reflection/grpc_reflection_v1alpha)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/reflection/grpc_testing)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/reflection/grpc_testingv3)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/resolver)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/resolver/dns)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/resolver/manual)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/resolver/passthrough)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/stats)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/stats/grpc_testing)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/status)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/stress/client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/stress/grpc_testing)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/stress/metrics_client)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/tap)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/test)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/test/bufconn)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/test/codec_perf)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/testdata)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(google.golang.org/grpc/test/grpc_testing)) = 804c2a905125ada0c64a347eab5d09d0ad31895e
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/candidtest)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/params)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/ussodischarge)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/CanonicalLtd/candidclient.v1/ussologin)) = 6504df157e74a5f4b54dd720e5352e164e0f1882
Provides:       bundled(golang(gopkg.in/errgo.v1)) = c17903c6b19d5dedb9cfba9fa314c7fae63e554f
Provides:       bundled(golang(gopkg.in/httprequest.v1)) = a1015531595ff2ed1a0c126b55da352e6923eaac
Provides:       bundled(golang(gopkg.in/httprequest.v1/cmd/httprequest-generate-client)) = a1015531595ff2ed1a0c126b55da352e6923eaac
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
Provides:       bundled(golang(gopkg.in/mgo.v2)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/bson)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/dbtest)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/json)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/sasl)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/internal/scram)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/mgo.v2/txn)) = 9856a29383ce1c59f308dd1cf0363a79b5bef6b5
Provides:       bundled(golang(gopkg.in/retry.v1)) = a39ed324609b84adb77c705baa0909b409fbafcd
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
%gobuild -o _bin/lxc-to-lxd %{import_path}/lxc-to-lxd

# generate man-pages
LD_LIBRARY_PATH=dist/sqlite/.libs _bin/lxd manpage .
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
install -D -p -m 0755 _bin/lxd %{buildroot}%{_libexecdir}/%{name}/lxd
install -D -p -m 0755 _bin/lxc-to-lxd %{buildroot}%{_bindir}/lxc-to-lxd

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
# lxc-to-lxd test fails, see ganto/copr-lxc3#10
#%%gotest %%{import_path}/lxc-to-lxd
%gotest %{import_path}/lxd
# Cluster test fails, see ganto/copr-lxc3#7
#%%gotest %%{import_path}/lxd/cluster
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
