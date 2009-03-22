#define svndate 20080521

Name:           avidemux
Version:        2.4.4
Release:        2%{?dist}
Summary:        Graphical video editing and transcoding tool

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.avidemux.org/
Source0:        http://download.berlios.de/avidemux/avidemux_%{version}.tar.gz
Source1:        %{name}-gtk.desktop
Source2:        %{name}-qt.desktop
# Make PulseAudio the default audio out device
Patch0:         avidemux-2.4-pulseaudio-default.patch
# Search for lrelease-qt4 instead of lrelease
Patch1:         avidemux-2.4-qt4.patch
# Why are i18n files stored in bindir? Move to datadir...
Patch2:         avidemux-2.4-i18n.patch
# http://ftp.ncnu.edu.tw/Linux/Gentoo/gentoo-portage/media-video/avidemux/files/avidemux-2.4-libdca.patch
Patch3:         avidemux-2.4-libdca.patch
# https://bugzilla.rpmfusion.org/attachment.cgi?id=131
# Upstream report: http://bugs.avidemux.org/index.php?do=details&task_id=592
Patch4:         avidemux-2.4-gcc44-movq.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       %{name}-cli  = %{version}
Requires:       %{name}-gui = %{version}

# Compiling
BuildRequires:	cmake
BuildRequires:  gettext-devel

# Libraries
BuildRequires:  nasm >= 0.98.38
BuildRequires:  libxml2-devel >= 2.6.8
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  js-devel
BuildRequires:  libXv-devel
BuildRequires:  libXmu-devel
# Required by gtk: libXi-devel, libXext-devel, libX11-devel
# Required by qt: libXt-devel, libXext-devel, libX11-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	jack-audio-connection-kit-devel

# Sound out
BuildRequires:  alsa-lib-devel >= 1.0.3
BuildRequires:  esound-devel >= 0.2.0

# Video out 
BuildRequires:  SDL-devel >= 1.2.7

# Audio Codecs
BuildRequires:  a52dec-devel >= 0.7.4
BuildRequires:  faac-devel >= 1.24
BuildRequires:  faad2-devel >= 2.0
BuildRequires:  lame-devel >= 3.96.1
BuildRequires:  libmad-devel >= 0.15.1
BuildRequires:  libogg-devel >= 1.1
BuildRequires:  libvorbis-devel >= 1.0.1

# needs libdts/dts_internal.h; but that's not shipped by  libdca-devel because
# it's an internal lib. Someone needs to report that upstream to get fixed
# ** this is fixed by patch3
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

%package cli
Summary:        CLI for %{name}
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description cli
This package provides command-line interface for %{name}.

%package gtk
Summary:        GTK GUI for %{name}
Group:          Applications/Multimedia
BuildRequires:  gtk2-devel >= 2.8.0
BuildRequires:  cairo-devel
# Slightly higher so it is default, but it can be avoided by installing
# avidemux-qt directly or it can be removed later once avidemux-qt is installed
Provides:       %{name}-gui = %{version}-%{release}.1
Requires:       %{name} = %{version}-%{release}

%description gtk
This package provides the GTK interface for %{name}.

%package qt
Summary:        QT GUI for %{name}
Group:          Applications/Multimedia
BuildRequires:  qt4-devel
Provides:       %{name}-gui = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}

%description qt
This package provides the Qt interface for %{name}.

%prep
%setup -q -n avidemux_%{version}
%patch0 -p1 -b .pulse
%patch1 -p1 -b .qt4
%patch2 -p1 -b .i18n
%patch3 -p1 -b .libdca
%patch4 -p1 -b .gcc44

%build
%cmake
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE1}

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE2}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog History README TODO
%dir %{_datadir}/%{name}

%files cli
%defattr(-,root,root,-)
%{_bindir}/avidemux2_cli

%files gtk
%defattr(-,root,root,-)
%{_bindir}/avidemux2_gtk
%{_datadir}/applications/*gtk*.desktop

%files qt
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}/i18n/
%{_datadir}/%{name}/i18n/*.qm
%{_bindir}/avidemux2_qt4
%{_datadir}/applications/*qt*.desktop

%changelog
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
