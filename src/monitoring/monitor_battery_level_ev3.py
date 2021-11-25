from ev3dev2.power import PowerSupply


def get_battery_level_ev3():
    # not sure why, but I need to multiply measured_voltage with 10 otherwise it is below min_voltage
    return (((PowerSupply().measured_voltage * 10) - PowerSupply().min_voltage) /
            (PowerSupply().max_voltage - PowerSupply().min_voltage)) * 100
