#!/bin/bash
ps uax | grep testStreamingRate.py | grep -v grep | awk {'print $2'} | xargs kill
