"""
MCP Server for Ocular Accommodative Microfluctuations (AMF) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import AccommodativeMicrofluctuationClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-ocular-accommodative-microfluctuations-amf-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "analyze_amf",
                        "description": "Analyze ocular accommodative microfluctuations (AMF), LFC, HFC, and ciliary muscle fatigue.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "diopter_series": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Continuous refractive power recordings in Diopters (D)."
                                },
                                "baseline_target_distance_m": {
                                    "type": "number",
                                    "description": "Target distance in meters (default: 0.40 m)."
                                },
                                "sampling_rate_hz": {
                                    "type": "number",
                                    "description": "Sampling rate in Hertz (default: 10.0 Hz)."
                                }
                            },
                            "required": ["diopter_series"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "analyze_amf":
            sampling_rate_hz = float(args.get("sampling_rate_hz", 10.0))
            baseline_target_distance_m = float(args.get("baseline_target_distance_m", 0.40))
            diopter_series = args.get("diopter_series", [])
            client = AccommodativeMicrofluctuationClient(sampling_rate_hz=sampling_rate_hz)
            try:
                res = client.analyze_amf(
                    diopter_series=diopter_series,
                    baseline_target_distance_m=baseline_target_distance_m
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
