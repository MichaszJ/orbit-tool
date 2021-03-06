import numpy as np

from solve_ode_ivp import rk_45


def periapsis_to_true_anomaly(eccentricity, angular_momentum, true_anomaly, mu=398600):
    orbit_period = (2 * np.pi / mu ** 2) * (angular_momentum / np.sqrt(1 - eccentricity ** 2)) ** 3

    eccentric_anomaly = 2 * np.arctan(np.sqrt((1 - eccentricity) / (1 + eccentricity) * np.tan(true_anomaly / 2)))
    mean_anomaly = eccentric_anomaly - eccentricity * np.sin(eccentric_anomaly)

    time = (mean_anomaly / (2 * np.pi)) * orbit_period

    return time


def two_body_propagator(t_init,
                        t_final,
                        mass_1,
                        mass_2,
                        initial_conditions,
                        grav_constant=6.67259e-11,
                        step_size=None,
                        tolerance=0.2,
                        beta=0.8):

    """
    Solves a general two-body problem using the rk_45 ode solver
    Initial conditions is a list of the form: [x_1, y_1, z_1, vx_1, vy_1, vz_1, x_2, y_2, z_2, vx_2, vy_2, vz_2]

    Returns a list, the first element being an array of each input variable, the second element being the times of each
        point. The solution array is the same form as the input
    """

    mu_1 = grav_constant * mass_1
    mu_2 = grav_constant * mass_2

    def differential_system(t, s):
        x_1, y_1, z_1, vx_1, vy_1, vz_1, x_2, y_2, z_2, vx_2, vy_2, vz_2 = s

        r = np.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2 + (z_2 - z_1) ** 2)

        return_vector = [
            vx_1,
            vy_1,
            vz_1,
            mu_2 * (x_2 - x_1) / r ** 3,
            mu_2 * (y_2 - y_1) / r ** 3,
            mu_2 * (z_2 - z_1) / r ** 3,
            vx_2,
            vy_2,
            vz_2,
            mu_1 * (x_1 - x_2) / r ** 3,
            mu_1 * (y_1 - y_2) / r ** 3,
            mu_1 * (z_1 - z_2) / r ** 3,
        ]

        return return_vector

    solution_out, time_out = rk_45(differential_system, initial_conditions, t_init, t_final, step_size, tolerance, beta)

    return solution_out, time_out


def three_body_cr_propagator(t_init,
                             t_final,
                             mass_1,
                             mass_2,
                             r_12,
                             initial_conditions,
                             grav_constant=6.67259e-11,
                             step_size=None,
                             tolerance=0.2,
                             beta=0.8):

    """
    Solves the circular restricted three-body problem using the rk_45 ode solver
    Initial conditions is a list of the form: [x, y, z, v_x, v_y, v_z]

    Returns a list, the first element being an array of each input variable, the second element being the times of each
        point. The solution array is the same form as the input
    """

    mu_1 = grav_constant * mass_1
    mu_2 = grav_constant * mass_2

    pi_1 = mass_1 / (mass_1 + mass_2)
    pi_2 = mass_2 / (mass_1 + mass_2)

    omega = np.sqrt(grav_constant * (mass_1 + mass_2) / r_12 ** 3)

    def differential_system(t, s):
        x, y, z, v_x, v_y, v_z = s

        r_1 = np.sqrt((x + pi_2 * r_12) ** 2 + y ** 2 + z ** 2)
        r_2 = np.sqrt((x - pi_1 * r_12) ** 2 + y ** 2 + z ** 2)

        return_vector = [
            v_x,
            v_y,
            v_z,
            2 * omega * v_y + x * omega ** 2 - (mu_1 / r_1 ** 3) * (x + pi_2 * r_12) - (mu_2 / r_2 ** 3) * (
                    x - pi_1 * r_12),
            -2 * omega * v_x + y * omega ** 2 - (mu_1 / r_1 ** 3) * y - (mu_2 / r_2 ** 3) * y,
            -(mu_1 / r_1 ** 3) * z - (mu_2 / r_2 ** 3) * z
        ]

        return return_vector

    solution_out, time_out = rk_45(differential_system, initial_conditions, t_init, t_final, step_size, tolerance, beta)

    return solution_out, time_out


def three_body_propagator(t_init,
                          t_final,
                          mass_1,
                          mass_2,
                          mass_3,
                          initial_conditions,
                          grav_constant=6.67259e-11,
                          step_size=None,
                          tolerance=0.2,
                          beta=0.8):

    """
    Solves the general three-body problem using the rk_45 ode solver
    Initial conditions is a list of the form:
        [x_1, y_1, z_1, vx_1, vy_1, vz_1, x_2, y_2, z_2, vx_2, vy_2, vz_2, x_3, y_3, z_3, vx_3, vy_3, vz_3]

    Returns a list, the first element being an array of each input variable, the second element being the times of each
        point. The solution array is the same form as the input
    """

    mu_1 = grav_constant * mass_1
    mu_2 = grav_constant * mass_2
    mu_3 = grav_constant * mass_3

    def differential_system(t, s):
        x_1, y_1, z_1, vx_1, vy_1, vz_1, x_2, y_2, z_2, vx_2, vy_2, vz_2, x_3, y_3, z_3, vx_3, vy_3, vz_3 = s

        r_12 = np.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2 + (z_2 - z_1) ** 2)
        r_13 = np.sqrt((x_3 - x_1) ** 2 + (y_3 - y_1) ** 2 + (z_3 - z_1) ** 2)
        r_32 = np.sqrt((x_3 - x_2) ** 2 + (y_3 - y_2) ** 2 + (z_3 - z_2) ** 2)

        return_vector = [
            vx_1,
            vy_1,
            vz_1,
            mu_2 * (x_2 - x_1) / r_12 ** 3 + mu_3 * (x_3 - x_1) / r_13 ** 3,
            mu_2 * (y_2 - y_1) / r_12 ** 3 + mu_3 * (y_3 - y_1) / r_13 ** 3,
            mu_2 * (z_2 - z_1) / r_12 ** 3 + mu_3 * (z_3 - z_1) / r_13 ** 3,
            vx_2,
            vy_2,
            vz_2,
            mu_1 * (x_1 - x_2) / r_12 ** 3 + mu_3 * (x_3 - x_2) / r_32 ** 3,
            mu_1 * (y_1 - y_2) / r_12 ** 3 + mu_3 * (y_3 - y_2) / r_32 ** 3,
            mu_1 * (z_1 - z_2) / r_12 ** 3 + mu_3 * (z_3 - z_2) / r_32 ** 3,
            vx_3,
            vy_3,
            vz_3,
            mu_1 * (x_1 - x_3) / r_13 ** 3 + mu_2 * (x_2 - x_3) / r_32 ** 3,
            mu_1 * (y_1 - y_3) / r_13 ** 3 + mu_2 * (y_2 - y_3) / r_32 ** 3,
            mu_1 * (z_1 - z_3) / r_13 ** 3 + mu_2 * (z_2 - z_3) / r_32 ** 3
        ]

        return return_vector

    solution_out, time_out = rk_45(differential_system, initial_conditions, t_init, t_final, step_size, tolerance, beta)

    return solution_out, time_out
