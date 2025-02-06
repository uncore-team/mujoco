from controller import Controller
from utils import Joint

class ManipulatorArm:
    def __init__(self, controller: Controller = None, joints: list = None):
        '''
        Initializes the ReactorX 200 simulator.

        Args:
            robot_name (str): Name of the robot (default is 'rx200')
        '''
        self.controller = controller
        self.joints = joints

    def _get_joint_servos(self, joint: Joint) -> list:
        '''
        Returns the servos associated with a joint.
        '''
        return self.joints[joint]

    def get_joints_number(self) -> int:
        '''
        Get the number of joints of the arm.
        Returns:
            int: Number of joints.
        '''
        return len(self.joints)

    def close(self):
        self.disable_all_joints_torques()
        self.controller.close()

    def home_joint(self, joint: Joint):
        '''
        Moves a joint to its home (default) position.
        '''
        if Joint.is_valid(joint):
            for servo in self._get_joint_servos(joint):
                servo.home()
        else:
            raise ValueError('Invalid joint ID')

    def home_all_joints(self):
        '''
        Moves all joints to their home (default) positions.
        '''
        for joint in self.joints:
            for servo in self._get_joint_servos(joint):
                servo.home()

    def enable_joint_torque(self, joint: Joint):
        '''
        Enables position control for the servo.
        '''
        if Joint.is_valid(joint):
            for servo in self._get_joint_servos(joint):
                servo.enable_torque()
        else:
            raise ValueError('Invalid joint ID')

    def enable_all_joints_torques(self):
        '''
        Enables position control for all servos.
        '''
        for joint in self.joints:
            for servo in self._get_joint_servos(joint):
                servo.enable_torque()

    def disable_joint_torque(self, joint: Joint):
        '''
        Disables position control for the servo.
        '''
        if Joint.is_valid(joint):
            for servo in self._get_joint_servos(joint):
                servo.disable_torque()                
        else:
            raise ValueError('Invalid joint ID')

    def disable_all_joints_torques(self):
        '''
        Disables position control for all servos.
        '''
        for joint in self.joints:
            for servo in self._get_joint_servos(joint):
                servo.disable_torque()

    def get_joint_torque(self, joint: Joint) -> float:
        '''
        Gets the current torque/force percent of the joint.

        Args:
        :joint (Joint): Joint to get the torque/force from.

        Returns:
        :float: The current torque percent.
        '''
        if Joint.is_valid(joint):
            servos = self._get_joint_servos(joint)
            return servos[0].get_torque()  # Get torque from the first servo
        else:
            raise ValueError('Invalid joint ID')

    def get_all_joints_torques(self) -> list:
        '''
        Gets the current torques/forces percent of all servos.

        Returns:
            list: A list of current torques/forces for all joints.
        '''
        torques = []
        for joint in self.joints:
            servos = self._get_joint_servos(joint)
            torques.append(
                servos[0].get_torque()  # Get velocity from the first servo
            )
        return torques

    def get_joint_torque(self, joint: Joint):
        '''
        '''
        if Joint.is_valid(joint):
            servos = self._get_joint_servos(joint)
            return servos[0].get_torque()  # Get position from the first servo
        else:
            raise ValueError(f'Invalid joint ID: {joint}')

    def get_all_joints_torques(self):
        '''
        '''
        positions = []
        for joint in self.joints:
            servos = self._get_joint_servos(joint)
            positions.append(
                servos[0].get_torque()  # Get position from the first servo
            )
        return positions

    def set_joint_velocity(self, joint: Joint, rpm: float):
        '''
        Sets the maximum velocity of the servo in RPM.
        This limits the rate of change of the target position.

        Args:
            joint (Joint): Joint to control (e.g., Shoulder, Elbow).
            rpm (float): Velocity in RPM (0-100).
        '''
        if Joint.is_valid(joint):
            for servo in self._get_joint_servos(joint):
                servo.set_velocity(rpm)
        else:
            raise ValueError('Invalid joint ID')

    def set_all_joints_velocities(self, velocities: list):
        '''
        Sets the maximum velocities for all servos in RPM.
        This limits the rate of change of the target positions for all joints.

        Args:
            velocities (list): List of velocities in RPM for each joint.
        '''
        if len(velocities) != len(self.joints):
            raise ValueError('Number of velocities must match the number of joints.')

        for index, joint in enumerate(self.joints):
            for servo in self._get_joint_servos(joint):
                servo.set_velocity(velocities[index])

    def get_joint_velocity(self, joint: Joint) -> float:
        '''
        Gets the current velocity of the servo in RPM.

        Args:
            joint (Joint): Joint to get the velocity from.

        Returns:
            float: The current velocity in RPM.
        '''
        if Joint.is_valid(joint):
            servos = self._get_joint_servos(joint)
            return servos[0].get_velocity()  # Get velocity from the first servo
        else:
            raise ValueError('Invalid joint ID')

    def get_all_joints_velocities(self) -> list:
        '''
        Gets the current velocities of all servos in RPM.

        Returns:
            list: A list of current velocities in RPM for all joints.
        '''
        velocities = []
        for joint in self.joints:
            servos = self._get_joint_servos(joint)
            velocities.append(
                servos[0].get_velocity()  # Get velocity from the first servo
            )
        return velocities

    def open_gripper(self):
        '''
        Opens the gripper by moving it to its home position.
        '''
        for servo in self._get_joint_servos(Joint.Gripper):
            # if not isinstance(servo, Gripper):
            #     raise TypeError(f'Expected joint to be of type GripperServo, but got {type(servo).__name__} instead.')
            servo.open()

    def close_gripper(self):
        '''
        Closes the gripper by moving it to its home position.
        '''
        for servo in self._get_joint_servos(Joint.Gripper):
            # if not isinstance(servo, Gripper):
            #     raise TypeError(f'Expected joint to be of type GripperServo, but got {type(servo).__name__} instead.')
            servo.close()

    def set_joint_position(self, joint: Joint, position: float):
        '''
        Sets the target position of a specific joint (in degrees).

        Parameters:
            joint (Joint): Joint to move.
            position (float): Target position in degrees.
        '''
        if Joint.is_valid(joint):
            for servo in self._get_joint_servos(joint):
                servo.set_position(position)
        else:
            raise ValueError(f'Invalid joint ID: {joint}')

    def set_all_joint_positions(self, positions):
        '''
        Sets the target positions for all joints in degrees.

        Parameters:
        positions (list): A list of positions in degrees for each joint.
        '''
        if len(positions) != len(self.joints):
            raise ValueError('Number of positions must match the number of joints.')

        for index, joint in enumerate(self.joints):
            for servo in self._get_joint_servos(joint):
                servo.set_position(positions[index])

    def get_joint_position(self, joint: Joint) -> float:
        '''
        Gets the current position of the servo in degrees.

        Args:
            joint (Joint): Joint to get the position from.

        Returns:
            float: The current position of the joint in degrees.
        '''
        if Joint.is_valid(joint):
            servos = self._get_joint_servos(joint)
            return servos[0].get_position()  # Get position from the first servo
        else:
            raise ValueError(f'Invalid joint ID: {joint}')

    def get_all_joint_positions(self):
        '''
        Gets the current positions of all joints in degrees.

        Returns:
        list: A list of current positions in degrees for all joints.
        '''
        positions = []
        for joint in self.joints:
            servos = self._get_joint_servos(joint)
            positions.append(
                servos[0].get_position()  # Get position from the first servo
            )
        return positions
