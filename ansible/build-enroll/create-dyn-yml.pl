#!/usr/bin/perl -w

use strict;

my $template = "dyn-yml-template";
my $out = "dyn.yml";

my $avamar_server = "un-fit-01.backup.hms.cdw.com";
my $avamar_domain = "CUSTA";
my $nimbus_hub_ip = "10.43.5.7";
my $bmnip = "10.43.5.7";
my $silo = "10.43.5.7";

my %servers = (
	"wwwbh01v" => "10.43.9.20",
	"wwwahcp01v" => "10.43.9.21",
	"wwwp01v" => "10.43.9.22",
	"wwwp02v" => "10.43.9.23",
	"wwwahs01v" => "10.43.9.26",
	"wwws01v" => "10.43.9.27",
	"wwwmsmp01v" => "10.43.5.140",
	"wwwmssp01v" => "10.43.5.141",
	"wwwrmp01v" => "10.43.5.142",
	"wwwrsp01v" => "10.43.5.143",
	"wwwmsms01v" => "10.43.5.144",
	"wwwrms01v" => "10.43.5.146",
	"wwwapmrd01v" => "10.43.5.148",
);

my $header = <<'HEADER';
---

_meta:
  hostvars:
    all:
      passfile: passfile

HEADER

my $footer = <<'FOOTER';
local:
- 127.0.0.1

group1:
  hosts:
FOOTER

open(OUT, ">$out");
print OUT $header;

foreach my $server (sort keys %servers) {
	#next if $server ne "wwwbh01v";
	open(TEMPLATE, "$template");
	while(<TEMPLATE>) {
		s/__SERVER__/$server/g;
		s/__IP__/$servers{$server}/g;
		s/__AVAMAR_SERVER__/$avamar_server/g;
		s/__AVAMAR_DOMAIN__/$avamar_domain/g;
		s/__NIMBUS_HUB_IP__/$nibus_hub_ip/g;
		s/__BMN__/$bmnip/g;
		s/__SILO__/$silo/g;
		print OUT;
	}
	print OUT "\n";
	close(TEMPLATE);
}

print OUT $footer;

foreach my $server (sort keys %servers) {
	print OUT "  - $server\n";
}
print OUT "\n";

close(OUT);
