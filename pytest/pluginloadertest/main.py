#!/usr/local/bin/python
import studioenv
from studio.dept.td.utils.plugin.pluginloader import PluginLoader

def main():
    loader = PluginLoader(["foo"], [object])
    plugins = loader.getPluginList()
    print plugins

if __name__ == "__main__":
    main()
