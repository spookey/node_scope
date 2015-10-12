scope_mon
#########

This tool is a quick and dirty hack, don't expect too much..


pull
====

Specify some Freifunk-Nodes to collect some data using ``alfred-json``:

* Hostname
* Clients
* Load
* Traffic (bytes)

The script will store the values as ``./data/<node_id>.json`` with a timestamp.


plot
====

This will collect all json-files in ``./data``, and render graphs using ``pygal``.

They are stored as ``./data/<safe_hostname>_<graph_type>.svg``.


push
====

This collects all svg-files in ``./data``, and uploads them to any remote machine using ``scp``.

Make sure the target folder on the machine exists, and is writable.


Installation & Configuration
============================

Just clone this repository anywhere.

Any time a ``./config.json`` does not exist, or any top level key inside it is missing, the *magic config wizard* is launched.


connection
----------

At some point this Script needs data from the mesh network.
It launches a shell and runs ``alfred-json`` inside it, parsing the json output.

**SSH**: Either run ``alfred-json`` localy or on a remote machine via ``ssh``.

**SSH options**: How to connect to the remote machine.
Think of it like anything between ``ssh`` and ``alfred-json``::

    ssh <your_ssh_options> "alfred-json ..."

**channels**: What Alfred channels to retrieve.

**socket**: Full path to the Alfred socket.

**sudo**: Should only ``alfred-json ...`` be used or ``sudo alfred-json ...``?

**keep**: The full Alfred data can be stored in ``./alfred_raw.json``.
Do turn this off in production!


targets
-------

List of Nodes to collect data from.

Use either the **exact Hostname**, the **MAC-Address** or the **Node ID**.


upload
------

**SSH options**: Same as above.
Think of it like anything between ``scp`` and the svg-files to upload::

    scp ./data/<plots>.svg <your_ssh_options>:<target_folder>/

**folder**: The location on the remote machine where to upload to.
