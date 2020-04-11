
import psutil
import subprocess
import asyncio as aio


class RaspberryPi:
    def get_cpu_load(self):
        load = psutil.cpu_percent(interval=None)
        return load

    async def async_get_cpu_load(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.get_cpu_load)

    def reboot(self):
        subprocess.run(['sudo', 'reboot'])