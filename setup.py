from setuptools import setup, find_packages

setup(
    name='yourpackage',
    version='0.1',
    py_modules=['tagmodule', 'tagmodule.new_item', 'tagmodule.tagdb'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'terminaltables',
        'click_completion'
    ],
    entry_points='''
        [console_scripts]
        noted=noted:cli
    ''',
)
