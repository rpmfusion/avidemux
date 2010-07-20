%define _pkgbuilddir %{_builddir}/%{name}_%{version}

Name:           avidemux
Version:        2.5.3
Release:        4%{?dist}
Summary:        Graphical video editing and transcoding tool

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.avidemux.org/
Source0:        http://download.berlios.de/avidemux/avidemux_%{version}.tar.gz
## This procedure is used to make a SVN checkout
# svn co svn://svn.berlios.de/avidemux/branches/avidemux_2.5_branch_gruntster
# svn export avidemux_2.5_branch_gruntster avidemux-2.5.1-20091010svn-r5371
# pushd avidemux-2.5.1-20091010svn-r5371/avidemux/ADM_libraries
# rm {ffmpeg,libswscale}*.tar.gz
##(cmake/admFFmpegBuild.cmake provides the up-to-date SVN revision numbers)
# svn co svn://svn.ffmpeg.org/ffmpeg/trunk -r 19894 --ignore-externals ffmpeg_r19894
# svn export ffmpeg{_r19894,} --ignore-externals
# tar cfz ffmpeg_r19894.tar.gz ffmpeg && rm -rf ffmpeg{,_r19894}
# svn co svn://svn.ffmpeg.org/mplayer/trunk/libswscale -r 29686 libswscale_r29686
# svn export libswscale{_r29686,}
# tar cfz libswscale_r29686.tar.gz libswscale && rm -rf libswscale{,_r29686}
# popd
# tar cfj avidemux-2.5.1-20091010svn-r5371.tar.bz2 avidemux-2.5.1-20091010svn-r5371
#Source0:        avidemux-%{version}-20091010svn-r5371.tar.bz2
Source1:        %{name}-gtk.desktop
Source2:        %{name}-qt.desktop
# Patch0 obtained from avidemux-2.5.0-patches-1.tar.bz2:
# http://mirror.csclub.uwaterloo.ca/gentoo-distfiles/distfiles/avidemux-2.5.0-patches-1.tar.bz2
Patch0:         2.5.0-coreImage-parallel-build.patch
Patch1:         avidemux-2.5-pulseaudio-default.patch
Patch2:         avidemux-2.4-qt4.patch
# Prevents avidemux from creating the symlinks for .so files, which we do below
Patch3:         avidemux-2.5.3-tmplinktarget.patch
# Fixes multiple definitions of mjpeg_log
# http://fixounet.free.fr/2.6/2.5.3_mjpeg_fix.diff
Patch4:         2.5.3_mjpeg_fix.diff
# libADM_xvidRateCtl.so and libADM_vidEnc_pluginOptions.so are supposed to be
# build statically according to upstream... Let's get them installed instead
Patch5:         avidemux-2.5.3-mpeg2enc.patch
Patch6:         avidemux-2.5.3-pluginlibs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Upstream has been informed http://avidemux.org/admForum/viewtopic.php?id=6447
ExcludeArch: ppc ppc64

Requires:       %{name}-cli  = %{version}-%{release}
Requires:       %{name}-gui = %{version}-%{release}
Requires:       %{name}-plugins = %{version}

# Compiling
BuildRequires:  cmake
BuildRequires:  gettext-devel

# Libraries
BuildRequires:  yasm-devel
BuildRequires:  libxml2-devel >= 2.6.8
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  js-devel
BuildRequires:  libXv-devel
BuildRequires:  libXmu-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  jack-audio-connection-kit-devel

# Sound out
BuildRequires:  alsa-lib-devel >= 1.0.3
BuildRequires:  pulseaudio-libs-devel

# Video out 
BuildRequires:  SDL-devel >= 1.2.7

# Audio Codecs
BuildRequires:  a52dec-devel >= 0.7.4
%{?_with_faac:BuildRequires:  faac-devel >= 1.24}
BuildRequires:  faad2-devel >= 2.0
BuildRequires:  lame-devel >= 3.96.1
BuildRequires:  libmad-devel >= 0.15.1
BuildRequires:  libogg-devel >= 1.1
BuildRequires:  libvorbis-devel >= 1.0.1
BuildRequires:  libdca-devel


# Video Codecs
BuildRequires:  xvidcore-devel >= 1.0.2
BuildRequires:  x264-devel
BuildRequires:  ffmpeg-devel

