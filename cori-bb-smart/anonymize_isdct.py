#!/usr/bin/env python3
"""
Provide a CLI interface for :meth:`tokio.connectors.nersc_isdct.NerscIsdct.to_dataframe`
and :meth:`tokio.connectors.nersc_isdct.NerscIsdct.save_cache` methods.
"""

import hashlib

import argparse
import tokio.connectors.nersc_isdct

def main(argv=None):
    """Entry point for the CLI interface
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("isdctfile", type=str, help="NERSC ISDCT dump to process")
    parser.add_argument("-j", "--json", action="store_true", default=True,
                        help="return output in JSON format")
    parser.add_argument("-c", "--csv", action="store_true", help="return output in CSV format")
    parser.add_argument("-o", "--output", type=str, default=None, help="output file")
    args = parser.parse_args(argv)

    # Read from a cache file
    isdct_data = tokio.connectors.nersc_isdct.NerscIsdct(args.isdctfile)

    # anonymize
    del_keys = set()
    anon_data = {}
    for key, val in isdct_data.items():
        serialno, idx = key.split('-', 1)
        new_key = hashlib.md5(str(serialno).encode()).hexdigest() + "-" + idx
        anon_data[new_key] = val
        del_keys.add(key)
        if 'serial_number' in anon_data[new_key]:
            anon_data[new_key]['serial_number'] = new_key
        else:
            raise KeyError("serial_number is not a key in key")

    for key, val in anon_data.items():
        #print("Adding %s" % key)
        isdct_data[key] = val
    for del_key in del_keys:
        #print("Deleting %s" % del_key)
        del isdct_data[del_key]

    # Serialize the object
    cache_file = args.output
    if cache_file is not None:
        print("Caching to %s" % cache_file)

    if args.csv:
        if cache_file is None:
            print(isdct_data.to_dataframe().to_csv())
        else:
            isdct_data.to_dataframe().to_csv(cache_file)
    elif args.json:
        isdct_data.save_cache(cache_file)
    else:
        raise Exception("No output format specified")

if __name__ == "__main__":
    main()
