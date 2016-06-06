# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin


class Corosync(Plugin):
    """ Corosync cluster engine
    """

    plugin_name = "corosync"
    profiles = ('cluster',)
    packages = ('corosync',)

    def setup(self):
        self.add_copy_spec([
            "/etc/corosync",
            "/var/lib/corosync/fdata"
        ])
        if self.get_option("all_logs"):
            self.add_copy_spec_limit("/var/log/cluster/corosync.log*",
                                     sizelimit=self.get_option("log_size"))
        else:
            self.add_copy_spec_limit("/var/log/cluster/corosync.log",
                                     sizelimit=self.get_option("log_size"))
        self.add_cmd_output([
            "corosync-quorumtool -l",
            "corosync-quorumtool -s",
            "corosync-cpgtool",
            "corosync-cfgtool -s",
            "corosync-blackbox",
            "corosync-objctl -a",
            "corosync-cmapctl"
        ])
        self.call_ext_prog("killall -USR2 corosync")

    def postproc(self):
        self.do_cmd_output_sub(
            "corosync-objctl",
            r"(.*fence.*\.passwd=)(.*)",
            r"\1******"
        )


class RedHatCorosync(Corosync, RedHatPlugin):

    def setup(self):
        super(RedHatCorosync, self).setup()


class DebianCorosync(Corosync, DebianPlugin, UbuntuPlugin):

    def setup(self):
        super(DebianCorosync, self).setup()

    files = ('/usr/sbin/corosync',)

# vim: set et ts=4 sw=4 :