# FIXME: aften not packaged, add BR when it is

# Finally...
BuildRequires:  desktop-file-utils

%description
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible
MPEG files, MP4 and ASF, using a variety of codecs. Tasks can be automated
using projects, job queue and powerful scripting capabilities.

For compatibility reasons, avidemux is a meta-package which installs the
graphical, command line and plugin packages. If you want a smaller setup,
you may selectively install one or more of the avidemux-* subpackages.

%package cli
Summary:        CLI for %{name}
Group:          Applications/Multimedia
Requires:       %{name}-libs = %{version}-%{release}

%description cli
This package provides a command-line interface to editing videos with %{name}.

%package libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description libs
This package contains the runtime libraries for %{name}.

%package gtk
Summary:        GTK interface for %{name}
Group:          Applications/Multimedia
BuildRequires:  gtk2-devel >= 2.8.0
BuildRequires:  cairo-devel
# Slightly higher so it is default, but it can be avoided by installing
# avidemux-qt directly or it can be removed later once avidemux-qt is installed
Provides:       %{name}-gui = %{version}-%{release}.1
Requires:       %{name}-libs = %{version}-%{release}

%description gtk
This package provides the GTK graphical interface for %{name}.

%package qt
Summary:        Qt interface for %{name}
Group:          Applications/Multimedia
# 4.5.0-9 fixes a failure when there are duplicate translated strings
# https://bugzilla.redhat.com/show_bug.cgi?id=491514
BuildRequires:  qt4-devel >= 4.5.0-9
Provides:       %{name}-gui = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description qt
This package contains the Qt graphical interface for %{name}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description devel
This package contains files required to develop with or extend %{name}.

%package plugins
Summary:        Plugins for the avidemux video editing and transcoding tool
Group:          Applications/Multimedia
Requires:       %{name}-libs = %{version}-%{release}

%description plugins
This package contains various plugins for avidemux.

%prep
%setup -q -n avidemux_%{version}

# change hardcoded libdir paths
%ifarch x86_64 ppc64
sed -i.bak 's/startDir="lib";/startDir="lib64";/' avidemux/ADM_core/src/ADM_fileio.cpp
sed -i.bak 's/startDir="lib";/startDir="lib64";/' avidemux/main.cpp
%endif

%patch0 -p1 -b .parallel
%patch1 -p1 -b .pulse
%patch2 -p1 -b .qt4
%patch3 -p1 -b .tmplinktarget
%patch4 -p1 -b .mjpeg_log
%patch5 -p1 -b .mpeg2enc
%patch6 -p1 -b .pluginlibs


%build
# Out of source build
mkdir build && cd build
%cmake -DAVIDEMUX_INSTALL_PREFIX=%{_prefix} \
       -DAVIDEMUX_SOURCE_DIR="%{_pkgbuilddir}" \
       -DAVIDEMUX_CORECONFIG_DIR="%{_pkgbuilddir}/build/config" \
       ..
make %{?_smp_mflags}
# Create the temp link directory manually since otherwise it happens too early
mkdir -p %{_pkgbuilddir}/build/%{_lib}
find %{_pkgbuilddir}/build/avidemux -name '*.so*' | \
     xargs ln -sft %{_pkgbuilddir}/build/%{_lib}

mkdir ../build_plugins && cd ../build_plugins
%cmake -DAVIDEMUX_INSTALL_PREFIX="%{_pkgbuilddir}/build/" \
       -DAVIDEMUX_SOURCE_DIR="%{_pkgbuilddir}" \
       -DAVIDEMUX_CORECONFIG_DIR="%{_pkgbuilddir}/build/config" \
       ../plugins
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make -C build install DESTDIR=$RPM_BUILD_ROOT
make -C build_plugins install DESTDIR=$RPM_BUILD_ROOT
# Install the build configuration for devel package
install -d -m755 $RPM_BUILD_ROOT%{_includedir}
install -m644 build/config/ADM_coreConfig.h $RPM_BUILD_ROOT%{_includedir}/ADM_coreConfig.h
install -d -m755 $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m644 avidemux/ADM_userInterfaces/ADM_QT4/ADM_gui/pics/avidemux_icon.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/avidemux.png

# Find and remove all la files
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

# Install .desktop shortcuts
desktop-file-install --vendor rpmfusion \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE1}

