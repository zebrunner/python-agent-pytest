from distutils.core import setup
setup(
  name = 'zebrunnerpy',
  packages = ['zebrunnerpy'],
  version = '0.1.2',
  license='MIT',
  description = 'Python3 connector for Zebrunner-reporting',
  author = 'Sergey Shukalovich',
  author_email = 'sshukalovich@solvd.com',
  url = 'https://github.com/shukal94/zebrunner_py',
  download_url = 'https://github.com/shukal94/zebrunner_py',
  keywords = ['automation', 'zebrunner', 'testing'],
  install_requires=[
          'pytest',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
