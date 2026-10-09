# Go1 deployment status

The Isaac Lab Go1 task, policy export, URDF and joint ordering are supported by
this repository. The upstream `deploy/robots/go2` executable uses Unitree SDK2
and Go2 DDS message types. Go1 hardware uses a different low-level SDK/API, so
that executable must not be relabelled or run on Go1.

For Go1 deployment, reuse the exported HIMLoco policy together with a verified
Go1 low-level runner that provides the same 12-joint order and observation
normalization recorded in `deploy.yaml`. Hardware deployment remains a separate
safety-checked step; this adaptation currently validates the Isaac Lab training
and export path.
