%global _pkgbuilddir %{_builddir}/%{name}_%{version}
# Turn off the brp-python-bytecompile script as in this case the scripts are
# internally interpreted.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:           avidemux
Version:        2.7.4
Release:        4%{?dist}
Summary:        Graphical video editing and transcoding tool

License:        GPLv2+
URL:            http://www.avidemux.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}.tar.gz

# Don't try to build on arm, aarch64 or ppc
ExclusiveArch:  i686 x86_64

# Utilities
BuildRequires:  cmake3 gcc-c++ yasm
%{?el7:BuildRequires: epel-rpm-macros}
BuildRequires:  gettext intltool
BuildRequires:  libxslt
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig
BuildRequires:  sqlite-devel
BuildRequires:  bzip2
BuildRequires:  libappstream-glib

# Libraries
BuildRequires:  libxml2-devel >= 2.6.8
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  fribidi-devel
BuildRequires:  libXv-devel
BuildRequires:  libXmu-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libass-devel
BuildRequires:  libmp4v2-devel

# Sound out
BuildRequires:  alsa-lib-devel >= 1.0.3
BuildRequires:  pulseaudio-libs-devel

# Video out
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libva-devel

# Audio Codecs
BuildRequires:  a52dec-devel >= 0.7.4
%{?_with_faac:BuildRequires:  faac-devel >= 1.24}
BuildRequires:  faad2-devel >= 2.0
BuildRequires:  lame-devel >= 3.96.1
BuildRequires:  libmad-devel >= 0.15.1
BuildRequires:  libogg-devel >= 1.1
BuildRequires:  libvorbis-devel >= 1.0.1
BuildRequires:  libdca-devel
BuildRequires:  opencore-amr-devel
BuildRequires:  twolame-devel
BuildRequires:  opus-devel

# Video Codecs
BuildRequires:  xvidcore-devel >= 1.0.2
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  nv-codec-headers

# Main package is a metapackage, bring in something useful.
Requires:       %{name}-gui = %{version}-%{release}


%description
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including MKV, MP4, TS, DVD
compatible MPEG files and AVI, using a variety of codecs. Tasks can be
automated using projects, job queue and powerful scripting capabilities.

This is a meta package that brings in all interfaces: QT and CLI.


%package cli
Summary:        CLI for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description cli
This package provides a command-line interface to editing videos with %{name}.

%package libs
Summary:        Libraries for %{name}

%description libs
This package contains the runtime libraries for %{name}.

%package qt
Summary:        Qt interface for %{name}
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-linguist
BuildRequires:  libxslt
Provides:       %{name}-gui = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       hicolor-icon-theme
Obsoletes:      %{name}-gtk < 2.6.10
Obsoletes:      %{name}-help

%description qt
This package contains the Qt graphical interface for %{name}.

%package i18n
Summary:        Translations for %{name}
Requires:       %{name}    = %{version}-%{release}
Requires:       %{name}-qt = %{version}-%{release}
BuildArch:      noarch

%description i18n
This package contains translation files for %{name}.


%prep
%autosetup -p1 -n %{name}_%{version}

# Remove sources of bundled libraries.
rm -rf avidemux_plugins/ADM_audioDecoders/ADM_ad_ac3/ADM_liba52 \
       avidemux_plugins/ADM_audioDecoders/ADM_ad_mad/ADM_libMad \
       avidemux_plugins/ADM_videoFilters6/ass/ADM_libass \
       avidemux_plugins/ADM_muxers/muxerMp4v2/libmp4v2

%build
# Build avidemux_core
export LDFLAGS="-lc -Wl,--as-needed"
mkdir build_core && pushd build_core
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       ../avidemux_core
%make_build V=1

# We have to do a fake install so header files are avaialble for the other
# packages.
make install DESTDIR=%{_pkgbuilddir}/fakeRoot
popd

# Build cli interface
rm -rf build_cli && mkdir build_cli && pushd build_cli
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DFAKEROOT=%{_pkgbuilddir}/fakeRoot \
       ../avidemux/cli
%make_build V=1
make install DESTDIR=%{_pkgbuilddir}/fakeRoot
popd

# Build QT5 gui
rm -rf build_qt5 && mkdir build_qt5 && pushd build_qt5
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DFAKEROOT=%{_pkgbuilddir}/fakeRoot \
       -DENABLE_QT5=TRUE \
       ../avidemux/qt4
