

class Calibration:
    #   Calibrate.

    #   Determine min max

    #   count when something is out of calibrated range (atypical)

    count_to_calibrate = 100
    deviations_off = 2
    jump_deviation_multiplier = 5

    def __init__(self):
        self.xs = []
        self.x_diff = None
        self.x_avg = None

        self.ys = []
        self.y_diff = None
        self.y_avg = None

        self.zs = []
        self.z_diff = None
        self.z_avg = None

        self.is_calibrated = False
        self.count = 0
        self.count_off_calibration = 0

    def is_jump(self, x, y, z):
        #   Xs
        if x < (self.x_avg - (self.x_diff * self.jump_deviation_multiplier)) or x > (self.x_avg + (self.x_diff * self.jump_deviation_multiplier)):
            return True

        #   Ys
        if y < (self.y_avg - (self.y_diff * self.jump_deviation_multiplier)) or y > (self.y_avg + (self.y_diff * self.jump_deviation_multiplier)):
            return True

        #   Zs
        if z < (self.z_avg - (self.z_diff * self.jump_deviation_multiplier)) or z > (self.z_avg + (self.z_diff * self.jump_deviation_multiplier)):
            return True

        return False

    def is_in_still_range(self, x, y, z):
        #   Xs
        if (self.x_avg - (self.x_diff * self.deviations_off)) <= x <= (self.x_avg + (self.x_diff * self.deviations_off)):
            return True

        #   Ys
        if (self.y_avg - (self.y_diff * self.deviations_off)) <= y <= (self.y_avg + (self.y_diff * self.deviations_off)):
            return True

        #   Zs
        if (self.z_avg - (self.z_diff * self.deviations_off)) <= y <= (self.z_avg + (self.z_diff * self.deviations_off)):
            return True

        return False

    def get_value(self, x, y, z):
        """
        :param x:
        :param y:
        :param z:
        :return: tuple (corrected_x, corrected_y, corrected_z, is_calibrated
        """
        if self.is_calibrated:
            if self.is_jump(x, y, z):
                x = (x - self.x_avg) if self.x_avg > 0 else (x + self.x_avg)
                y = (x - self.y_avg) if self.y_avg > 0 else (x + self.y_avg)
                z = (x - self.z_avg) if self.z_avg > 0 else (x + self.z_avg)
                return (x, y, z, True)

            #   not a jump, so add to count.
            self.count += 1
            self.count_off_calibration += 0 if self.is_in_still_range(x, y, z) else 1

            if self.count == self.count_to_calibrate:
                #   value of calibration is whether it hits 50% of the time.
                self.is_calibrated = (self.count_off_calibration / self.count_to_calibrate) < 0.5
                #   reset stuff.
                self.count_off_calibration = 0
                self.count = 0
                pass


            #   if in calibration range, return zero values
            return 0, 0, 0, True
        else:
            self.xs.append(x)
            self.ys.append(y)
            self.zs.append(z)
            if len(self.xs) == self.count_to_calibrate:
                self.set_range()
            return x, y, z, False

    @staticmethod
    def get_average(value_array):
        return round(sum(value_array) / len(value_array), 3)

    def set_range(self):
        self.x_diff = round((max(self.xs) - min(self.xs)), 3)
        self.x_avg = self.get_average(self.xs)
        self.xs = []

        self.y_diff = round((max(self.ys) - min(self.ys)), 3)
        self.y_avg = self.get_average(self.ys)
        self.ys = []

        self.z_diff = round((max(self.zs) - min(self.zs)), 3)
        self.z_avg = self.get_average(self.zs)
        self.zs = []

        print(self.x_avg, self.x_diff, self.y_avg, self.y_diff, self.z_avg, self.z_diff)
        self.is_calibrated = True


if __name__ == '__main__':
    calibration = Calibration()

    with open('/Users/davidhaverberg/PycharmProjects/wobbleBoard/calibrate.txt') as potentials:
        for i, line in enumerate(potentials):
            line = line.strip().split('|')
            x = round(float(line[0]), 3)
            y = round(float(line[1]), 3)
            z = round(float(line[2]), 3)

            calibration.get_value(x, y, z)


