import os
import sys
import subprocess
import string
import setuptools
import setuptools_scm

if sys.version_info < (3, 6):
    print("Python 3.6 or higher required, please upgrade.")
    sys.exit(1)

on_rtd = os.environ.get('READTHEDOCS') == 'True'

TAG_VERSION = setuptools_scm.get_version(parentdir_prefix_version='ffcx-',
                                         version_scheme='post-release').split(".", 3)[:3]
TAG_VERSION = '.'.join(TAG_VERSION)
RESTRICT_REQUIREMENTS = ">=" + TAG_VERSION
print(RESTRICT_REQUIREMENTS)

if on_rtd:
    REQUIREMENTS = []
else:
    REQUIREMENTS = [
        "numpy",
        "cffi",
        "fenics-fiat{}".format(RESTRICT_REQUIREMENTS),
        "fenics-ufl{}".format(RESTRICT_REQUIREMENTS),
    ]

ENTRY_POINTS = {'console_scripts': ['ffcx = ffcx.__main__:main']}

AUTHORS = """\
Anders Logg, Kristian Oelgaard, Marie Rognes, Garth N. Wells,
Martin Sandve Alnæs, Hans Petter Langtangen, Kent-Andre Mardal,
Ola Skavhaug, et al.
"""

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)
Operating System :: POSIX
Operating System :: POSIX :: Linux
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Scientific/Engineering :: Mathematics
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Code Generators
"""


def get_git_commit_hash():
    """Return git commit hash of currently checked out revision or "unknown"."""
    try:
        hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    except (OSError, subprocess.CalledProcessError) as e:
        print('Retrieving git commit hash did not succeed with exception:')
        print('"{}"'.format(e))
        print()
        print('Stored git commit hash will be set to "unknown"!')
        return "unknown"
    else:
        return hash.decode("ascii").strip()


def write_config_file(infile, outfile, variables={}):
    """Write config file based on template."""

    print(variables)
    class AtTemplate(string.Template):
        delimiter = "$"

    s = AtTemplate(open(infile, "r").read())
    s = s.substitute(**variables)
    with open(outfile, "w") as a:
        a.write(s)


def generate_git_hash_file(GIT_COMMIT_HASH):
    """Generate module with git hash."""
    write_config_file(
        os.path.join("ffcx", "git_commit_hash.py.in"),
        os.path.join("ffcx", "git_commit_hash.py"),
        variables={'GIT_COMMIT_HASH': GIT_COMMIT_HASH})


def generate_ufc_h_file(version):
    """Generate ufc.h with version."""
    write_config_file(
        os.path.join("ffcx", "codegeneration", "ufc.h.in"),
        os.path.join("ffcx", "codegeneration", "ufc.h"),
        variables={'UFC_VERSION': version})


def run_install():
    """Run installation."""

    # Get common variables
    GIT_COMMIT_HASH = get_git_commit_hash()

    # Scripts list
    entry_points = ENTRY_POINTS

    # Generate module with git hash from template
    generate_git_hash_file(GIT_COMMIT_HASH)

    generate_ufc_h_file(TAG_VERSION)

    # Call distutils to perform installation
    setuptools.setup(
        name="fenics-ffcx",
        description="The FEniCS Form Compiler",
        author=AUTHORS,
        classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
        license="LGPL version 3 or later",
        author_email="fenics-dev@googlegroups.com",
        maintainer_email="fenics-dev@googlegroups.com",
        use_scm_version={'parentdir_prefix_version': 'ffcx-'},
        setup_requires=["setuptools_scm"],
        url="https://github.com/FEniCS/ffcx/",
        platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
        packages=[
            "ffcx",
            "ffcx.codegeneration",
            "ffcx.codegeneration.C",
            "ffcx.ir",
            "ffcx.ir.analysis",
        ],
        package_dir={"ffcx": "ffcx"},
        package_data={"ffcx": [os.path.join('codegeneration', 'ufc.h'),
                               os.path.join('codegeneration', 'ufc_geometry.h')]},
        entry_points=entry_points,
        install_requires=REQUIREMENTS,
        zip_safe=False)


if __name__ == "__main__":
    run_install()
