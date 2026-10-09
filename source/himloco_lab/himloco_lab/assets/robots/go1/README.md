# Unitree Go1 asset

This directory contains the Go1 URDF and meshes used by the existing
`HIMLoco-for-Go2W` Go1 simulation. The files were copied without changing
inertial, collision, joint-limit or mesh data so the Isaac Lab task and the
validated Isaac Gym task share one robot description.

The URDF uses paths relative to `urdf/go1.urdf`:

```text
go1/
├── urdf/go1.urdf
└── meshes/
    ├── trunk.stl
    ├── hip.stl
    ├── thigh.stl
    ├── thigh_mirror.stl
    └── calf.stl
```

Joint order used by HIMLoco and the Unitree low-level interface:

```text
FR_hip_joint, FR_thigh_joint, FR_calf_joint,
FL_hip_joint, FL_thigh_joint, FL_calf_joint,
RR_hip_joint, RR_thigh_joint, RR_calf_joint,
RL_hip_joint, RL_thigh_joint, RL_calf_joint
```

The source description is derived from Unitree's public Go1 robot description.
Confirm the upstream asset license before redistributing these mesh files in a
binary product.
