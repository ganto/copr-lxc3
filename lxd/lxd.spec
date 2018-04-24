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
Version:        3.0.0
Release:        0.3%{?dist}
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
# Add patches from lxd-3.0.0-0ubuntu4
Patch0:         lxd-3.0.0-0001-lxc-Fix-mistakenly-hidden-commands.patch
Patch1:         lxd-3.0.0-0002-lxd-main-Add-version-subcommand.patch
Patch2:         lxd-3.0.0-0003-lxd-main-Add-version-subcommand.patch
Patch3:         lxd-3.0.0-0004-i18n-Update-translation-templates.patch
Patch4:         lxd-3.0.0-0005-lxd-migration-Pre-validate-profiles.patch
Patch5:         lxd-3.0.0-0006-client-Improve-remote-operation-errors.patch
Patch6:         lxd-3.0.0-0007-Fix-some-typos-and-wording.patch
Patch7:         lxd-3.0.0-0008-Wording-fix.patch
Patch8:         lxd-3.0.0-0009-lxc-image-Fix-crash-due-to-bad-arg-parsing.patch
Patch9:         lxd-3.0.0-0010-lxd-add-missing-limits.h-include.patch
Patch10:        lxd-3.0.0-0011-lxd-init-Fix-auto-with-network-config.patch
Patch11:        lxd-3.0.0-0012-lxc-Consistent-naming-of-clustering-terms.patch
Patch12:        lxd-3.0.0-0013-i18n-Update-translation-templates.patch
Patch13:        lxd-3.0.0-0014-lxc-file-Fix-pushing-files-to-remote.patch
Patch14:        lxd-3.0.0-0015-lxd-init-Don-t-setup-a-remote-storage-pool-by-defaul.patch
Patch15:        lxd-3.0.0-0016-Fix-lxd-init-failing-to-join-a-cluster-in-interactiv.patch
Patch16:        lxd-3.0.0-0017-lxc-query-Fix-d-and-X.patch
Patch17:        lxd-3.0.0-0018-lxc-help-Make-help-respect-all-too.patch
Patch18:        lxd-3.0.0-0019-Fix-typo-in-help-of-lxc-network.patch
Patch19:        lxd-3.0.0-0020-Properly-filter-node-level-storage-configs-by-pool-I.patch
Patch20:        lxd-3.0.0-0021-i18n-Update-translation-templates.patch
Patch21:        lxd-3.0.0-0022-lxd-init-Consistency.patch
Patch22:        lxd-3.0.0-0023-Make-new-gofmt-happy.patch
Patch23:        lxd-3.0.0-0024-lxc-file-Allow-using-r-to-follow-symlinks.patch
Patch24:        lxd-3.0.0-0025-lxc-config-Fix-adding-trust-cert-on-snap.patch
Patch25:        lxd-3.0.0-0026-lxc-alias-Fix-example-in-help-message.patch
Patch26:        lxd-3.0.0-0027-i18n-Update-translation-templates.patch
Patch27:        lxd-3.0.0-0028-client-Introduce-LXD_SOCKET.patch
Patch28:        lxd-3.0.0-0029-Makefile-Add-a-manifest.patch
Patch29:        lxd-3.0.0-0030-containers-fix-snapshot-deletion.patch
Patch30:        lxd-3.0.0-0031-lxc-init-Add-missing-no-profiles.patch
Patch31:        lxd-3.0.0-0032-i18n-Update-translations.patch
Patch32:        lxd-3.0.0-0033-lxc-file-Fix-pull-target-logic.patch
Patch33:        lxd-3.0.0-0034-doc-Fix-example-in-userns-idmap.patch
Patch34:        lxd-3.0.0-0035-devices-fail-if-Nvidia-device-minor-is-missing.patch
Patch35:        lxd-3.0.0-0036-Add-db.ContainersNodeList.patch
Patch36:        lxd-3.0.0-0037-storage-createContainerMountpoint-fix-perms.patch
Patch37:        lxd-3.0.0-0038-ceph-s-0755-0711-g.patch
Patch38:        lxd-3.0.0-0039-lvm-s-0755-0711-g.patch
Patch39:        lxd-3.0.0-0040-storage-utils-s-0755-0711-g.patch
Patch40:        lxd-3.0.0-0041-zfs-s-0755-0711-g.patch
Patch41:        lxd-3.0.0-0042-patches-add-storage_api_path_permissions.patch
Patch42:        lxd-3.0.0-0043-sys-fs-s-MkdirAll-Mkdir-g.patch
Patch43:        lxd-3.0.0-0044-btrfs-fix-permissions.patch
Patch44:        lxd-3.0.0-0045-Pass-a-logger-to-raft-http.patch
Patch45:        lxd-3.0.0-0046-Add-new-cluster.Promote-function-to-turn-a-non-datab.patch
Patch46:        lxd-3.0.0-0047-Add-new-cluster.Rebalance-function-to-check-if-we-ne.patch
Patch47:        lxd-3.0.0-0048-Notify-the-cluster-leader-after-a-node-removal-so-it.patch
Patch48:        lxd-3.0.0-0049-Add-integration-test.patch
Patch49:        lxd-3.0.0-0050-doc-Tweak-backup.md.patch
Patch50:        lxd-3.0.0-0051-lxd-init-Require-root-for-interactive-cluster-join.patch
Patch51:        lxd-3.0.0-0052-Disable-flaky-unit-tests-for-now.patch
Patch52:        lxd-3.0.0-0053-Log-the-error-that-made-Daemon.Init-fail.patch
Patch53:        lxd-3.0.0-0054-client-Expose-http-URL-in-ConnectionInfo.patch
Patch54:        lxd-3.0.0-0055-lxc-query-Add-support-for-non-JSON-endpoints.patch
# Fix issue with TestEndpoints on Fedora 27
Patch55:        lxd-2.20-000-Fix-TestEndpoints_LocalUnknownUnixGroup-test.patch

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
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/armon/go-metrics))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/armon/go-metrics/circonus))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/armon/go-metrics/datadog))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/armon/go-metrics/prometheus))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/boltdb/bolt))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/boltdb/bolt/cmd/bolt))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite/internal/connection))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite/internal/protocol))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite/internal/registry))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite/internal/replication))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite/internal/trace))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite/internal/transaction))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/dqlite/testdata))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-grpc-sql))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-grpc-sql/internal/protocol))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/custom_func))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/hook))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/limit))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/mod_regexp))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/mod_vtable))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/simple))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/trace))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/_example/vtable))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/go-sqlite3/tool))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/raft-http))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/raft-membership))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/raft-test))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/CanonicalLtd/raft-test/internal/raftext))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/cpuguy83/go-md2man))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/cpuguy83/go-md2man/md2man))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/cpuguy83/go-md2man/vendor/github.com/russross/blackfriday))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/cpuguy83/go-md2man/vendor/github.com/shurcooL/sanitized_anchor_name))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/dustinkirkland/golang-petname))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/dustinkirkland/golang-petname/cmd/petname))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/flosch/pongo2))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/_conformance))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/_conformance/conformance_proto))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/descriptor))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/jsonpb))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/jsonpb/jsonpb_test_proto))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/proto))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/protoc-gen-go))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/protoc-gen-go/descriptor))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/protoc-gen-go/generator))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/protoc-gen-go/grpc))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/protoc-gen-go/plugin))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/protoc-gen-go/testdata))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/protoc-gen-go/testdata/my_test))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/proto/proto3_proto))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/proto/testdata))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/ptypes))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/ptypes/any))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/ptypes/duration))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/ptypes/empty))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/ptypes/struct))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/ptypes/timestamp))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/golang/protobuf/ptypes/wrappers))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gorilla/mux))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gorilla/websocket))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gorilla/websocket/examples/autobahn))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gorilla/websocket/examples/chat))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gorilla/websocket/examples/command))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gorilla/websocket/examples/echo))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gorilla/websocket/examples/filewatch))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gosexy/gettext))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gosexy/gettext/_examples))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/gosexy/gettext/go-xgettext))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/go-immutable-radix))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/golang-lru))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/golang-lru/simplelru))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/go-msgpack/codec))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/raft))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/raft/bench))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/raft-boltdb))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/hashicorp/raft/fuzzy))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/errors))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/bytereplacer))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/cloud/cloudlaunch))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/cloud/google/gceutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/cloud/google/gcsutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/ctxutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/errorutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/fault))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/jsonconfig))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/legal))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/lock))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/net/throttle))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/oauthutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/osutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/readerutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/strutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/syncutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/syncutil/singleflight))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/syncutil/syncdebug))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/types))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/wkfs))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/wkfs/gcs))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/go4/writerutil))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/gomaasapi))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/gomaasapi/example))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/gomaasapi/templates))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/httprequest))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/httprequest/cmd/httprequest-generate-client))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/idmclient))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/idmclient/idmtest))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/idmclient/params))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/idmclient/ussodischarge))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/idmclient/ussologin))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/loggo))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/loggo/example))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/loggo/loggocolor))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/persistent-cookiejar))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/schema))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/arch))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/bzr))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/cache))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/cert))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/clock))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/clock/monotonic))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/debugstatus))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/deque))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/du))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/exec))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/featureflag))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/filepath))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/filestorage))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/fs))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/hash))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/jsonhttp))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/keyvalues))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/mgokv))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/os))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/packaging))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/packaging/commands))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/packaging/config))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/packaging/manager))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/packaging/manager/testing))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/parallel))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/proxy))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/readpass))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/registry))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/series))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/set))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/shell))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/ssh))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/ssh/testing))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/symlink))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/tailer))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/tar))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/uptime))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/voyeur))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/winrm))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/utils/zip))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/version))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/juju/webbrowser))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/julienschmidt/httprouter))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mattn/go-colorable))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mattn/go-colorable/cmd/colorable))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mattn/go-colorable/_example/escape-seq))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mattn/go-colorable/_example/logrus))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mattn/go-colorable/_example/title))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mattn/go-isatty))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mattn/go-runewidth))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/mpvl/subtest))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/olekukonko/tablewriter))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/olekukonko/tablewriter/csv2table))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/pborman/uuid))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/pkg/errors))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/rogpeppe/fastuuid))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/ryanfaerman/fsm))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/spf13/cobra))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/spf13/cobra/cobra))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/spf13/cobra/cobra/cmd))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/spf13/cobra/doc))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/spf13/pflag))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/assert))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/_codegen))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/http))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/mock))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/require))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/suite))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/vendor/github.com/davecgh/go-spew/spew))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/vendor/github.com/pmezard/go-difflib/difflib))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/stretchr/testify/vendor/github.com/stretchr/objx))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/syndtr/gocapability/capability))
Provides:       bundled(golang(%{import_path}/vendor/src/github.com/syndtr/gocapability/capability/enumgen))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/acme))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/acme/autocert))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/argon2))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/bcrypt))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/blake2b))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/blake2s))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/blowfish))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/bn256))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/cast5))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/chacha20poly1305))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/cryptobyte))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/cryptobyte/asn1))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/curve25519))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ed25519))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ed25519/internal/edwards25519))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/hkdf))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/internal/chacha20))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/md4))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/nacl/auth))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/nacl/box))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/nacl/secretbox))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/nacl/sign))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ocsp))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/openpgp))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/openpgp/armor))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/openpgp/clearsign))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/openpgp/elgamal))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/openpgp/errors))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/openpgp/packet))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/openpgp/s2k))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/otr))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/pbkdf2))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/pkcs12))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/pkcs12/internal/rc2))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/poly1305))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ripemd160))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/salsa20))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/salsa20/salsa))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/scrypt))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/sha3))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ssh))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ssh/agent))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ssh/knownhosts))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ssh/terminal))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ssh/test))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/ssh/testdata))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/tea))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/twofish))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/xtea))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/crypto/xts))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/bpf))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/context))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/context/ctxhttp))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/dict))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/dns/dnsmessage))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/html))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/html/atom))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/html/charset))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/http2))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/http2/h2demo))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/http2/h2i))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/http2/hpack))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/http/httpproxy))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/icmp))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/idna))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/internal/iana))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/internal/nettest))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/internal/socket))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/internal/timeseries))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/ipv4))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/ipv6))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/lex/httplex))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/lif))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/nettest))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/netutil))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/proxy))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/publicsuffix))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/route))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/trace))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/webdav))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/webdav/internal/xml))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/websocket))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/net/xsrftoken))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/plan9))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/unix))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/unix/linux))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/windows))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/windows/registry))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/windows/svc))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/windows/svc/debug))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/windows/svc/eventlog))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/windows/svc/example))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/sys/windows/svc/mgr))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/cases))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/cmd/gotext))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/cmd/gotext/examples/extract))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/cmd/gotext/examples/extract_http))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/cmd/gotext/examples/extract_http/pkg))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/cmd/gotext/examples/rewrite))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/collate))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/collate/build))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/collate/tools/colcmp))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/currency))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/date))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/charmap))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/htmlindex))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/ianaindex))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/internal))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/internal/enctest))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/internal/identifier))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/japanese))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/korean))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/simplifiedchinese))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/traditionalchinese))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/unicode))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/encoding/unicode/utf32))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/feature/plural))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/catmsg))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/cldrtree))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/cldrtree/testdata/test1))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/cldrtree/testdata/test2))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/colltab))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/export/idna))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/format))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/gen))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/gen/bitfield))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/language))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/language/compact))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/number))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/stringset))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/tag))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/testtext))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/triegen))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/ucd))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/internal/utf8internal))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/language))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/language/display))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/message))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/message/catalog))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/message/pipeline))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/message/pipeline/testdata/test1))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/number))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/runes))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/search))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/secure))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/secure/bidirule))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/secure/precis))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/transform))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/unicode))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/unicode/bidi))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/unicode/cldr))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/unicode/norm))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/unicode/rangetable))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/unicode/runenames))
Provides:       bundled(golang(%{import_path}/vendor/src/golang.org/x/text/width))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/annotations))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/configchange))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/distribution))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/httpbody))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/label))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/metric))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/monitoredres))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/serviceconfig))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/servicecontrol/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/api/servicemanagement/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/appengine/legacy))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/appengine/logging/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/appengine/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/assistant/embedded/v1alpha1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/assistant/embedded/v1alpha2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/bigtable/admin/cluster/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/bigtable/admin/table/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/bigtable/admin/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/bigtable/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/bigtable/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/bytestream))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/audit))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/bigquery/datatransfer/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/bigquery/logging/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/billing/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/dataproc/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/dataproc/v1beta2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/dialogflow/v2beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/functions/v1beta2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/iot/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/language/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/language/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/language/v1beta2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/location))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/ml/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/oslogin/common))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/oslogin/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/oslogin/v1alpha))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/oslogin/v1beta))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/resourcemanager/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/runtimeconfig/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/speech/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/speech/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/speech/v1p1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/support/common))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/support/v1alpha1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/texttospeech/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/videointelligence/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/videointelligence/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/videointelligence/v1beta2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/videointelligence/v1p1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/vision/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/vision/v1p1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/cloud/vision/v1p2beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/container/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/container/v1alpha1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/container/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/datastore/admin/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/datastore/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/datastore/v1beta3))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/build/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/cloudbuild/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/clouddebugger/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/clouderrorreporting/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/cloudprofiler/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/cloudtrace/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/cloudtrace/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/containeranalysis/v1alpha1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/remoteexecution/v1test))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/remoteworkers/v1test2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/sourcerepo/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/devtools/source/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/example/library/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/firestore/admin/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/firestore/v1beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/genomics/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/genomics/v1alpha2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/iam/admin/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/iam/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/iam/v1/logging))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/logging/type))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/logging/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/longrunning))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/monitoring/v3))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/privacy/dlp/v2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/privacy/dlp/v2beta1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/privacy/dlp/v2beta2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/pubsub/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/pubsub/v1beta2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/rpc/code))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/rpc/errdetails))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/rpc/status))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/spanner/admin/database/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/spanner/admin/instance/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/spanner/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/storagetransfer/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/streetview/publish/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/type/color))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/type/date))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/type/dayofweek))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/type/latlng))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/type/money))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/type/postaladdress))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/type/timeofday))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/googleapis/watcher/v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/protobuf/api))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/protobuf/field_mask))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/protobuf/ptype))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/genproto/protobuf/source_context))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/balancer))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/balancer/base))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/balancer/roundrobin))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/benchmain))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/benchresult))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/grpc_testing))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/latency))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/primitives))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/server))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/stats))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/benchmark/worker))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/codes))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/connectivity))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts/core))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts/core/authinfo))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts/core/conn))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts/core/handshaker))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts/core/handshaker/service))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts/core/proto/grpc_gcp))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/alts/core/testutil))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/credentials/oauth))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/encoding))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/encoding/gzip))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/encoding/proto))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/helloworld/greeter_client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/helloworld/greeter_server))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/helloworld/helloworld))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/helloworld/mock_helloworld))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/route_guide/client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/route_guide/mock_routeguide))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/route_guide/routeguide))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/route_guide/server))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/rpc_errors/client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/examples/rpc_errors/server))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/grpclb))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/grpclb/grpc_lb_v1/messages))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/grpclb/grpc_lb_v1/service))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/grpclog))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/grpclog/glogger))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/health))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/health/grpc_health_v1))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/internal))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/interop))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/interop/alts/client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/interop/alts/server))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/interop/client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/interop/grpc_testing))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/interop/http2))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/interop/server))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/keepalive))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/metadata))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/naming))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/peer))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/reflection))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/reflection/grpc_reflection_v1alpha))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/reflection/grpc_testing))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/reflection/grpc_testingv3))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/resolver))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/resolver/dns))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/resolver/manual))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/resolver/passthrough))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/stats))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/stats/grpc_testing))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/status))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/stress/client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/stress/grpc_testing))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/stress/metrics_client))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/tap))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/test))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/test/bufconn))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/test/codec_perf))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/testdata))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/test/grpc_testing))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/test/leakcheck))
Provides:       bundled(golang(%{import_path}/vendor/src/google.golang.org/grpc/transport))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/errgo.v1))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/httprequest.v1))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/httprequest.v1/cmd/httprequest-generate-client))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/juju/environschema.v1))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/juju/environschema.v1/form))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/juju/environschema.v1/form/cmd/formtest))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/juju/names.v2))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/lxc/go-lxc.v2))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/lxc/go-lxc.v2/examples))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/checkers))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/dbrootkeystore))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/example))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/example/meeting))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/identchecker))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/internal/macaroonpb))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/mgorootkeystore))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakery/postgresrootkeystore))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/bakerytest))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/cmd/bakery-keygen))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/httpbakery))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/httpbakery/agent))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/httpbakery/form))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon-bakery.v2/internal/httputil))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/macaroon.v2))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/mgo.v2))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/mgo.v2/bson))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/mgo.v2/dbtest))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/mgo.v2/internal/json))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/mgo.v2/internal/sasl))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/mgo.v2/internal/scram))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/mgo.v2/txn))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/retry.v1))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/tomb.v2))
Provides:       bundled(golang(%{import_path}/vendor/src/gopkg.in/yaml.v2))
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
%{lua:for i=0,54 do print(string.format("%%patch%u -p1\n", i)) end}
%if 0%{?fedora} == 27
%patch55 -p1
%endif

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

%gotest %{import_path}/lxc
%gotest %{import_path}/lxd
# Cluster test fails
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
* Tue Apr 24 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch>
- Add upstream patches according to lxd-3.0.0-0ubuntu4
- Add new sub-package lxd-p2c
- Fix lxd.socket path in systemd service and socket

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