%make_build V=1
make install DESTDIR=%{_pkgbuilddir}/fakeRoot
popd

# Build avidemux_plugins_common
rm -rf build_plugins_common && mkdir build_plugins_common && pushd build_plugins_common
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DFAKEROOT=%{_pkgbuilddir}/fakeRoot \
       -DAVIDEMUX_SOURCE_DIR=%{_builddir}/%{name}_%{version} \
       -DENABLE_QT5=TRUE \
       -DPLUGIN_UI=COMMON \
       -DUSE_EXTERNAL_LIBASS=TRUE \
       -DUSE_EXTERNAL_LIBMAD=TRUE \
       -DUSE_EXTERNAL_LIBA52=TRUE \
       -DUSE_EXTERNAL_MP4V2=TRUE \
       ../avidemux_plugins
%make_build V=1
make install DESTDIR=%{_pkgbuilddir}/fakeRoot
popd

# Build avidemux_plugins_cli
rm -rf build_plugins_cli && mkdir build_plugins_cli && pushd build_plugins_cli
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DFAKEROOT=%{_pkgbuilddir}/fakeRoot \
       -DAVIDEMUX_SOURCE_DIR=%{_builddir}/%{name}_%{version} \
       -DENABLE_QT5=TRUE \
       -DPLUGIN_UI=CLI \
       -DUSE_EXTERNAL_LIBASS=TRUE \
       -DUSE_EXTERNAL_LIBMAD=TRUE \
       -DUSE_EXTERNAL_LIBA52=TRUE \
       -DUSE_EXTERNAL_MP4V2=TRUE \
       ../avidemux_plugins
%make_build V=1
make install DESTDIR=%{_pkgbuilddir}/fakeRoot
popd

# Build avidemux_plugins_qt5
rm -rf build_plugins_qt5 && mkdir build_plugins_qt5 && pushd build_plugins_qt5
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DFAKEROOT=%{_pkgbuilddir}/fakeRoot \
       -DAVIDEMUX_SOURCE_DIR=%{_builddir}/%{name}_%{version} \
       -DENABLE_QT5=TRUE \
       -DPLUGIN_UI=QT4 \
       -DUSE_EXTERNAL_LIBASS=TRUE \
       -DUSE_EXTERNAL_LIBMAD=TRUE \
       -DUSE_EXTERNAL_LIBA52=TRUE \
       -DUSE_EXTERNAL_MP4V2=TRUE \
       ../avidemux_plugins
%make_build V=1
make install DESTDIR=%{_pkgbuilddir}/fakeRoot
popd


%install
%make_install -C build_core
%make_install -C build_cli
%make_install -C build_qt5
%make_install -C build_plugins_common
%make_install -C build_plugins_cli
%make_install -C build_plugins_qt5

# Remove useless devel files
rm -rf %{buildroot}%{_includedir}/%{name}

# FFMpeg libraries are not being installed as executable.
chmod +x %{buildroot}%{_libdir}/libADM6*.so.*

# Fix library permissions
find %{buildroot}%{_libdir} -type f -name "*.so.*" -exec chmod 0755 {} \;


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/metainfo/*.appdata.xml


%ldconfig_scriptlets libs
%ldconfig_scriptlets qt
%ldconfig_scriptlets cli


%if 0%{?el7}
%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /bin/touch --no-create %{_datadir}/icons/%{name} &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/%{name} &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/%{name} &>/dev/null || :
%endif

%files
%doc AUTHORS README

%files libs -f build_plugins_common/install_manifest.txt
%license COPYING
%dir %{_datadir}/avidemux6
%{_libdir}/libADM*
%exclude %{_libdir}/libADM_render*
%exclude %{_libdir}/libADM_UI*
# Catch the stuff missed using install_manifest.txt
%dir %{_libdir}/ADM_plugins6
%dir %{_libdir}/ADM_plugins6/*
%dir %{_libdir}/ADM_plugins6/autoScripts/lib

%files cli -f build_plugins_cli/install_manifest.txt
%{_bindir}/avidemux3_cli
%{_libdir}/libADM_UI_Cli*.so
%{_libdir}/libADM_render6_cli.so

%files qt 
%{_bindir}/avidemux3_qt5
%{_bindir}/avidemux3_jobs_qt5
%{_libdir}/libADM_openGLQT*.so
%{_libdir}/libADM_UIQT*.so
%{_libdir}/libADM_render6_QT5.so
%{_datadir}/applications/org.avidemux.Avidemux.desktop
%{_datadir}/metainfo/org.avidemux.Avidemux.appdata.xml
%{_datadir}/icons/hicolor/*/apps/org.avidemux.Avidemux.png
# QT plugins
%{_libdir}/ADM_plugins6/videoEncoders/qt5/
%{_libdir}/ADM_plugins6/videoFilters/qt5/
%{_libdir}/ADM_plugins6/shaderDemo/

