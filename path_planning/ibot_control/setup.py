from setuptools import setup

package_name = 'ibot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='phanikiran',
    maintainer_email='phanikiran1169@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ibot_steer = ibot_control.ibot_steer:main',
            'ibot_edf_thrust_control = ibot_control.ibot_edf_thrust_control:main'
        ],
    },
)
