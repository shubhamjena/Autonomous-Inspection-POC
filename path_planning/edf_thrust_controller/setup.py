from setuptools import setup

package_name = 'edf_thrust_controller'

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
    maintainer='ki2',
    maintainer_email='jena.shubham@outlook.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'edf_thrust_controller_node = edf_thrust_controller.edf_thrust_controller_node:main'
        ],
    },
)
