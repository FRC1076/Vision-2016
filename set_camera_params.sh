# These are the commands to confgure the camera.

v4l2-ctl --device=/dev/video0 -c gain_automatic=0 -c white_balance_automatic=0 -c exposure=128 -c gain=0 -c auto_exposure=0 -c brightness=0 -c hue=-32 -c saturation=96
