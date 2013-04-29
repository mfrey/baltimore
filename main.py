#!/usr/bin/env python2.7

from representation import scalarfile as scalar

def main():
  scalarParser = scalar.ScalarFile()
  scalarParser.read("test.sca")
#  parser = argparse.ArgumentParser(description='evaluation script for the ara-sim framework')
#  arguments = parser.parse_args()

if __name__ == "__main__":
  main()
