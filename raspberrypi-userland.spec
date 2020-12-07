%global commit0 093b30bbc2fd083d68cc3ee07e6e555c6e592d11
%global date 20201130
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           raspberrypi-userland
Version:        1.0.0
Release:        2.%{date}git%{shortcommit0}%{?dist}
Summary:        ARM side libraries for interfacing to Raspberry Pi GPU
License:        BSD
URL:            https://www.raspberrypi.org/
ExclusiveArch:  armv7hl aarch64

Source0:        https://github.com/raspberrypi/userland/archive/%{commit0}/userland-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:        10-vchiq.rules

Patch0:         0001-Allow-applications-to-set-next-resource-handle.patch
Patch1:         0002-wayland-Add-support-for-the-Wayland-winsys.patch
Patch2:         0003-wayland-Add-Wayland-example.patch
Patch3:         0004-wayland-egl-Add-bcm_host-to-dependencies.patch
Patch4:         0005-interface-remove-faulty-assert-to-make-weston-happy-.patch
Patch5:         0006-zero-out-wl-buffers-in-egl_surface_free.patch
Patch6:         0007-initialize-front-back-wayland-buffers.patch
Patch7:         0008-Remove-RPC_FLUSH.patch
Patch8:         0009-fix-cmake-dependency-race.patch
Patch9:         0010-Fix-for-framerate-with-nested-composition.patch
Patch10:        0011-build-shared-library-for-vchostif.patch
Patch11:        0012-implement-buffer-wrapping-interface-for-dispmanx.patch
Patch12:        0013-Implement-triple-buffering-for-wayland.patch
Patch13:        0014-GLES2-gl2ext.h-Define-GL_R8_EXT-and-GL_RG8_EXT.patch
Patch14:        0015-EGL-glplatform.h-define-EGL_CAST.patch
Patch15:        0016-Allow-multiple-wayland-compositor-state-data-per-pro.patch
Patch16:        0017-khronos-backport-typedef-for-EGL_EXT_image_dma_buf_i.patch
Patch17:        0018-Add-EGL_IMG_context_priority-related-defines.patch
Patch18:        0019-libfdt-Undefine-__wordsize-if-already-defined.patch
Patch19:        0020-openmaxil-add-pkg-config-file.patch
Patch20:        0021-cmake-Disable-format-overflow-warning-as-error.patch

BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libfdt-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  systemd

%description
ARM side libraries and tools used on Raspberry Pi.

%package        libs
Summary:        Shared libraries for Raspberry Pi

%description    libs
Shared libraries for Raspberry Pi to interface to: EGL, mmal, GLESv2, vcos,
openmaxil, vchiq_arm, bcm_host, WFC, OpenVG.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        examples
Summary:        Source code examples for Raspberry Pi

%description    examples
Source code for examples using the Raspberry Pi libraries.

%prep
%autosetup -p1 -n userland-%{commit0}

# Use system device tree library
rm -fr opensrc/helpers/libfdt
sed -i -e '/add_subdirectory.*libfdt/d' CMakeLists.txt

%build

mkdir build
pushd build
%cmake \
  -DARM64=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_FLAGS:STRING="%{optflags}" \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DBUILD_WAYLAND=TRUE \
  -DVMCS_INSTALL_PREFIX=%{_prefix} \
  ..
%make_build
popd

%install
pushd build
%make_install
popd

find %{buildroot} -name '*.a' -delete

# Move libraries to the correct place
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}

sed -i -e 's|/lib|/%{_lib}|g' %{buildroot}%{_libdir}/pkgconfig/*.pc

# Move headers in a subfolder
mkdir %{buildroot}/vc
mv %{buildroot}%{_includedir}/* %{buildroot}/vc
mv %{buildroot}/vc %{buildroot}%{_includedir}/
sed -i -e 's|/include|/include/vc|g' %{buildroot}%{_libdir}/pkgconfig/*.pc

# udev rule for GPU access
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/10-vchiq.rules

%ldconfig_scriptlets libs

%files
%ifarch armv7hl
%{_bindir}/containers_check_frame_int
%{_bindir}/containers_datagram_receiver
%{_bindir}/containers_datagram_sender
%{_bindir}/containers_dump_pktfile
%{_bindir}/containers_rtp_decoder
%{_bindir}/containers_stream_client
%{_bindir}/containers_stream_server
%{_bindir}/containers_test
%{_bindir}/containers_test_bits
%{_bindir}/containers_test_uri
%{_bindir}/containers_uri_pipe
%{_bindir}/mmal_vc_diag
%{_bindir}/raspistill
%{_bindir}/raspivid
%{_bindir}/raspividyuv
%{_bindir}/raspiyuv
%{_bindir}/vcsmem
%endif
%{_bindir}/dtmerge
%{_bindir}/dtoverlay
%{_bindir}/dtoverlay-post
%{_bindir}/dtoverlay-pre
%{_bindir}/dtparam
%{_bindir}/tvservice
%{_bindir}/vcgencmd
%{_bindir}/vchiq_test
%{_bindir}/vcmailbox
%{_udevrulesdir}/10-vchiq.rules

%files libs
%license LICENCE
%{_libdir}/libbcm_host.so
%{_libdir}/libdebug_sym.so
%{_libdir}/libdtovl.so
%{_libdir}/libvchiq_arm.so
%{_libdir}/libvchostif.so
%{_libdir}/libvcos.so
%ifarch armv7hl
%{_libdir}/libEGL.so
%{_libdir}/libGLESv2.so
%{_libdir}/libOpenVG.so
%{_libdir}/libWFC.so
%{_libdir}/libbrcmEGL.so
%{_libdir}/libbrcmGLESv2.so
%{_libdir}/libbrcmOpenVG.so
%{_libdir}/libbrcmWFC.so
%{_libdir}/libcontainers.so
%{_libdir}/libmmal.so
%{_libdir}/libmmal_components.so
%{_libdir}/libmmal_core.so
%{_libdir}/libmmal_util.so
%{_libdir}/libmmal_vc_client.so
%{_libdir}/libopenmaxil.so
%{_libdir}/libvcsm.so
%{_libdir}/plugins/*.so
%endif

%files devel
%{_includedir}/vc
%{_libdir}/pkgconfig/bcm_host.pc
%{_libdir}/pkgconfig/brcmegl.pc
%{_libdir}/pkgconfig/brcmglesv2.pc
%{_libdir}/pkgconfig/brcmvg.pc
%{_libdir}/pkgconfig/mmal.pc
%{_libdir}/pkgconfig/openmaxil.pc
%{_libdir}/pkgconfig/vcsm.pc

%files examples
%{_usrsrc}/hello_pi

%changelog
* Mon Dec 07 2020 Simone Caronni <negativo17@gmail.com> - 1.0.0-2.20201130git093b30b
- Update to latest snapshot.

* Tue May 12 2020 Simone Caronni <negativo17@gmail.com> - 1.0.0-1.20200509gitcb852cd
- First build.
