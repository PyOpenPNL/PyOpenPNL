import imp,os
imp.load_dynamic("_openpnl", os.path.join(os.path.dirname(os.path.dirname(__file__)),"openpnl.so"))

