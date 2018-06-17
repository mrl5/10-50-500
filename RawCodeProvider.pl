#!/usr/bin/env perl
use strict;
use warnings;

my @lines;

while (<>) {
    #remove \n from end of the line
    chomp;

    #remove spaces from the beggining of the line
    s/^\s+//;
    #remove '/* comments */'
    s/^\/\*.*\*\///;
    #remove '//comments'
    s/^\/\/.*//;

    #add non-empty line to the end of array
    if ($_ ne '') {
        print "$_\n";#tmp
        push(@lines, $_);
    }

}

#foreach (@lines) {
#  print "$_\n";
#  s/^\/\*.*\*\///;
#  print "$_\n";
#  #push(@sloc, $_)
#}
