import numpy as np

from moldocker.structure import Complex
from moldocker.dockers.serial import SerialDocker
from moldocker.dockers.mcdocker import MonteCarloDocker


class SuccessDocker(SerialDocker):
    PARSER_NAME = "success"
    HELP = "Docks guests to host until a successful docking is found"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dock_at_point(self, point, attempts):
        hcoords = self.translate_host(point)

        for trial in range(attempts):
            cpx = self.create_new_complex(
                host_coords=hcoords, 
                guest_coords=self.rotate_guest()
            )

            if self.fitness(cpx) >= 0:
                print(f"{trial + 1} attempts to success")
                return [cpx]

        return []


class SuccessMonteCarloDocker(MonteCarloDocker):
    PARSER_NAME = "mcsuccess"
    HELP = "Docks guests to host until a successful docking is found (Monte Carlo version)"

    def dock(self, attempts):
        cpx = Complex(self.host.copy(), self.guest.copy())

        for trial in range(attempts):
            cpx = self.run(cpx, 1)

            if self.fitness(cpx) >= 0:
                print(f"{trial + 1} attempts to success")
                return [cpx]

        return []
