#!/usr/bin/env perl
use strict;
use warnings;

my @lines;
my @sloc;
my $multiLineComment = 0;

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
        push(@lines, $_);
    }

}

foreach (@lines) {
    #skip /** multi-line comments
    if (/^\/(\*)+/) {
        $multiLineComment = 1;
        next;
    }
    #check if multi-line comment was closed
    elsif (/(\*)+\//) {
        $multiLineComment = 0;
        next;
    }
    #add line if it's not multi-line comment
    elsif ($multiLineComment == 0) {
        push(@sloc, $_);
    }
}

foreach (@sloc) {
    print "$_\n";
}
