
#!/usr/bin/perl

use strict;
use warnings;
use IO::Socket;
use Data::Validate::IP qw(is_ipv4 is_ipv6);

my $ip, my $port;
my $portbegin = 0;
my $portend = 65535;
my $totalinput = $#ARGV + 1;

if ($totalinput != 1) {
        die "Enter only one argument!\n";
} else {
        $ip = $ARGV[0];
}

for ($port=$portbegin;$port<$portend;$port++) {
        my $remote = IO::Socket::INET->new(
        Proto=>"tcp",
        PeerAddr=>$ip,
        PeerPort=>$port,
        Timeout => 0.01,
        );

        if ($remote) {
                print "IP $ip port $port is open\n";
        }
}
