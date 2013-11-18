#!/usr/bin/perl -w
use strict;

my (@file, @time, $i, $k, @all);
#my $dump = $ARGV[0];
my $dump_file = "/tmp/dump";
my $dump_tmp = "/tmp/dumptmp";
my $dump = "/tmp/dump_p";
system("tshark -R http -T text -V -r $dump_file > $dump_tmp");
#system(" cat $dump_tmp | sed -n -e 's\/Arrival Time.*:\\([0-9]*:[0-9\\.]*\\)\$\/\\1\/'p -e '/GET\\s/'p -e '/POST\\s/'p > $dump");

open TMP, "$dump_tmp" or die "$!";
open WRFILE, ">$dump" or die "$!";
print WRFILE "Start\n";
while (<TMP>) {
    /GET \// && print WRFILE;
    /POST/ && print WRFILE;
    /Arrival Time: [^\s]+ [^\s]+ [^\s]+ [0-9]+:([0-9]+):([0-9]+)\.([0-9][0-9][0-9])([0-9][0-9][0-9])/ && print WRFILE "".($1*60000 + $2*1000 + $3 + $4/1000)."\n";
    
}

close WRFILE;
close TMP;

open DUMP, "$dump" or die "$!";
@file = <DUMP>;

my @pat = (
           "GET /video/1515114 ",  "POST /qrpc", "GET /video/", "GET /swfs/qikPlayer4.swf",
           "POST /videos/played", "POST /log", "GET /wmxist/latest-videos",
           "GET /swfs/qik_chat.swf", "GET /video/"
           );
my %data = ();

for $k (1..$#file) {
    
    for $i (0..$#pat) {
        if ($file[$k] =~ /$pat[$i]/) {
            $time[$i] = &get_time($k);
            push(@all, &get_time($k));
            $data{&get_time($k) - $time[0]} = $pat[$i];
            #print "".$pat[$i]." -- ".$time[$i]." -- ".($time[$i] - $time[0])."\n";
        }
        
    }
    
}

for (1..$#time) {
    $time[$_] = ($time[$_] - $time[0]);
    
}
$time[0] = 0; 
close DUMP;
#print "Time = @time";
for (1..$#all) {
    $all[$_] = ($all[$_] - $all[0]);
    
}
$all[0] = 0;

#print "\n"."All = @all"."\n";
for my $i ( sort keys %data ) {
        #print "$i\t$data{$i}\n";
    }

open WF, ">/tmp/dict1" or die "$!";
for my $i ( sort keys %data ) {
        print WF "$i:$data{$i}\n";
    }
close WF;
system ("/home/lupus/testools/graphic.py");
system ("cp /tmp/filepic.png /tmp/filepic_`date +%s`.png");
sub get_time($) {
    my $num = $_[0];
    my $in;
    for ($in = $num; $in >= 0; $in--) {
        if ($file[$in] !~ /[a-z]/i && $file[$in] =~ /^[0-9]+\.[0-9]+$/) {
            #print $file[$in];
            #if ($file[$in] =~ /([0-9])+:([0-9])+\.([0-9][0-9][0-9])/){
            if ($file[$in] =~ /([0-9\.]+)/){
                return $1;
            #    return ($1*3600 + $2*60 + $3);
            }
            
        }
        
    }
    
}
