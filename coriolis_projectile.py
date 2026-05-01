"""
Projectile motion with drag and Earth rotation effects.

This script simulates the trajectory of a projectile under gravity, linear drag,
Coriolis acceleration and centrifugal acceleration. The result is compared with
a reference trajectory that only includes gravity and drag.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class SimulationConfig:
    earth_radius: float = 6.4e6
    gravity: float = 9.81
    earth_angular_speed: float = 7.272205e-5

    drag_coefficient: float = 0.15
    dt: float = 0.1

    initial_height: float = 1.5
    initial_velocity: tuple = (0.0, 50.0, 50.0)

    latitude_angle: float = np.pi / 3


def earth_rotation_vector(config):
    """
    Return the Earth angular velocity vector.

    The vector is oriented according to the selected latitude angle.
    """
    direction = np.array([
        0.0,
        np.cos(config.latitude_angle),
        np.sin(config.latitude_angle)
    ])

    return config.earth_angular_speed * direction


def coriolis_acceleration(velocity, omega):
    """Return Coriolis acceleration."""
    return 2 * np.cross(velocity, omega)


def centrifugal_acceleration(position, omega):
    """Return centrifugal acceleration."""
    return np.cross(np.cross(omega, position), omega)


def acceleration_with_rotation(position, velocity, omega, config):
    """Total acceleration including drag and Earth rotation effects."""
    gravity_acc = np.array([0.0, 0.0, -config.gravity])
    drag_acc = -config.drag_coefficient * velocity

    return (
        gravity_acc
        + drag_acc
        + coriolis_acceleration(velocity, omega)
        + centrifugal_acceleration(position, omega)
    )


def acceleration_reference(velocity, config):
    """Reference acceleration with gravity and drag only."""
    gravity_acc = np.array([0.0, 0.0, -config.gravity])
    drag_acc = -config.drag_coefficient * velocity

    return gravity_acc + drag_acc


def simulate_with_rotation(config):
    """Simulate projectile motion including Earth rotation effects."""
    omega = earth_rotation_vector(config)

    position = np.array([
        0.0,
        0.0,
        config.earth_radius + config.initial_height
    ])

    velocity = np.array(config.initial_velocity, dtype=float)

    times = [0.0]
    positions = [position.copy()]
    velocities = [velocity.copy()]
    distance = 0.0

    while positions[-1][2] > config.earth_radius:
        current_position = positions[-1]
        current_velocity = velocities[-1]

        acceleration = acceleration_with_rotation(
            current_position,
            current_velocity,
            omega,
            config
        )

        new_velocity = current_velocity + acceleration * config.dt
        new_position = current_position + new_velocity * config.dt

        distance += np.linalg.norm(new_position - current_position)

        velocities.append(new_velocity)
        positions.append(new_position)
        times.append(times[-1] + config.dt)

    return np.array(times), np.array(positions), np.array(velocities), distance


def simulate_reference(config, n_steps):
    """Simulate reference motion without Earth rotation effects."""
    position = np.array([
        0.0,
        0.0,
        config.earth_radius + config.initial_height
    ])

    velocity = np.array(config.initial_velocity, dtype=float)

    positions = [position.copy()]
    velocities = [velocity.copy()]

    for _ in range(n_steps):
        acceleration = acceleration_reference(velocity, config)

        new_velocity = velocity + acceleration * config.dt
        new_position = position + new_velocity * config.dt

        velocity = new_velocity
        position = new_position

        velocities.append(velocity.copy())
        positions.append(position.copy())

    return np.array(positions), np.array(velocities)


def convert_to_local_coordinates(positions, earth_radius):
    """Convert absolute positions to local coordinates above Earth surface."""
    local_positions = positions.copy()
    local_positions[:, 2] -= earth_radius

    return local_positions


def plot_trajectories(rotating_positions, reference_positions):
    """Plot both trajectories in 3D."""
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(
        rotating_positions[:, 0],
        rotating_positions[:, 1],
        rotating_positions[:, 2],
        label="With Earth rotation"
    )

    ax.plot(
        reference_positions[:, 0],
        reference_positions[:, 1],
        reference_positions[:, 2],
        label="Reference: gravity + drag"
    )

    ax.set_title("Projectile trajectory with Coriolis and centrifugal effects")
    ax.set_xlabel("x position (m)")
    ax.set_ylabel("y position (m)")
    ax.set_zlabel("height (m)")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()

    return fig


def main():
    config = SimulationConfig()

    times, positions, velocities, distance = simulate_with_rotation(config)

    reference_positions, reference_velocities = simulate_reference(
        config,
        n_steps=len(times) - 1
    )

    local_positions = convert_to_local_coordinates(
        positions,
        config.earth_radius
    )

    local_reference_positions = convert_to_local_coordinates(
        reference_positions,
        config.earth_radius
    )

    print(f"Flight time: {times[-1]:.3f} s")
    print(f"Distance traveled: {distance:.3f} m")

    horizontal_deviation = np.linalg.norm(
        local_positions[-1, :2] - local_reference_positions[-1, :2]
    )

    print(f"Horizontal deviation due to rotation: {horizontal_deviation:.6f} m")

    plot_trajectories(local_positions, local_reference_positions)

    plt.show()


if __name__ == "__main__":
    main()