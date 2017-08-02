#! /usr/bin/env python3
"""
    This is the "helios_common.py" module
    So far, it provides "UpdateMounted," "GetPasswd,"
    "AptSourceReplace," "AptSourceRestore," "SendNotice,"
    "SendError," "Warning," and "Die"
"""

from psutil import disk_partitions
from yad import YAD
from io import StringIO
from time import sleep
from shutil import move, copy
import re, sh, os

BASE_UPDATE_DIR = '/usr/local/share/HeliOS-Update'
POST_INSTALL_DIR = '/usr/local/share/HeliOS-Post-Install'
STAGING = os.path.join( BASE_UPDATE_DIR, 'staging' )

APT_DIR = '/etc/apt'
APT_EXTRAS_DIR = '/etc/apt/sources.list.d/'
APT_OFFLINE_DIR = '/etc/apt/offline.d/'
APT_SOURCES_ONLINE = '/etc/apt/sources.list'
APT_SOURCES_OFFLINE = '/etc/apt/offline.d/sources.list'
APT_SOURCES_SAVE = '/etc/apt/sources.list.save'

# ===================================================================================================

def UpdateMounted():
    partitions = disk_partitions(all=False)

    apt_mount_point = None
    apt_pattern = re.compile(r"(.*APT.*)")
    for p in partitions:
         match = apt_pattern.match(p.mountpoint)
         if match is not None:
            apt_mount_point = match.group(1)
            break
    return( apt_mount_point )

# ===================================================================================================

def GetPasswd():
    buf = StringIO()
    try:
        sh.yad( "--entry", "--hide-text", "--entry-label", "Enter Password", 
                "--width", "340", "--borders=10", "--on-top", "--center",
                "--title", "Enter Your Password", _out=buf )
        passwd = buf.getvalue().splitlines().pop()
        return( passwd )
    except sh.ErrorReturnCode_1:
        return( None )

# ===================================================================================================

def AptSourceReplace( new_source=None ):
    if new_source is None:
        return( [False, "No APTonCD source repository specified", 'Notice:'] )

    if os.path.isfile( APT_SOURCES_ONLINE ):
        if os.path.isfile( APT_SOURCES_OFFLINE ):
            os.remove( APT_SOURCES_OFFLINE )
        try:
            move( APT_SOURCES_ONLINE, APT_SOURCES_OFFLINE )
        except Exception as e:
            return( [False, "Unable to move the APT sources.list off-line: " + repr(e), 'Error:'] )

    err_msg = []
    for i in os.listdir( APT_EXTRAS_DIR ):
        online_version = os.path.join( APT_EXTRAS_DIR, i )
        offline_version = os.path.join( APT_OFFLINE_DIR, i )
        if not os.path.isdir( online_version ):
            if os.path.isfile( offline_version ):
                os.remove( offline_version )
            try:
                move( online_version, offline_version )
            except Exception as e:
                err_msg.append( repr(e) )

    if len( err_msg ) > 0:
        return( [False, 'Unable to relocate APT sources off-line: ' + ', '.join( err_msg ), 'Error:'] )

    try:
        with open( APT_SOURCES_ONLINE, 'wt') as fh:
            fh.write( "deb file:" + new_source + "/ /" + "\n" )
    except Exception as e:
        return( [False, "Unable to point APT sources.list to \"" + new_source + "\" -- " + repr(e), 'Error:'] )

    return( [True, 'APT sources prepared for update OK', 'OK:'] )

# ===================================================================================================

def AptSourceRestore():
    if os.path.isfile( APT_SOURCES_OFFLINE ):
        try:
            move( APT_SOURCES_OFFLINE, APT_SOURCES_ONLINE )
        except Exception as e:
            return( [False, "Unable to restore the APT sources.list file: " + repr(e), 'Error:'] )
    elif os.path.isfile( APT_SOURCES_SAVE ):
        try:
            copy( APT_SOURCES_SAVE, APT_SOURCES_ONLINE )
        except Exception as e:
            SendError( "Unable to restore the APT sources.list from the \"saved\" version: " + repr(e) )
            return( False )

    err_msg = []
    for i in os.listdir( APT_OFFLINE_DIR ):
        offline_file = os.path.join( APT_OFFLINE_DIR, i )
        online_file = os.path.join( APT_EXTRAS_DIR, i )
        if not os.path.isdir( offline_file ):
            if os.path.isfile( online_file ):
                os.remove( online_file )
            try:
                move( offline_file, online_file )
            except Exception as e:
                err_msg.append( repr(e) )

    if len(err_msg) > 0:
        return( [False, 'Unable to restore all of the off-line APT sources: ' + ', '.join( err_msg ), 'Error:'] )

    return( [True, 'APT sources restored OK', 'OK:'] )

# ===================================================================================================

def NoticeFormat(raw_input):
    bubble = raw_input.splitlines()
    cnt = len(bubble)
    width = 0
    for ll in bubble:
        width = max( width, len(ll) )
    width = width + 10

    format_str = '{:^' + str( width ) + '}'
    output = ['  ']
    for ll in bubble:
        output.append( format_str.format(ll) )

    window_width = width * 11

    return( "\n".join( output ), cnt, window_width )

# ==================================================================================================

def SendNotice( message=None, header='Notice:' ):
    if message is None:
        return

    Yad = YAD()
    output, line_cnt, win_width = NoticeFormat( header + ' ' + message )
    win_height = str( (line_cnt * 13) + 60 )
    time_out = max( 3, line_cnt )
    x = Yad.TextInfo( 
                        listen=True, tail=True,
                        font=['Liberation Mono', 'Regular', '12'],
                        height=win_height, width=win_width, center=True,
                        skip_taskbar=True, on_top=True, fore='#0F482E', back='#FFFACD',
                        no_buttons=True, timeout=time_out, undecorated=True )
    x( output )

# ==================================================================================================

def SendError( message=None, header='Error:' ):
    if message is None:
        return

    Yad = YAD()
    output, line_cnt, win_width = NoticeFormat( header + ' ' + message )
    win_height = str( (line_cnt * 13) + 60 )
    time_out = max( 3, line_cnt )
    x = Yad.TextInfo( 
                        listen=True, tail=True,
                        font=['Liberation Mono', 'Regular', '12'],
                        height=win_height, width=win_width, center=True,
                        skip_taskbar=True, on_top=True, fore='#961D1D', back='#FFFACD',
                        no_buttons=True, timeout=time_out, undecorated=True )
    x( output )

# ===================================================================================================

def Warning( message=None, header="Notice:" ):
    if message is None:
        return

    print( "-------------------------------------------------------------------------")
    print( header + " " + message )
    print( "-------------------------------------------------------------------------")

# ===================================================================================================

def Die( message="Program Script Terminated", header=None ):
    if header is None:
        SendError( message )
    else:
        SendError( message, header )
    sleep( 1 )
    raise SystemExit(1)

