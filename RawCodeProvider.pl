#!/usr/bin/env perl
use strict;
use warnings;

my @lines;

while (<>) {
    #remove \n from end of the line
    chomp;

    #remove spaces from the beggining of the line
    s/^\s+//;

}

#foreach (@lines) {
#  print "$_\n";
#  s/^\/\*.*\*\///;
#  print "$_\n";
#  #push(@sloc, $_)
#}
