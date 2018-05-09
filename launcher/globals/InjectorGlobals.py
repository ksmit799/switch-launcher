"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

# The address where the RCM payload is placed.
# This is fixed for most device.
RCM_PAYLOAD_ADDR = 0x40010000

# The address where the user payload is expected to begin.
PAYLOAD_START_ADDR = 0x40010E40

# Specify the range of addresses where we should inject oct
# payload address.
STACK_SPRAY_START = 0x40014E40
STACK_SPRAY_END = 0x40017000

# USB constants used.
STANDARD_REQUEST_DEVICE_TO_HOST_TO_ENDPOINT = 0x82
STANDARD_REQUEST_DEVICE_TO_HOST_TO_DEVICE = 0x80
GET_DESCRIPTOR = 0x6
GET_CONFIGURATION = 0x8

# Interface requests.
GET_STATUS = 0x0

# Default Nintendo Switch RCM VID (VendorID) and PID (ProductID).
DEFAULT_VID = 0x0955
DEFAULT_PID = 0x7321

# The addresses of the DMA buffers we can trigger a copy _from_.
COPY_BUFFER_ADDRESSES = [0x40005000, 0x40009000]

# The address just after the end of the device's stack.
STACK_END = 0x40010000