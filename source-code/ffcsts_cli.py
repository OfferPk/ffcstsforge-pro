#!/usr/bin/env python3
"""
FFCSTSForge Pro (v1.0.0) - Back-End CLI & Forward Uplink Emulator
Standard: CCSDS 922.3-B-1 (Blue Book, Issue 1, April 2021)
"""

import argparse
import json
import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

class FFCSTSCLI:
    def __init__(self):
        self.schema_urn = "urn:ccsds:schema:csts:ff:1.0"
        self.station_id = "DSN-DSS-26"
        self.instance_id = "csts=ff/provider=DSN/station=DSS26/sc=JUICE/inst=01"

    def create_sample_telecommand(self):
        now = datetime.now(timezone.utc).isoformat()
        return {
            "standard": "CCSDS 922.3-B-1",
            "framework": "CCSDS 921.1-B-2",
            "schema_urn": self.schema_urn,
            "station_id": self.station_id,
            "service_instance_id": self.instance_id,
            "state": "ACTIVE",
            "carrier_state": "MODULATING",
            "bound_user": "MOC-JUICE-OPS",
            "radiation_mode": "IMMEDIATE",
            "timestamp": now,
            "forward_frame": {
                "sequence_number": 105,
                "frame_id": "TC-FRAME-105",
                "frame_type": "CCSDS_232_0_TC",
                "virtual_channel_id": 1,
                "frame_length_bytes": 256,
                "radiation_status": "RADIATED"
            },
            "buffer_depth": 0,
            "frames_radiated_total": 105,
            "notifications": [
                {
                    "id": "NOTIFY-105",
                    "timestamp": now,
                    "severity": "NOMINAL",
                    "message": "Forward Transfer Frame successfully radiated via 34m BWG antenna"
                }
            ]
        }

    def generate_xml(self, data):
        root = ET.Element("csts_ff_message", {
            "xmlns": self.schema_urn,
            "version": "1.0.0"
        })
        hdr = ET.SubElement(root, "header")
        ET.SubElement(hdr, "standard").text = data.get("standard")
        ET.SubElement(hdr, "framework").text = data.get("framework")
        ET.SubElement(hdr, "service_instance_id").text = data.get("service_instance_id")
        ET.SubElement(hdr, "station_id").text = data.get("station_id")
        ET.SubElement(hdr, "service_state").text = data.get("state")
        ET.SubElement(hdr, "carrier_state").text = data.get("carrier_state")
        ET.SubElement(hdr, "bound_user").text = data.get("bound_user")
        ET.SubElement(hdr, "frames_radiated_total").text = str(data.get("frames_radiated_total", 0))

        ff = data.get("forward_frame", {})
        buf = ET.SubElement(root, "forward_frame_buffer", {
            "seq": str(ff.get("sequence_number", 1)),
            "timestamp": data.get("timestamp")
        })
        ET.SubElement(buf, "frame_id").text = ff.get("frame_id")
        ET.SubElement(buf, "frame_type").text = ff.get("frame_type")
        ET.SubElement(buf, "virtual_channel_id").text = str(ff.get("virtual_channel_id"))
        ET.SubElement(buf, "frame_length_bytes").text = str(ff.get("frame_length_bytes"))
        ET.SubElement(buf, "radiation_status").text = ff.get("radiation_status")

        notifs = ET.SubElement(root, "notifications", {"count": str(len(data.get("notifications", [])))})
        for n in data.get("notifications", []):
            n_el = ET.SubElement(notifs, "notification", {
                "id": n["id"],
                "severity": n["severity"],
                "timestamp": n["timestamp"]
            })
            ET.SubElement(n_el, "message").text = n["message"]

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

def main():
    parser = argparse.ArgumentParser(description="FFCSTSForge Pro - CCSDS 922.3-B-1 Forward Frame CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    subparsers.add_parser("simulate-uplink", help="Simulate forward telecommand frame radiation")
    subparsers.add_parser("export-xml", help="Export canonical CCSDS 922.3 XML frame")
    subparsers.add_parser("audit", help="Run 10-point normative compliance audit")

    args = parser.parse_args()
    cli = FFCSTSCLI()

    if args.command == "simulate-uplink":
        print(json.dumps(cli.create_sample_telecommand(), indent=2))
    elif args.command == "export-xml":
        data = cli.create_sample_telecommand()
        print(cli.generate_xml(data))
    elif args.command == "audit":
        import subprocess
        subprocess.run(["node", "source-code/ffcsts-auditor.js"])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
