"""
Create, update, or list n8n workflows via the REST API.

Usage:
    python execution/create_n8n_workflow.py --list-workflows
    python execution/create_n8n_workflow.py --get-workflow <ID>
    python execution/create_n8n_workflow.py --name "My Workflow" --input .tmp/workflow.json
    python execution/create_n8n_workflow.py --update <ID> --input .tmp/workflow.json
    python execution/create_n8n_workflow.py --activate <ID>
"""

import argparse
import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

N8N_API_URL = os.environ["N8N_API_URL"].rstrip("/")
N8N_API_KEY = os.environ["N8N_API_KEY"]

HEADERS = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json",
}


def list_workflows():
    resp = requests.get(f"{N8N_API_URL}/api/v1/workflows", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    workflows = resp.json().get("data", [])
    for wf in workflows:
        active = "active" if wf.get("active") else "inactive"
        print(f"  {wf['id']:>6}  [{active}]  {wf['name']}")
    print(f"\n{len(workflows)} workflows total.")


def get_workflow(workflow_id: str):
    resp = requests.get(f"{N8N_API_URL}/api/v1/workflows/{workflow_id}", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    print(json.dumps(resp.json(), indent=2))


def create_workflow(name: str, input_path: str):
    with open(input_path) as f:
        payload = json.load(f)
    payload["name"] = name
    resp = requests.post(f"{N8N_API_URL}/api/v1/workflows", headers=HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    wf = resp.json()
    print(f"Created workflow '{wf['name']}' with ID {wf['id']}")
    return wf["id"]


def update_workflow(workflow_id: str, input_path: str):
    with open(input_path) as f:
        payload = json.load(f)
    resp = requests.patch(
        f"{N8N_API_URL}/api/v1/workflows/{workflow_id}",
        headers=HEADERS,
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    print(f"Updated workflow {workflow_id}")


def activate_workflow(workflow_id: str):
    resp = requests.patch(
        f"{N8N_API_URL}/api/v1/workflows/{workflow_id}/activate",
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    print(f"Activated workflow {workflow_id}")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-workflows", action="store_true")
    group.add_argument("--get-workflow", metavar="ID")
    group.add_argument("--name", metavar="NAME", help="Name for new workflow (requires --input)")
    group.add_argument("--update", metavar="ID", help="Workflow ID to update (requires --input)")
    group.add_argument("--activate", metavar="ID")
    parser.add_argument("--input", metavar="PATH", help="Path to workflow JSON file")
    args = parser.parse_args()

    if args.list_workflows:
        list_workflows()
    elif args.get_workflow:
        get_workflow(args.get_workflow)
    elif args.name:
        if not args.input:
            print("Error: --name requires --input")
            sys.exit(1)
        create_workflow(args.name, args.input)
    elif args.update:
        if not args.input:
            print("Error: --update requires --input")
            sys.exit(1)
        update_workflow(args.update, args.input)
    elif args.activate:
        activate_workflow(args.activate)


if __name__ == "__main__":
    main()
