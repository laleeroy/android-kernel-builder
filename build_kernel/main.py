from argparse import ArgumentParser
from build_kernel.utils.ak3 import AK3Manager
from build_kernel.utils.device import devices
from build_kernel.utils.dumpvars import dumpvars
from build_kernel.utils.logging import LOGE, LOGI, setup_logging
from build_kernel.utils.make import Make

def main():
	setup_logging()

	parser = ArgumentParser(prog='python3 -m kernel_build')

	parser.add_argument("device", type=str, help="device codename")
	parser.add_argument("-c", "--clean", action='store_true', help="clean before building")
	parser.add_argument("-v", "--verbose", action='store_true', help="verbose logging")

	args = parser.parse_args()

	if not args.device in devices:
		LOGE(f"Device {args.device} not found")
		LOGI("Available devices:\n" + "\n".join(devices.keys()))
		return

	device = devices[args.device]
	make = Make(device)

	dumpvars(device)

	if args.clean is True:
		LOGI("Cleaning before building")
		make.run("clean")
		make.run("mrproper")

	LOGI("Building defconfig")
	make.run([device.TARGET_KERNEL_CONFIG] + device.TARGET_KERNEL_FRAGMENTS)

	LOGI("Building kernel")
	make.run()

	LOGI("Creating AnyKernel3 zip")
	ak3manager = AK3Manager(device)
	zip_filename = ak3manager.create_ak3_zip()

	LOGI(f"Build completed successfully: {zip_filename}")
