"""Validate the bundled Go1 description without requiring Isaac Sim."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "source/himloco_lab/himloco_lab/assets/robots/go1"
URDF = ASSET / "urdf/go1.urdf"
EXPECTED_JOINTS = [
    f"{leg}_{joint}_joint"
    for leg in ("FR", "FL", "RR", "RL")
    for joint in ("hip", "thigh", "calf")
]
EXPECTED_FEET = [f"{leg}_foot" for leg in ("FR", "FL", "RR", "RL")]


def main():
    tree = ET.parse(URDF)
    root = tree.getroot()
    links = {element.attrib["name"] for element in root.findall("link")}
    movable = [
        element.attrib["name"]
        for element in root.findall("joint")
        if element.attrib.get("type") not in ("fixed", "floating")
    ]
    assert movable == EXPECTED_JOINTS, (movable, EXPECTED_JOINTS)
    assert set(EXPECTED_FEET).issubset(links)
    assert "base" in links and "trunk" in links
    mesh_paths = []
    for mesh in root.findall(".//mesh"):
        filename = mesh.attrib["filename"]
        assert not re.match(r"^[a-zA-Z]+://", filename), filename
        path = (URDF.parent / filename).resolve()
        assert path.is_file(), path
        mesh_paths.append(path)
    assert len(set(mesh_paths)) == 5
    limits = {
        joint.attrib["name"]: joint.find("limit")
        for joint in root.findall("joint")
        if joint.attrib["name"] in EXPECTED_JOINTS
    }
    assert all(limit is not None for limit in limits.values())
    assert all(float(limit.attrib["effort"]) == 33.5 for limit in limits.values())
    print(
        "Go1 asset valid: %d movable joints, %d feet, %d meshes"
        % (len(movable), len(EXPECTED_FEET), len(set(mesh_paths)))
    )


if __name__ == "__main__":
    main()
