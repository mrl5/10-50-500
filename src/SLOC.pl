#!/usr/bin/env perl

# HowTo: 'perl SLOC.pl File.java'

use strict;
use warnings;
use RawCodeProvider;

my @output = getRawCode;

# todo focus only on code
print "\nSLOC: $#output\n";