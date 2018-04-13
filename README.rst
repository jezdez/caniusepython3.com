Can I Use Python 3
==================

.. image:: https://requires.io/github/caniusepython3/caniusepython3.com/requirements.png?branch=master
   :target: https://requires.io/github/caniusepython3/caniusepython3.com/requirements/?branch=master
   :alt: Requirements Status

This is the companion site to the CLI tool caniusepython3_ available at
caniusepython3.com_.

Workflow
--------

User perspective
^^^^^^^^^^^^^^^^

- Go to frontpage
- Find form with textarea to enter requirements
- Enter one or more package names or URLs to requirements files
- Click on submit
- Find yourself on a detail page of the check /checks/<uuid>
- See the result of the check once it's done
- See a submit button to restart the check

Backend perspective
^^^^^^^^^^^^^^^^^^^

- Render frontpage form
- Once the form is submitted, create a unique check object
- Parse requirements and return error if not parseable
- create celery tasks and them to check object
- Redirect to check detail page with a list of attached tasks
- Render self-updating result list page with each job attached to the check

- Periodically update the trove classifier cache (~30 mins)

.. _caniusepython3: https://pypi.python.org/pypi/caniusepython3
.. _caniusepython3.com: https://caniusepython3.com