%files i18n
%{_datadir}/avidemux6/qt5/i18n/


%changelog
* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 2.7.4-3
- Mass rebuild for x264

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 2.7.4-2
- Rebuild for new x265

* Fri Aug 16 2019 Richard Shaw <hobbes1069@gmail.com> - 2.7.4-1
- Update to 2.7.4.

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.7.3-2
- Rebuilt for x265

* Wed Mar 27 2019 Richard Shaw <hobbes1069@gmail.com> - 2.7.3-1
- Update to 2.7.3 and apply upstream patches per user request.
  Fixes RFBZ#5208.

* Wed Mar 13 2019 Leigh Scott <leigh123linux@googlemail.com> - 2.7.1-12
- Switch to nv-codec-headers

* Tue Mar 12 2019 Sérgio Basto <sergio@serjux.com> - 2.7.1-11
- Mass rebuild for x264

* Mon Mar 04 2019 Richard Shaw <hobbes1069@gmail.com> - 2.7.1-10
- Add patch for gcc 9 to fix bundled ffmpeg building, fixes RFBZ#5175.

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 2.7.1-8
- Rebuild for new x265

* Wed Nov 21 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.7.1-7
- Rebuild for x265-2.9 on el7
- Rebuild for x264-0.148 on el7
- Install avidemux.png
- Add scriptlets for epel

* Sun Nov 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.7.1-6
- Rebuild for new x265

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 2.7.1-5
- Mass rebuild for x264 and/or x265

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.7.1-3
- Rebuild for new libass version

* Thu Jun 07 2018 Richard Shaw <hobbes1069@gmail.com> - 2.7.1-2
- Update to 2.7.1
- Fix appdata file and build requires tweaks.

* Wed Feb 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.7.0-6
- Rebuilt for new x265
- Fix scriptlets

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.7.0-5
- Rebuilt for VA-API 1.0.0

* Sun Dec 31 2017 Sérgio Basto <sergio@serjux.com> - 2.7.0-4
- Mass rebuild for x264 and x265

* Mon Oct 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.7.0-3
- Rebuild for ffmpeg update

* Tue Oct  3 2017 Richard Shaw <hobbes1069@gmail.com> - 2.7.0-2
- Rebuild for f28.
- Add patch to deal with removal of pow10f function from glibc, fixes
  RFBZ#4672.

* Fri Sep 01 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.7.0-1
- Update to latest upstream release, 2.7.0.
- Remove gtk files section

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.6.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Richard Shaw <hobbes1069@gmail.com> - 2.6.20-1
- Update to latest upstream release, 2.6.20.

* Sat Apr 22 2017 Richard Shaw <hobbes1069@gmail.com> - 2.6.19-1
- Update to latest upstream release, 2.6.19.

* Wed Mar 22 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.6.16-5
- Build for x86 only

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.6.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan  3 2017 Richard Shaw <hobbes1069@gmail.com> - 2.6.16-3
- Disable byte-compiling of python scrips as they are designed to be 
  interpreted internally.
- Add backport fixes for filter preview windows, unbundle libmp4v2,
  and enable eac3.

* Tue Jan 03 2017 Dominik Mierzejewski <rpm@greysector.net> - 2.6.16-2
- rebuild for x265

* Sat Dec 31 2016 Richard Shaw <hobbes1069@gmail.com> - 2.6.16-1
- Update to the 2.6.16 release.
- Include pull request from RFBZ#4395.

* Tue Nov 22 2016 Sérgio Basto <sergio@serjux.com> - 2.6.15-1
- Update to the 2.6.15 release, rfbz#4344

* Tue Nov 08 2016 Sérgio Basto <sergio@serjux.com> - 2.6.12-7
- Rebuild for x265-2.1