desktop-file-install --vendor rpmfusion \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE2}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# metapackage, no files

%files libs -f %{name}.lang
%doc AUTHORS COPYING README TODO
%dir %{_datadir}/%{name}
%{_datadir}/ADM_scripts/
%{_datadir}/pixmaps/avidemux.png
%{_libdir}/libADM*

%files cli
%defattr(-,root,root,-)
%{_bindir}/avidemux2_cli

%files gtk
%defattr(-,root,root,-)
%{_bindir}/avidemux2_gtk
%{_datadir}/applications/*gtk*.desktop

%files qt
%defattr(-,root,root,-)
%{_datadir}/%{name}/i18n/
%{_bindir}/avidemux2_qt4
%{_datadir}/applications/*qt*.desktop

%files plugins
%defattr(-,root,root,-)
%{_libdir}/ADM_plugins/

%files devel
%defattr(-,root,root,-)
%{_includedir}/ADM_coreConfig.h

%changelog
* Tue Jul 20 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.3-4
- Rebuild for new x264

* Sun May 30 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.3-3
- Add /usr/bin/xsltproc BR for qt4 subpackage

* Wed May 26 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.3-2
- Bump for F-13 --> devel EVR

* Wed May 26 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.3-1
- Update to 2.5.3 release
- Use avidemux.png as icon in the desktop shorcuts to fix problem on KDE
- Make ldconfig run in post/postun of libs package
- Fix typo in %%description

* Wed Jan 27 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.2-4
- Remove the i18n folder from %%files, as it seems it does not get created nor
  populated with any files on rawhide.

* Tue Jan 26 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.2-3
- Fix stupid mistake in mkdir command (add -p for subdir creation)

* Mon Jan 25 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.2-2
- Temporary workaround for build failure on rawhide

* Mon Jan 18 2010 Stewart Adam <s.adam at diffingo.com> - 2.5.2-1
- Update to 2.5.2 release

* Thu Nov  5 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.5.1-6.20091010svn
- Update bugfix to 20091105

* Sat Oct 24 2009 Stewart Adam <s.adam at diffingo.com> - 2.5.1-5.20091010svn
- Temporarily disable FAAC as per discussion on RF-dev ML
- Create temporary linking dir before running find | xargs

* Fri Oct 23 2009 Orcan Ogetbil <oged[DOT]fedora[AT]gmail[DOT]com> - 2.5.1-4.20091010svn
- Update desktop file according to F-12 FedoraStudio feature

* Sat Oct 10 2009 Stewart Adam <s.adam at diffingo.com> - 2.5.1-3.20091010svn
- Fix AVIDEMUX_INSTALL_PREFIX define so plugins can link correctly

* Sat Oct 10 2009 Stewart Adam <s.adam at diffingo.com> - 2.5.1-2.20091010svn
- Update to 2.5.1 subversion r5371

* Fri Jun 19 2009 Stewart Adam <s.adam at diffingo.com> - 2.4.4-9
- Add patch to fix build with CMake 2.6.4
- Update gcc44 patch to match Gentoo upstream
- Update PulseAudio patch to work as expected with avidemux 2.4.4

* Sun May 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4.4-8
- skip %%_smp_mflags in po/

* Sat Apr 25 2009 Stewart Adam <s.adam at diffingo.com> - 2.4.4-7
- Test build with ppc* enabled

* Sat Apr 25 2009 Stewart Adam <s.adam at diffingo.com> - 2.4.4-6
- Rebuild, disable ppc* for now

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.4.4-5
- rebuild for new F11 features

* Wed Mar 25 2009 Dominik Mierzejewski <rpm at greysector.net> - 2.4.4-4
- Fix gcc 4.4 patch
- Improve dca patch

* Sun Mar 22 2009 Stewart Adam <s.adam at diffingo.com> - 2.4.4-3
- Apply the patch

* Sun Mar 22 2009 Stewart Adam <s.adam at diffingo.com> - 2.4.4-2
- Fix build errors when compiling with gcc 4.4 (#386) (thanks to Rathann)

* Wed Feb 18 2009 Stewart Adam <s.adam at diffingo.com> - 2.4.4-1
- Update to 2.4.4 final, update patches accordingly
- Move Qt translation files to qt subpackage

* Sun Dec 14 2008 Dominik Mierzejewski <rpm at greysector.net> - 2.4.3-8
- Fix build with current x264

* Fri Dec 5 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-7.1
- Rebuild for 20081202 ffmpeg snapshot

* Tue Nov 25 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-7
- Don't uselessly provide avidemux-cli
- Make GUI and CLI subpackages require the main package (fixes bz#178)

* Tue Nov 25 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-6
- Bump release to fix EVR

* Sat Sep 27 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-5
- Add CMake patch for PPC64
- Update patches for 2.4.3
- Remove outdated libmad patch (Nov. 2007)

* Thu Sep 18 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-4
- Add another patch to fix ppc64 build (pointer type), first
  patch was for libmad

* Fri Aug 22 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-3
- Add patch to fix ppc64 build

* Sat Aug 16 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-2
- retag

* Sat Aug 16 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.3-1
- Update to 2.4.3

* Tue Aug 12 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.2-3
- ppc64 uint_32 fun

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.4.2-2
- rebuild

* Sat Jul 19 2008 Thorsten Leemhuis <s.adam at diffingo.com> - 2.4.2-1
- Update to 2.4.2

* Wed May 21 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4.1-3.20080521svn
- Disable --new-faad
- 20080521 subversion snapshot

* Sat Mar 15 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4.1-2
- Disable %%{?_smp_mflags}

* Sat Mar 15 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4.1-1
- Update to 2.4.1
- Don't list the bin files twice, revisited
- Default to GTK frontend

* Wed Feb 20 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-6.20080126svn
- Make pulseaudio default for sound out
- Don't list the bin files twice
- Don't build with arts support

* Fri Feb 15 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-5.20080126svn
- Don't list the .desktop files twice (bz#1870)
- Oops, we should have %%{svndate}svn in release tag!

* Sat Feb 2 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-4
- F-8/F-7 x86_64 does seem to need --with-newfaad

* Fri Feb 1 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-3
- Update to version 2.4 (20080126svn) and include fixes from devel branch

* Mon Jan 14 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-2
- Fix many copy/paste errors and desktop file's Exec field

* Sun Jan 13 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-1
- Update to 2.4 final
- Split up desktop files and make them pass desktop-file-validate
- Add structure to split into gtk and qt pacakges
- Disable qt4 for now, doesn't compile

* Sun Oct 7 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info>3- 2.3.0-4.3
- move js-include to a place where it is honored

* Sun Oct 7 2007 Stewart Adam <s.adam AT diffingo DOT com> - 2.3.0-4.2
- Fix macro problem
- Fix changelog date
- Rebuild with faad, but don't pass --newfaad

* Sun Oct 7 2007 Stewart Adam <s.adam AT diffingo DOT com> - 2.3.0-4.1
- Rebuild with no faad

* Sat Oct 6 2007 Stewart Adam <s.adam AT diffingo DOT com> - 2.3.0-4
- Rebuild for ffmpeg dependency problems
- Update License: tag per Fedora guidelines

* Sat Jan 13 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.3.0-3
- more features with new BR's: x264-devel libXv-devel
- make a note regarding the libdca-devel problem
- remove the "0:" from the versioned BR's

* Thu Jan 04 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.3.0-2
- don't use smp_mflags during make for now

* Sat Dec 23 2006 kwizart < kwizart at gmail.com > - 2.3.0-1
- Update to 2.3.0 Final
- Use find_lang

* Mon Apr 03 2006 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.1.2-1
- Update to 2.1.2

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Jan 04 2006 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.1.0-0.lvn.1
- Update to 2.1.0
- Drop epoch
- gtk 2.6 now, so drop FC3 support

* Sat Aug 27 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.42-0.lvn.3
- Remove bogus BR ffmpeg-devel (#555)

* Thu Jul 09 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.42-0.lvn.2
- Add missing BR desktop-file-utils (thanks to ixs)

* Thu Jul 07 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.42-0.lvn.1
- Update to 2.0.42

* Sat Jan 22 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.36-0.lvn.1
- Update to 2.0.34
- Rename package to avidemux -- no need for avidemux2 afaics

* Sun Nov 21 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.34-0.lvn.1.test1
- Update to 2.0.34-test1
- BR gettext, libtool

* Tue Oct 18 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.30-0.lvn.1
- Initial RPM release.
