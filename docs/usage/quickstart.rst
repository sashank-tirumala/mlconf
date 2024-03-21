Quickstart
----------------
.. role:: bash(code)
   :language: bash

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
