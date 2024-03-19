=======================
MLConf
=======================

.. role:: bash(code)
   :language: bash


A lightweight pure python configuration manager geared towards machine learning projects.

Installation
------------

1. First, make sure you have Python 3.6+ installed.
2. Clone this repository: :bash:`git clone https://github.com/your-username/your-repo.git`
3. Change into the project directory: :bash:`cd your-repo`
4. Install the package: :bash:`pip install -e ./`

Quickstart
-----

To use MLConf, you can create a new configuration file in your project directory. Here's an example of a simple configuration file:

.. code-block:: yaml

    # config.yaml
    model:
        name: "your_model"
        params:
            learning_rate: 0.001
            num_layers: 3
            num_units: 128
        data:
            path: "path/to/your/data.csv"
            target: "target_column"

Then, you can load the configuration file in your Python code and access the parameters like this:

.. code-block:: python

    import mlconf
    config = mlconf.load_argparse()
    print(config)

and run your code with the `--config` argument:

.. code-block:: bash

    python your_script.py --config config.yaml

You should see the following output:

.. code-block:: yaml


    model:
    name: your_model
    params:
        learning_rate: 0.001
        num_layers: 3.0
        num_units: 128.0
    data:
        path: path/to/your/data.csv
        target: target_column

The config values can be accessed like a dictionary or using the `.` notation:

.. code-block:: python

    print(config["model"]["name"])  # your_model
    print(config["model"]["params"]["learning_rate"])  # 0.001
    print(config.data.path)  # path/to/your/data.csv

Any of the values can be overridden using command line arguments. For example, you can override the `learning_rate` parameter like this:

.. code-block:: bash

    python your_script.py --config config.yaml --model.params.learning_rate 0.01


Contributing
------------

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them.
4. Push to your forked repository.
5. Submit a pull request.

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.