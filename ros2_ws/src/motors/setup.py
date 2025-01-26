from setuptools import find_packages, setup

package_name = 'motors'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='computer vision',
    maintainer_email='tamurobomasters@gmail.com',
    description='Controls BALL-E\'s wheels and dump motors',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wheels = motors.wheels:main',
            'listener = motors.subscriber_member_function:main',
        ],
    },
)
