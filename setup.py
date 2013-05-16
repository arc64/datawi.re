from setuptools import setup, find_packages

setup(name='datawire',
      version='0.1',
      description="An act of daily journalism",
      long_description="",
      classifiers=[],
      keywords='data queue wire service processing matching',
      author='Friedrich Lindenberg, Annabel Church',
      author_email='info@datawi.re',
      url='http://datawi.re',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