* Wed Oct 19 2016 Richard Shaw <hobbes1069@gmail.com> - 2.6.12-6
- Remove all old GTK packages and references, also fixes scriptlet issue,
  BZ#4217.

* Tue Aug 16 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.6.12-5
- Add hardening to LDFLAGS

* Mon Jul 25 2016 Richard Shaw <hobbes1069@gmail.com> - 2.6.12-4
- Add patch to fix qt gui issues, fixes BZ#4035.

* Mon Jul 11 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 2.6.12-3
- Really fix building with GCC6, patch provided by Dan Horák <dan@danny.cz>

* Sat Jun 25 2016 Richard Shaw <hobbes1069@gmail.com> - 2.6.12-2
- Bump for rebuild in new infra.
- Add patch for GCC 6 narrowing conversion and other GCC 6 errors.

* Mon Apr  4 2016 Richard Shaw <hobbes1069@gmail.com> - 2.6.12-1
- Fix library file permissions, BZ#3923.

* Mon Nov 30 2015 Richard Shaw <hobbes1069@gmail.com> - 2.6.10-4
- Fix un-owned dir, BZ#3881.
- Fix broken scriptlet, BZ#3880.

* Sat Nov 28 2015 Richard Shaw <hobbes1069@gmail.com> - 2.6.10-3
- Revert back to QT4.

* Mon Nov  9 2015 Richard Shaw <hobbes1069@gmail.com> - 2.6.10-2
- Fix bug introduced while debugging FTBFS problem. Fixes RFBZ#3830.

* Tue Jun 16 2015 Richard Shaw <hobbes1069@gmail.com> - 2.6.10-1
- Update to latest upstream release.
- Disable GTK interface as it is unmaintained and does not build.

* Wed Jan 21 2015 Richard Shaw <hobbes1069@gmail.com> - 2.6.8-3
- Fix directory ownership.

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 2.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun May 11 2014 Richard Shaw <hobbes1069@gmail.com> - 2.6.8-1
- Update to latest upstream release.

* Sat Mar 22 2014 Sérgio Basto <sergio@serjux.com> - 2.6.7-4
- Rebuilt for x264

* Thu Mar 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6.7-3
- Rebuilt for x264

* Thu Mar 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6.7-2
- Rebuilt

* Mon Jan 27 2014 Richard Shaw <hobbes1069@gmail.com> - 2.6.7-1
- Update to latest upstream release.
- Obsolete unneeded devel subpackage.

* Tue Nov 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.6.4-8
- Rebuilt for x264/FFmpeg

* Tue Oct 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.6.4-7
- Rebuilt for x264

* Sat Jul 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.6.4-6
- Rebuilt for x264

* Mon Jun 24 2013 Richard Shaw <hobbes1069@gmail.com> - 2.6.4-5
- Can't have arch requirement on noarch package, fixes BZ#2840.

* Sun Jun 16 2013 Richard Shaw <hobbes1069@gmail.com> - 2.6.4-3
- Move translations to their own subpackage to make use optional, fixes BZ#2825.

* Mon Jun  3 2013 Richard Shaw <hobbes1069@gmail.com> - 2.6.4-2
- Fix packaging of translations (qt package only).

* Wed May 15 2013 Richard Shaw <hobbes1069@gmail.com> - 2.6.4-1
- Update to latest upstream release.

* Sun May 05 2013 Richard Shaw <hobbes1069@gmail.com> - 2.6.3-2
- Rebuild for updated x264.

* Wed Mar 20 2013 Richard Shaw <hobbes1069@gmail.com> - 2.6.3-1
- Update to latest bugfix release.

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.6.1-2
- Rebuilt for ffmpeg/x264

* Sat Dec 22 2012 Richard Shaw <hobbes1069@gmail.com> - 2.6.1-1
- Update to latest upstream release.

* Sun Dec 16 2012 Richard Shaw <hobbes1069@gmail.com> - 2.6.0-4
- Make sure we're building all available plugins. (#2575)
- Don't install the gtk interface when all you want is the qt one. (#2574)
- Exclude arm as a build target. (#2466)

* Fri Nov 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.6.0-2
- Rebuilt for x264

* Sun Oct 14 2012 Richard Shaw <hobbes1069@gmail.com> - 2.6.0-1
- Update to new upstream release.
