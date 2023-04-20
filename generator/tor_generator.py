#!/usr/bin/python3
import _io
import argparse
import os.path

# This file generates the torrc line..
# that will make ports available.
# You might need to add this line manually: "ControlPort 9050"

ver = "TG v1.0.0 Alpha-Beta"
write_mode = "append"[0] # write
default_from = 9051
default_to = 9151
default_output = "/etc/tor/torrc"
default_show = False
default_version = False

parser = argparse.ArgumentParser(prog=os.path.split(__file__)[-1], exit_on_error=True, add_help=True)

parser.add_argument("-f", "--from", default=default_from, type=int, required=False, metavar="[PORT-NUMBER-FROM]", dest="frm")
parser.add_argument("-t", "--to", default=default_to, type=int, required=False, metavar="[PORT-NUMBER-TO]")
parser.add_argument("-o", "--output", default=default_output, type=argparse.FileType(mode=write_mode, encoding="utf-8"), required=False, metavar="[OUTPUT-FILE]")
parser.add_argument("-s", "--show", default=default_show, required=False, action="store_true")
parser.add_argument("-v", "--version", default=default_version, action="version", version=ver)
args = parser.parse_args()

# verifying input
range_from = args.frm
range_to = args.to
output:_io.TextIOWrapper = args.output
show = args.show
version = args.version

output_name = output.name

line = lambda port:f"SocksPort {port}"
lines = []

verbose = lambda msg:print(msg) if show else None

if not version:
    verbose("Starting..")
    if range_from < range_to:
        verbose(f"{range_to - range_from} port will be written to {output_name}..")
        for sp in range(range_from, range_to): # socks port
            l = line(sp)
            lines.append(l)
            verbose(l)
        verbose("Done generating.")
    else:
        print("[FROM] range must be < [TO] range")
        exit(2)
else:
    print(ver)


verbose(f"Writing ports to {output_name}..")
output.write("\n"+'\n'.join(lines))
verbose(f"All done!")