"""
APZmedia ComfyUI JSON and CSV Utility Nodes
A collection of utility nodes for JSON and CSV data processing in ComfyUI
"""

import os
import importlib.util

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


def load_nodes():
    nodes_dir = os.path.join(os.path.dirname(__file__), "nodes")
    if not os.path.exists(nodes_dir):
        return

    for filename in os.listdir(nodes_dir):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        module_name = filename[:-3]
        module_path = os.path.join(nodes_dir, filename)

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "NODE_CLASS_MAPPINGS"):
                NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
            if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
        except Exception as e:
            print(f"[APZmedia] Failed to load {filename}: {e}")


load_nodes()

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
