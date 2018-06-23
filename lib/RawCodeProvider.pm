#!/usr/bin/env perl

# Works with Java source code
# Probably would also work with other C-like languages

# References:
# 1) https://stackoverflow.com/questions/1712016/how-do-i-include-functions-from-another-file-in-my-perl-script

#perlmod
package lib::RawCodeProvider;
use strict;
use warnings;
use Exporter;

my @lines;
my @rawSourceCode;
my $multiLineComment = 0;

#perlmod
our @ISA = qw(Exporter);
our @EXPORT = qw(getRawCode);

sub getRawCode {
    #read all lines
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
            push(@rawSourceCode, $_);
        }
    }
    return @rawSourceCode;
}
